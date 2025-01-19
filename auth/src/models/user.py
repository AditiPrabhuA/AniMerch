# models/user.py
from mongoengine import Document, StringField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

    meta = {
        'db_alias': 'ecommerce',  # Specify the database alias
        'collection': 'users'  # Specify the collection name
    }