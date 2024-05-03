import os
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__,template_folder='templates')


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/test")
def test():
    return render_template("test.html")

@app.route('/allproducts', methods=['GET', 'POST'])
def addproducts():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        try:
            response = requests.post(f'http://product-service.default.svc.cluster.local:5001/products', json={
                'name': name,
                'price': price
            })
            print(response)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            error = 'product not added'
            return render_template('products.html', error=error)
    
    return render_template('products.html')

LOGIN_K = "http://auth-service.default.svc.cluster.local:8000/token"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    
        username = request.form['username']
        password = request.form['password']
        try:
            response = requests.post(f'http://auth-service.default.svc.cluster.local:8000/login', data={
                'username': username,
                'password': password
            })
            print(response)
            response.raise_for_status()
            res = response.json()
            return redirect(url_for('get_products',userId=res["access_token"]))
        except requests.exceptions.RequestException as e:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

REG_K = "http://auth-service.default.svc.cluster.local:8000/register"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        username = request.form['username']
        password = request.form['password']
        try:
            response = requests.post(f'http://auth-service.default.svc.cluster.local:8000/register', json={
                'name': name,
                'age': age,
                'gender': gender,
                'username': username,
                'password': password
            })
            print(response)
            response.raise_for_status()
            return redirect(url_for('login'))
        except requests.exceptions.RequestException as e:
            error = 'Registration failed'
            return render_template('register.html', error=error)
    return render_template('register.html')

FASTAPI_SERVICE_URL = "http://localhost:8000"

@app.route('/cart/<userId>', methods=['GET'])
def get_cart(userId):
    try:
        response = requests.get(f"http://cartapp-svc.default.svc.cluster.local:5004/cart/{userId}")
        ct = requests.get(f"http://cartapp-svc.default.svc.cluster.local:5004/cart/{userId}/total").json()
        cart = response.json()
        return render_template('cart.html', response_data = cart,userc=userId, cart_total=ct['total'])
    except requests.exceptions.HTTPError as e:
        cart_total = 0
        response_data = {}
        error = 'Empty Cart or Cart not found'
        return render_template('cart.html',userc = userId,cart_total=cart_total,error = error)

@app.route('/getproducts/<userId>', methods=['GET'])
def get_products(userId):
    response = requests.get(f"http://product-service.default.svc.cluster.local:5001/products")
    return render_template('dispproducts.html', response_data = response.json(),user=userId)

@app.route('/cart/<userId>/item/<int:product_id>', methods=['PUT'])
def update_cart_item(userId, product_id):
    item = request.form
    response = requests.put(f"http://cartapp-svc.default.svc.cluster.local:5004/cart/{userId}/item/{product_id}", json=item)
    return redirect(url_for('get_cart', userId=userId))

@app.route('/cart/<userId>/item/<int:product_id>', methods=['DELETE'])
def delete_cart_item(userId, product_id):
    response = requests.delete(f"http://cartapp-svc.default.svc.cluster.local:5004/cart/{userId}/item/{product_id}")
    return redirect(url_for('get_cart', userId=userId))

@app.route('/cart/<userId>/total', methods=['GET'])
def calculate_total(userId):
    response = requests.get(f"http://cartapp-svc.default.svc.cluster.local:5004/cart/{userId}/total")
    total = response.json()['total']
    return render_template('total.html', total=total)

@app.route('/orders/<userId>', methods=['GET'])
def get_orders(userId):
    try:
        response = requests.get(f"http://cartapp-svc.default.svc.cluster.local:5004/orders/{userId}")
        orders = response.json()
        return render_template('orders.html', orders=orders, userc=userId)
    except requests.exceptions.RequestException as e:
        orders = []
        error = 'Failed to retrieve orders'
        return render_template('orders.html', orders=orders, userc=userId, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)