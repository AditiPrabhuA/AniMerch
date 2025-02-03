from fastapi import FastAPI, HTTPException
import jsonschema
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
import requests
import uvicorn
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

MONGO_URI = "{mongodb_cluster_uri}"
client = MongoClient(MONGO_URI)
db = client.ecommerce
carts_collection = db['carts']
orders_collection = db['orders']
products_collection = db['products']

#To validate the schema
cart_item_schema = {
    "type": "object",
    "properties": {
        "product_id": {"type": "number"},
        "product_name": {"type": "string"},
        "quantity": {"type": "number", "minimum": 0},
        "price": {"type": "number", "minimum": 0}
    },
    "required": ["product_id", "product_name", "quantity", "price"]
}

class CartItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float

    @classmethod
    def validate_cart_item(cls, data: dict) -> bool:
        try:
            jsonschema.validate(data, cart_item_schema)
            return True, None
        except jsonschema.exceptions.ValidationError as e:
            return False, str(e)
        
class Order(BaseModel):
    id: str
    userId: str
    items: List[CartItem]
    total: float
    date: str
    status: str
        
@app.get("/cart/{userId}")
async def get_cart(userId: str):
    cart = carts_collection.find_one({'userId': userId})
    if cart:
        cart['_id'] = str(cart['_id'])
        return cart
    else:
        carts_collection.insert_one({'userId': userId, 'items': []})

#To update the item numbers in cart +/-
def add_or_update_item_in_cart(userId: str, item: CartItem):
    try:
        jsonschema.validate(item.dict(), cart_item_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid item data: {e}")

    cart = carts_collection.find_one({'userId': userId})
    if cart:
        product_id = item.product_id
        existing_item = next((i for i in cart['items'] if i['product_id'] == product_id), None)
        if existing_item:
            existing_item['quantity'] += item.quantity
            if existing_item['quantity']>0:
                carts_collection.update_one(
                    {'userId': userId, 'items.product_id': product_id},
                    {'$set': {'items.$.quantity': existing_item['quantity']}}
                )
            else:
                carts_collection.update_one(
                    {'userId': userId, 'items.product_id': product_id},
                    {'$pull': {'items': {'product_id': product_id}}}
                )
        else:
            carts_collection.update_one(
                {'userId': userId},
                {'$push': {'items': item.dict()}}
            )
    else:
        carts_collection.insert_one({'userId': userId, 'items': [item.dict()]})

@app.post("/cart/{userId}/additem/{product_id}")
async def add_or_update_cart_item(userId: str, product_id: int):
    item = CartItem(product_id=product_id, product_name="", quantity=1, price=0.0)
    res = requests.get(f'http://product-service.default.svc.cluster.local:5001/products/{product_id}')

    if not res.ok:
        raise HTTPException(status_code=404,detail="Product not found")
    product = res.json()
    item.product_name=product['name']
    item.price=product['price']
    current_cart = carts_collection.find_one({'userId':userId})
    current_cart_quantity = 0
    if current_cart:
        for i in current_cart['items']: 
            if i['product_id']==product_id:
                current_cart_quantity = i['quantity']
                break
    if current_cart_quantity+1 > product['quantity']:
        raise HTTPException(status_code=400,detail=f"cant add more items to cart")

    add_or_update_item_in_cart(userId, item)
    return {"message": "Item added/updated in cart"}

@app.post("/cart/{userId}/delitem/{product_id}")
async def add_or_update_cart_item(userId: str, product_id: int):
    item = CartItem(product_id=product_id, product_name="", quantity=-1, price=0.0)
    res = requests.get(f'http://product-service.default.svc.cluster.local:5001/products/{product_id}')
    print(res)
    product = res.json()
    item.product_name=product['name']
    item.price=product['price']
    add_or_update_item_in_cart(userId, item)
    return {"message": "Item added/updated in cart"}

@app.get("/cart/{userId}/total")
async def calculate_total(userId: str):
    cart = carts_collection.find_one({'userId': userId})
    if cart:
        total = sum(item['price'] * item['quantity'] for item in cart['items'])
        return {"total": total}
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

@app.get("/orders/{userId}")
async def get_orders(userId: str):
    order = orders_collection.find({'userId': userId})
    o = []
    for orders in order:
        if orders:
            orders['_id'] = str(orders['_id'])
            o.append(orders)
    return o

@app.post("/cart/{userId}/process_payment")
async def process_payment(userId: str):
    cart = carts_collection.find_one({'userId': userId})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    order = {
        'userId': userId,
        'items': cart['items'],
        'total': sum(item['price'] * item['quantity'] for item in cart['items']),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'Processing'
    }
    
    orders_collection.insert_one(order)
    
    await asyncio.sleep(10)
    
    current_order = orders_collection.find_one({'userId': userId, '_id': order['_id'], 'status': {'$in': ['Processing', 'Paid']}})
    
    if current_order['status'] == 'Paid':
        for item in cart['items']:
            products_collection.update_one(
                {'product_id': item['product_id']}, 
                {'$inc': {'quantity': -item['quantity']}}
            )
    else:
        orders_collection.update_one(
            {'userId': userId, 'status': 'Processing', '_id': order['_id']},
            {'$set': {'status': 'Not Paid'}}
        )

    carts_collection.delete_one({'userId': userId})
    return {"message": "Order processed"}

@app.post('/cart/{userId}/finalise_payment')
async def finalise_payment(userId: str):
    order = orders_collection.find_one(
        {'userId': userId, 'status': 'Processing'},sort=[('date', -1)]
    )
    if not order:
        raise HTTPException(status_code=404, detail="No processing order found")
    
    orders_collection.update_one(
        {'_id': order['_id']},
        {'$set': {'status': 'Paid'}}
    )
    return {"message": "Payment finalized successfully"}

@app.delete('/cart/{userId}')
async def deleteCart(userId: str):
    carts_collection.delete_one({'userId': userId})


if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=5004)
