from fastapi import FastAPI, HTTPException
import jsonschema
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from bson import ObjectId
from pymongo import MongoClient

# FastAPI app setup
app = FastAPI()

# MongoDB connection
MONGO_URI = "mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.ecommerce
carts_collection = db['Carts']
users_collection = db['Users']
products_collection = db['Products']

# Define the schema for a cart item
cart_item_schema = {
    "type": "object",
    "properties": {
        "product_id": {"type": "number"},
        "product_name": {"type": "string"},
        "quantity": {"type": "number", "minimum": 1},
        "price": {"type": "number", "minimum": 0}
    },
    "required": ["product_id", "product_name", "quantity", "price"]
}

# Define Pydantic models
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
        
@app.get("/cart/{userId}")
async def get_cart(userId: str):
    cart = carts_collection.find_one({'userId': userId})
    if cart:
        cart['_id'] = str(cart['_id'])
        return cart
    else:
        raise HTTPException(status_code=404, detail="Cart not found")

@app.post("/cart/{userId}")
async def add_to_cart(userId: str, item: CartItem):
    is_valid, error = CartItem.validate_cart_item(item.dict())
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid item data: {error}")
    
    item_dict = item.dict()
    item_dict['userId'] = userId
    result = carts_collection.update_one({'userId': userId}, {'$push': {'items': item_dict}}, upsert=True)
    if result.upserted_id:
        return {"message": "Cart created and item added"}
    else:
        return {"message": "Item added to existing cart"}

@app.put("/cart/{userId}/item/{product_id}")
async def update_cart_item(userId: str, product_id: int, item: CartItem):
    is_valid, error = CartItem.validate_cart_item(item.dict())
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid item data: {error}")
    
    result = carts_collection.update_one(
        {'userId': userId, 'items.product_id': product_id},
        {'$set': {'items.$.quantity': item.quantity, 'items.$.price': item.price}}
    )
    if result.modified_count:
        return {"message": "Item updated"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
