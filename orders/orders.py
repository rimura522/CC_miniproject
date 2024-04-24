# order_management.py
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
orders_collection = db['orders']

@app.route('/post_order', methods=['POST'])
def post_order():
    data = request.json
    user_name = data.get('user_name')
    product_name = data.get('product_name')
    size = data.get('size')
    quantity = data.get('quantity')
    
    # # Add the user_name and current timestamp to the products collection
    orders_collection.insert_one({'product_name': product_name,'user_name': user_name, 'size': size, 'quantity': quantity, 'timestamp': datetime.now(timezone.utc)})
    return jsonify({'message': 'Order logged successfully'}), 201



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005,debug=True,threaded=True)
