from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
from multipart import MultipartParser

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["ecommerce"]
users_collection = db["users"]

# User data model
class UserData(BaseModel):
    username: str
    password: str

# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register")
async def register(user_data: UserData):
    existing_user = users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    users_collection.insert_one(user_data.dict())
    return {"message": "User registered successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username, "password": form_data.password})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user["username"], "token_type": "bearer"}