# product_management.py
from flask import Flask
from flask import Flask, request
from flask_restful import Api
from flask import jsonify
import json
import requests
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb')
db = client['ecommerce']
products_collection = db['products']

@app.route('/post_current_product', methods=['POST'])
def post_current_product():
    data = request.json
    product_name = data.get('product_name')
    # Clear the existing records
    products_collection.delete_many({})
    
    # Add the user_name and current timestamp to the products collection
    if products_collection.insert_one({'product_name': product_name, 'timestamp': datetime.now(timezone.utc)}):
        return jsonify({'message': 'Product posted successfully', 'timestamp': datetime.now(timezone.utc)}), 201
    
    return jsonify({'message': 'Product not posted'}), 400

@app.route('/clear_current_product', methods=['POST'])
def clear_current_product():
    # Clear the existing records
    products_collection.delete_many({})
    
    # # Add the user_name and current timestamp to the products collection
    return jsonify({'message': 'Product cleared successfully', 'timestamp': datetime.now(timezone.utc)}), 201

@app.route('/fetch_current_product', methods=['GET'])
def fetch_current_product():
    # Fetch the logged in user and its timestamp
    current_products = products_collection.find_one()
    if current_products:
        return jsonify({'product_name': current_products.get('product_name')}), 201
    else:
        return jsonify({'message': 'No products currently in use'}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002,debug=True,threaded=True)