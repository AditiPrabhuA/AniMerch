from flask import Flask, jsonify, render_template, request
import pymongo.errors
import os 

app = Flask(__name__)
MONGO_URI = "mongodb+srv://lippitogapi:TFiItQgsfXbLiiEP@ecommerce-cluster.ke35fsq.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('Raptor')

@app.route("/")
def hello():
    return jsonify("Welcome to cart")

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

# Add a product to the cart
@app.route('/cart', methods=['POST'])
def add_product():
    products = db.products
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')
    user_id = data.get('userId') 

    product = {
        'name': name,
        'quantity': quantity,
        'price': price,
    }
    products.insert_one(product)

    product['_id'] = str(product['_id'])
    return jsonify(product), 201

# Update a product in the cart
@app.route('/cart/<product_id>', methods=['PUT'])
def update_product(product_id):
    products = db.products
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')
    
    query = {'_id': product_id}
    update = {'$set': {'name': name, 'quantity': quantity, 'price': price}}

    result = products.update_one(query, update)

    if result.modified_count == 1:
        return jsonify({'message': 'Product updated'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

# Remove a product from the cart
@app.route('/cart/<product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = db.products
    result = products.delete_one({'_id': product_id})

    if result.deleted_count == 1:
        return jsonify({'message': 'Product removed'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

# Get all products in the cart
@app.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('userId')
    products = db.products
    cursor = products.find({})
    cart = []
    for product in cursor:
        product['_id'] = str(product['_id'])
        cart.append(product)
    return jsonify(cart), 200

# Route to render the HTML template
@app.route('/view_cart')
def view_cart():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)
    
