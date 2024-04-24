from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import bcrypt
import os
import pymongo.errors

app = Flask(__name__)
MONGO_URI = "mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('ecommerce')

#Register User
@app.route("/")
def hello():
    return jsonify("Hello world")

@app.route('/check')
def check():
    a = 0
    try:
        db.command('ping')
        print("MongoDB Connection Successful!")
        a = 1
    except pymongo.errors.ConnectionFailure:
        print("MongoDB Connection Failed!")
    return jsonify(a)

@app.route('/users', methods=['POST'])
def register_user():
    users = db.users
    data = request.get_json()
    #empid = data.get("empid")
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    min_id = 0
    res = users.find().sort({"empid":-1}).limit(1)
    for doc in res:
        min_id = int(doc["empid"])

    user = {
        'empid': min_id+1,
        'username': username,
        'password': hashed_password.decode('utf-8'),
    }
    result = users.insert_one(user)

    user['_id'] = str(user['_id'])
    print("User Successfully Added")
    return jsonify(user), 201

#Get User
@app.route('/users/<int:emp_id>', methods=['GET'])
def get_user(emp_id):
    users = db.users
    user = users.find_one({'empid': emp_id}, {"_id":0})
    if user:
        user['empid'] = str(user['empid'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)