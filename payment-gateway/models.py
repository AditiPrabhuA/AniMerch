from flask_pymongo import PyMongo

mongo = PyMongo()

class Payment:
    def __init__(self, user_id, order_id, total_amount, payment_method):
        self.user_id = user_id
        self.order_id = order_id
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.status = 'pending'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'order_id': self.order_id,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'status': self.status
        }

    @staticmethod
    def from_dict(payment_dict):
        return Payment(
            user_id=payment_dict['user_id'],
            order_id=payment_dict['order_id'],
            total_amount=payment_dict['total_amount'],
            payment_method=payment_dict['payment_method']
        )