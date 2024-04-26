from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import os

app = Flask(__name__,template_folder='templates')

FASTAPI_SERVICE_URL = "http://localhost:8000"

@app.route('/cart/<userId>', methods=['GET'])
def get_cart(userId):
    response = requests.get(f"{FASTAPI_SERVICE_URL}/cart/{userId}")
    cart = response.json()
    return render_template('cart.html', cart=cart)

@app.route('/cart/<userId>', methods=['POST'])
def add_to_cart(userId):
    item = request.form
    response = requests.post(f"{FASTAPI_SERVICE_URL}/cart/{userId}", json=item)
    return redirect(url_for('get_cart', userId=userId))

@app.route('/cart/<userId>/item/<int:product_id>', methods=['PUT'])
def update_cart_item(userId, product_id):
    item = request.form
    response = requests.put(f"{FASTAPI_SERVICE_URL}/cart/{userId}/item/{product_id}", json=item)
    return redirect(url_for('get_cart', userId=userId))

@app.route('/cart/<userId>/item/<int:product_id>', methods=['DELETE'])
def delete_cart_item(userId, product_id):
    response = requests.delete(f"{FASTAPI_SERVICE_URL}/cart/{userId}/item/{product_id}")
    return redirect(url_for('get_cart', userId=userId))

@app.route('/cart/<userId>/total', methods=['GET'])
def calculate_total(userId):
    response = requests.get(f"{FASTAPI_SERVICE_URL}/cart/{userId}/total")
    total = response.json()['total']
    return render_template('total.html', total=total)

if __name__ == "__main__":
    app.run(debug=True)
