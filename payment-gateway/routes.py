from flask import Blueprint, jsonify, request
from models import Payment, mongo

payment_routes = Blueprint('payment_routes', __name__)

@payment_routes.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    user_id = data.get('user_id')
    order_id = data.get('order_id')
    total_amount = data.get('total_amount')
    payment_method = data.get('payment_method')

    if user_id and order_id and total_amount and payment_method:
        payment = Payment(user_id, order_id, total_amount, payment_method)
        mongo.db.payments.insert_one(payment.to_dict())
        return jsonify({'message': 'Payment processed successfully'})
    else:
        return jsonify({'error': 'Missing required fields'}), 400

@payment_routes.route('/payment_status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    payment = mongo.db.payments.find_one({'_id': payment_id})
    if payment:
        payment_obj = Payment.from_dict(payment)
        return jsonify({'status': payment_obj.status})
    else:
        return jsonify({'error': 'Payment not found'}), 404