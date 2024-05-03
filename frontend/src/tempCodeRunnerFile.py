@app.route('/cart/<userId>', methods=['POST'])
# def add_to_cart(userId):
#     item = request.form
#     response = requests.post(f"{FASTAPI_SERVICE_URL}/cart/{userId}", json=item)
#     return redirect(url_for('get_cart', userId=userId)