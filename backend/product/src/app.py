from pydantic import BaseModel, validator
from fastapi import FastAPI, HTTPException
import pymongo
from jsonschema import validate, ValidationError
from datetime import datetime
app = FastAPI()

MONGO_URI = "{mongodb_cluster_uri}"
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
    product_data = product.dict()
    result = db.products.insert_one(product_data)
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
        return Product(**product)
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
    uvicorn.run(app, host="0.0.0.0", port=5001)