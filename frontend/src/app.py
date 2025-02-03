import os
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__,template_folder='templates')


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/orders")
def test():
    return render_template("test.html")

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
            if username=='admin':
                return redirect(url_for('admin'))
            return redirect(url_for('get_products',userId=res["access_token"]))
        except requests.exceptions.RequestException as e:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    
    return render_template('login.html')
    
@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        action = request.form.get('action')
        pid = request.form.get('pid')
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        url = request.form.get('url')
        try:
            if action=='add':
                response = requests.post(f'http://product-service.default.svc.cluster.local:5001/products', json={
                    'product_id': pid,
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'img_url': url
                })
                response.raise_for_status()
                return redirect(url_for('admin'))
            elif action=='delete':
                response = requests.delete(f'http://product-service.default.svc.cluster.local:5001/products/{pid}')
                response.raise_for_status()
                return redirect(url_for('admin'))
        except requests.exceptions.RequestException as e:
            error = f'Failed to {action} product: {e}'
            return render_template('admin.html', error=error)
    return render_template('admin.html')


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