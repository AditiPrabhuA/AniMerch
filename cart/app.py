from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)
CORS(app)

# Import routes
from routes import cart_routes

app.register_blueprint(cart_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)