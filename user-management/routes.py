from flask import Blueprint, jsonify, request, render_template
from models import User, mongo

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def homepage():
    return render_template('index.html')

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if username and email and password:
        user = User(username, email, password)
        mongo.db.users.insert_one(user.to_dict())
        return jsonify({'message': 'User registered successfully'})
    else:
        return jsonify({'error': 'Missing required fields'}), 400

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email and password:
        user = mongo.db.users.find_one({'email': email})
        if user:
            user_obj = User.from_dict(user)
            if user_obj.check_password(password):
                return jsonify({'message': 'Login successful'})
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'Missing required fields'}), 400