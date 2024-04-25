from flask import Flask, jsonify, render_template, request
import pymongo.errors

app = Flask(__name__)
MONGO_URI = "mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.ecommerce

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
def add_to_cart():
    carts = db.carts
    data = request.get_json()
    userid = data.get('userid')
    productsa = data.get('products')
    print(productsa)
    product_name = productsa[0].get('name')
    quantity = productsa[0].get('quantity')
    productid = productsa[0].get('productid')
    print(product_name)
    # Fetch the product details from the products collection
    products = db.products
    product = products.find_one({'name': product_name})

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Check if the user has an existing cart
    cart = carts.find_one({'userid': userid})

    if not cart:
        # Create a new cart for the user
        cart = {
            'userid': userid,
            'products': [
                {
                    'name': product["name"],
                    'quantity': quantity
                }
            ]
        }
        carts.insert_one(cart)
    else:
        # Add the product to the existing cart
        existing_product = next((p for p in cart['products'] if p['name'] == product_name), None)
        if existing_product:
            existing_product['quantity'] += quantity
        else:
            cart['products'].append({
                'name': product['name'],
                'quantity': quantity
            })
        carts.update_one({'userid': userid}, {'$set': {'products': cart['products']}})

    return jsonify({'message': 'Product added to cart'}), 200

# Get the cart for a user
@app.route('/cart/<int:userid>', methods=['GET'])
def get_cart(userid):
    carts = db.carts
    cart = carts.find_one({'userid': userid}, {'_id': 0})
    if cart:
        return jsonify(cart)
    else:
        return jsonify({'error': 'Cart not found'}), 404

# Remove a product from the cart
@app.route('/cart/<int:userid>/<int:productid>', methods=['DELETE'])
def remove_from_cart(userid, productid):
    carts = db.carts

    cart = carts.find_one({'userid': userid})
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404

    cart['products'] = [p for p in cart['products'] if p['productid'] != productid]

    if not cart['products']:
        # If the cart is empty, remove the cart document
        carts.delete_one({'userid': userid})
    else:
        carts.update_one({'userid': userid}, {'$set': {'products': cart['products']}})

    return jsonify({'message': 'Product removed from cart'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)