from fastapi import FastAPI, HTTPException
import jsonschema
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from bson import ObjectId
from pymongo import MongoClient
import requests
import uvicorn
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://ui-service.default.svc.cluster.local:5000"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

MONGO_URI = "mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.ecommerce
carts_collection = db['Carts']
users_collection = db['Users']
products_collection = db['Products']
orders_collection = db['Orders']

cart_item_schema = {
    "type": "object",
    "properties": {
        "product_id": {"type": "number"},
        "product_name": {"type": "string"},
        "quantity": {"type": "number"},
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
        
@app.get("/cart/{userId}")
async def get_cart(userId: str):
    cart = carts_collection.find_one({'userId': userId})
    if cart:
        cart['_id'] = str(cart['_id'])
        return cart
    else:
        carts_collection.insert_one({'userId': userId, 'items': []})
    
def delete_cart_ite(userId: str, product_id: int):
    result = carts_collection.update_one(
        {'userId': userId},
        {'$pull': {'items': {'product_id': product_id}}}
    )
    if result.modified_count:
        return {"message": "Item removed"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

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
                res = delete_cart_ite(userId,product_id)
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
    print(res)
    resj = res.json()
    item.product_name=resj['name']
    item.price=resj['price']
    add_or_update_item_in_cart(userId, item)
    return {"message": "Item added/updated in cart"}

@app.post("/cart/{userId}/delitem/{product_id}")
async def add_or_update_cart_item(userId: str, product_id: int):
    item = CartItem(product_id=product_id, product_name="", quantity=-1, price=0.0)
    res = requests.get(f'http://product-service.default.svc.cluster.local:5001/products/{product_id}')
    print(res)
    resj = res.json()
    item.product_name=resj['name']
    item.price=resj['price']
    add_or_update_item_in_cart(userId, item)
    return {"message": "Item added/updated in cart"}

@app.delete("/cart/{userId}/item/{product_id}")
async def delete_cart_item(userId: str, product_id: int):
    result = carts_collection.update_one(
        {'userId': userId},
        {'$pull': {'items': {'product_id': product_id}}}
    )
    if result.modified_count:
        return {"message": "Item removed"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

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
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    orders_collection.insert_one(order)
    
    carts_collection.delete_one({'userId': userId})
    
    return {"message": "Payment processed successfully"}

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=5004)