from flask_pymongo import PyMongo

mongo = PyMongo()

class Product:
    def __init__(self, name, description, price, category, image_url):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.image_url = image_url

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url
        }

    @staticmethod
    def from_dict(product_dict):
        return Product(
            name=product_dict['name'],
            description=product_dict['description'],
            price=product_dict['price'],
            category=product_dict['category'],
            image_url=product_dict['image_url']
        )