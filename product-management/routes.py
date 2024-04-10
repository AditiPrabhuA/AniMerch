from flask import Blueprint, jsonify, request
from models import Product, mongo

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products', methods=['GET'])
def get_products():
    products = [Product.from_dict(product) for product in mongo.db.products.find()]
    return jsonify([product.to_dict() for product in products])

@product_routes.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = mongo.db.products.find_one({'_id': product_id})
    if product:
        product_obj = Product.from_dict(product)
        return jsonify(product_obj.to_dict())
    else:
        return jsonify({'error': 'Product not found'}), 404

@product_routes.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category = data.get('category')
    image_url = data.get('image_url')

    if name and description and price and category and image_url:
        product = Product(name, description, price, category, image_url)
        mongo.db.products.insert_one(product.to_dict())
        return jsonify({'message': 'Product created successfully'})
    else:
        return jsonify({'error': 'Missing required fields'}), 400