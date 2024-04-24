import pymongo
from schemas import cart_schema
from bson.objectid import ObjectId

MONGO_URI = "mongodb+srv://arevanthsreeram:Dg4eP6YcuClsxTf9@cluster0.lgmqzy1.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('ecommerce')

def add_to_cart(user_id, product_id, quantity):
    carts = db.carts
    products = db.products

    # Fetch the product details from the products collection
    product = products.find_one({'_id': ObjectId(product_id)})

    if not product:
        return {'error': 'Product not found'}

    # Check if the user has an existing cart
    cart = carts.find_one({'userid': user_id})

    if not cart:
        # Create a new cart for the user
        cart = {
            'userid': user_id,
            'products': [
                {
                    'productid': str(product['_id']),
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': quantity
                }
            ]
        }
        carts.insert_one(cart)
    else:
        # Add the product to the existing cart
        existing_product = next((p for p in cart['products'] if p['productid'] == str(product['_id'])), None)
        if existing_product:
            existing_product['quantity'] += quantity
        else:
            cart['products'].append({
                'productid': str(product['_id']),
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            })
        carts.update_one({'userid': user_id}, {'$set': {'products': cart['products']}})

    return {'message': 'Product added to cart'}

def get_cart(user_id):
    carts = db.carts
    cart = carts.find_one({'userid': user_id}, {'_id': 0})
    return cart

def update_cart(user_id, product_id, quantity):
    carts = db.carts

    cart = carts.find_one({'userid': user_id})
    if not cart:
        return {'error': 'Cart not found'}

    product_found = False
    for product in cart['products']:
        if product['productid'] == product_id:
            product['quantity'] = quantity
            product_found = True
            break

    if not product_found:
        return {'error': 'Product not found in cart'}

    carts.update_one({'userid': user_id}, {'$set': {'products': cart['products']}})
    return {'message': 'Cart updated'}

def remove_from_cart(user_id, product_id):
    carts = db.carts

    cart = carts.find_one({'userid': user_id})
    if not cart:
        return {'error': 'Cart not found'}

    cart['products'] = [p for p in cart['products'] if p['productid'] != product_id]

    if not cart['products']:
        # If the cart is empty, remove the cart document
        carts.delete_one({'userid': user_id})
    else:
        carts.update_one({'userid': user_id}, {'$set': {'products': cart['products']}})

    return {'message': 'Product removed from cart'}