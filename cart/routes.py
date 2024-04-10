from flask import Blueprint, jsonify, request
from models import CartItem, mongo

cart_routes = Blueprint('cart_routes', __name__)

@cart_routes.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    cart_items = [CartItem.from_dict(item) for item in mongo.db.cart.find({'user_id': user_id})]
    return jsonify([item.to_dict() for item in cart_items])

@cart_routes.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if user_id and product_id and quantity:
        cart_item = CartItem(user_id, product_id, quantity)
        mongo.db.cart.insert_one(cart_item.to_dict())
        return jsonify({'message': 'Item added to cart'})
    else:
        return jsonify({'error': 'Missing required fields'}), 400

@cart_routes.route('/cart/<user_id>/<product_id>', methods=['PUT'])
def update_cart_item(user_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity')

    if quantity:
        mongo.db.cart.update_one({'user_id': user_id, 'product_id': product_id}, {'$set': {'quantity': quantity}})
        return jsonify({'message': 'Cart item updated'})
    else:
        return jsonify({'error': 'Missing required fields'}), 400

@cart_routes.route('/cart/<user_id>/<product_id>', methods=['DELETE'])
def remove_from_cart(user_id, product_id):
    mongo.db.cart.delete_one({'user_id': user_id, 'product_id': product_id})
    return jsonify({'message': 'Item removed from cart'})