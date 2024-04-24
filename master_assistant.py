 from flask import Flask, request, jsonify, render_template
from flask_restful import Api
import json
import requests
from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from functools import wraps
  
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

client = MongoClient('mongodb://localhost:27017/')

api = Api(app)
# Custom decorator to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_authenticated' not in session:
            return redirect('/login')  # Redirect to login page if not authenticated
        return f(*args, **kwargs)
    return decorated_function

# URL of the users service
USERS_URL = 'http://users:5004'
PRODUCTS_URL = 'http://products:5002'
ORDERS_URL = 'http://orders:5005'

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    response = requests.post(f"{USERS_URL}/add_user", json=data)
    return response.json(), response.status_code

@app.route('/user_order', methods=['POST'])
def user_order():
    data = request.json
    response = requests.post(f"{USERS_URL}/user_order", json=data)
    return response.json()

@app.route('/fetch_user', methods=['GET'])
def fetch_user():
    user_name = request.args.get('user_name')
    password = request.args.get('password')
    response = requests.get(f"{USERS_URL}/fetch_user?user_name={user_name}&password={password}")
    return response.json(), response.status_code

@app.route('/auth_user', methods=['POST'])
def auth_user():
    data = request.json
    response = requests.post(f"{USERS_URL}/auth_user", json=data)
    if response.status_code == 201:
        session['user_authenticated'] = True
    return response.json(), response.status_code

@app.route('/logout', methods=['POST'])
def logout_user():
    response = requests.post(f"{USERS_URL}/logout")
    return response.json(), response.status_code

@app.route('/authed_user', methods=['GET'])
def authed_user():
    response = requests.get(f"{USERS_URL}/authed_user")
    return response.json(), response.status_code

@app.route('/orders')
# @login_required
def orders():
    response = requests.get("http://orders:5005/orders")
    return response.json()

@app.route('/products')
def products():
    response = requests.get("http://products:5002/products")
    return response.json()

@app.route('/login')
def landing_page():
    # if session['user_authenticated'] == True:
    #     return redirect('/home')
    return render_template('landing_page.html')

@app.route('/home')
# @login_required
def home_page():
    return render_template('index.html')

@app.route('/checkout')
# @login_required
def checkout_page():
    return render_template('checkout.html')

@app.route('/clear_current_product', methods=['POST'])
def clear_current_product():
    response = requests.post(f"{PRODUCTS_URL}/clear_current_product")
    return response.json(), response.status_code

@app.route('/post_current_product', methods=['POST'])
def post_current_product():
    data = request.json
    response = requests.post(f"{PRODUCTS_URL}/post_current_product", json=data)
    return response.json(), response.status_code

@app.route('/fetch_current_product', methods=['GET'])
def fetch_current_product():
    response = requests.get(f"{PRODUCTS_URL}/fetch_current_product")
    return response.json(), response.status_code

@app.route('/post_order', methods=['POST'])
def post_order():
    data = request.json
    response = requests.post(f"{ORDERS_URL}/post_order", json=data)
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True,threaded=True)
