import os
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__,template_folder='templates')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            response = requests.post(f'http://auth-service.default.svc.cluster.local:8000/token', data={
                'username': username,
                'password': password
            })
            print(response)
            response.raise_for_status()
            # Handle successful login
            # return redirect(url_for('home'))
            response_data = response.json()
            # Then, you can redirect or render a template with the response data
            return render_template('main.html', response_data=response_data)
        except requests.exceptions.RequestException as e:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            response = requests.post(f'http://auth-service.default.svc.cluster.local:8000/register', json={
                'username': username,
                'password': password
            })
            print(response)
            response.raise_for_status()
            # Handle successful registration
            return redirect(url_for('home'))
        except requests.exceptions.RequestException as e:
            error = 'Registration failed'
            return render_template('register.html', error=error)
    return render_template('register.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)