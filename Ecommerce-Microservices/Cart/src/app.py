from flask import Flask, jsonify, render_template, request
import pymongo.errors
from models import add_to_cart, get_cart, update_cart, remove_from_cart
import os 

app = Flask(__name__)
MONGO_URI = "mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('ecommerce')

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
def add_to_cart_route():
    data = request.get_json()
    user_id = data.get('userid')
    product_id = data.get('productid')
    quantity = data.get('quantity')

    add_to_cart(user_id, product_id, quantity)
    return jsonify({'message': 'Product added to cart'}), 200

# Get the cart for a user
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart_route(user_id):
    cart = get_cart(user_id)
    if cart:
        return jsonify(cart)
    else:
        return jsonify({'error': 'Cart not found'}), 404

# Update the quantity of a product in the cart
@app.route('/cart/<int:user_id>/<product_id>', methods=['PUT'])
def update_cart_route(user_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity')

    update_cart(user_id, product_id, quantity)
    return jsonify({'message': 'Cart updated'}), 200

# Remove a product from the cart
@app.route('/cart/<int:user_id>/<product_id>', methods=['DELETE'])
def remove_from_cart_route(user_id, product_id):
    remove_from_cart(user_id, product_id)
    return jsonify({'message': 'Product removed from cart'}), 200

# Route to render the HTML template
@app.route('/view_cart')
def view_cart():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)
    
