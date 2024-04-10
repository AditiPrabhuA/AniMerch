from flask_pymongo import PyMongo

mongo = PyMongo()

class CartItem:
    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

    @staticmethod
    def from_dict(cart_item_dict):
        return CartItem(
            user_id=cart_item_dict['user_id'],
            product_id=cart_item_dict['product_id'],
            quantity=cart_item_dict['quantity']
        )