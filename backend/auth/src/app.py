from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
import uvicorn

app = FastAPI()

client = MongoClient("{mongodb_cluster_uri}")
db = client["ecommerce"]
users_collection = db["users"]


class UserData(BaseModel):
    name: str
    age: int
    gender: str
    username: str
    password: str

@app.post("/register")
async def register(user_data: UserData):
    existing_user = users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_collection.insert_one(user_data.dict())
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username, "password": form_data.password})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user["username"], "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)