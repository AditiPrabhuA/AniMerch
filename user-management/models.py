from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

mongo = PyMongo()

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

    @staticmethod
    def from_dict(user_dict):
        return User(
            username=user_dict['username'],
            email=user_dict['email'],
            password=user_dict['password']
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)