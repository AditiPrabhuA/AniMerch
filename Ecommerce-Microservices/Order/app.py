from flask import Flask, jsonify, request,render_template
# from flask_pymongo import PyMongo
import os
import pymongo.errors

app = Flask(__name__)
MONGO_URI = "mongodb+srv://lippitogapi:TFiItQgsfXbLiiEP@ecommerce-cluster.ke35fsq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('Raptor')

@app.route('/')
def hello():
    return jsonify("Welcome to orders")

@app.route("/check")
def check():
    a = 0
    try:
        db.command('ping')
        print("MongoDB Connection Successful!")
        a = 1
    except pymongo.errors.ConnectionFailure:
        print("MongoDB Connection Failed!")
    return jsonify(a)


@app.route('/orders', methods=['POST'])
def create_order():
    orders = db.orders
    data = request.get_json()
    userid = data.get('userid')
    products = data.get('products')
    
    min_id = 0
    res = orders.find().sort({"orderid":-1}).limit(1)
    for doc in res:
        min_id = int(doc["orderid"])

    order = {
        'orderid': min_id + 1,
        'userid': userid,
        'products': products,
    }
    result = orders.insert_one(order)

    order['_id'] = str(order['_id'])
    print("Order Successfully Added")
    return jsonify(order), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    orders = db.orders
    order = orders.find_one({'orderid': order_id}, {"_id":0})
    if order:
        order['orderid'] = str(order['orderid'])
        return jsonify(order)
    else:
        return jsonify({'error': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)