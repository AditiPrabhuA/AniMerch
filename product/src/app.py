from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, validator
from fastapi import FastAPI, HTTPException
import pymongo
from jsonschema import validate, ValidationError

app = FastAPI()

MONGO_URI = "mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('ecommerce')

product_schema = {
    "type": "object",
    "properties": {
        "product_id": {"type": "number"},
        "name": {"type": "string"},
        "price": {"type": "number", "minimum": 0},
        "quantity": {"type": "number"},
        "img_url": {"type":"string"}
    },
    "required": ["product_id", "name", "price", "quantity","img_url"]
}

class Product(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    img_url: str

    @validator('price')
    def price_must_be_positive(cls, value):
        if value < 0:
            raise ValueError('Price must be a positive number')
        return value

def validate_product(data: dict):
    try:
        validate(instance=data, schema=product_schema)
        return True
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/products", response_model=Product)
async def create_product(product: Product):
    validate_product(product.dict())
    result = db.products.insert_one(product.dict())
    product_id = str(result.inserted_id)
    return {"product_id": product_id, **product.dict()}

@app.get("/products", response_model=list[Product])
def get_products():
    products = db.products.find()
    product_list = [
        {
            "product_id": product["product_id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": product["quantity"],
            "img_url": product["img_url"]
        }
        for product in products
    ]
    return product_list

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = db.products.find_one({"product_id": product_id})
    if product:
        product["product_id"] = product["product_id"]
        return Product(**product)
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updated_data: dict):
    validate_product(updated_data)

    product = db.products.find_one({"product_id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = {**product, **updated_data}
    result = db.products.update_one({"product_id": product_id}, {"$set": updated_product})

    if result.modified_count == 1:
        updated_product["product_id"] = updated_product["product_id"]
        return Product(**updated_product)
    else:
        raise HTTPException(status_code=404, detail="Product not found")
    
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    result = db.products.delete_one({"product_id": product_id})
    if result.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)