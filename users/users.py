# user management
from flask import Flask
from flask import Flask, request
from flask import jsonify
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('mongodb')
db = client['ecommerce']
users_collection = db['users']
logged_in_collection = db['logged_in']

@app.route("/add_user", methods=['POST'])
def add_user():
    data = request.json
    user_name = data.get('user_name')
    age = data.get('age')
    country = data.get('country')
    gender = data.get('gender')
    password = data.get('password')
    new_user = {
        'user_name': user_name,
        'age': age,
        'country': country,
        'gender': gender,
        'orders': [],  # Initialize orders as an empty list
        'password': password
    }
    if (users_collection.find_one({'user_name': user_name})):
        return jsonify({'message': f'Failed to add user'}), 400
    else:
        users_collection.insert_one(new_user)
        return jsonify({'message': f'User {user_name} added successfully'}), 201
        

@app.route("/user_order", methods=['POST'])
def user_order():
    data = request.json
    user_name = data.get('user_name')
    order_id = data.get('order_id')
    users_collection.update_one({'user_name': user_name}, {'$push': {'orders': order_id}})
    return jsonify({'message': f'Order {order_id} added to user {user_name} successfully'})

@app.route("/fetch_user", methods=['GET'])
def fetch_user():
    user_name = request.args.get('user_name')
    password = request.args.get('password')
    user = users_collection.find_one({'user_name': user_name})
    if user:
        if user.get('password') == password:
            return jsonify("Congrats" + str(user)), 201
        else:
             return jsonify({'message': 'Password wrong'}), 400
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/auth_user', methods=['POST'])
def auth_user():
    data = request.json
    user_name = data.get('user_name')
    # Clear the existing records
    logged_in_collection.delete_many({})
    
    # # Add the user_name and current timestamp to the logged_in collection
    logged_in_collection.insert_one({'user_name': user_name, 'timestamp': datetime.now(timezone.utc)})
    return jsonify({'message': 'User authenticated successfully', 'timestamp': datetime.now(timezone.utc)}), 201

@app.route('/authed_user', methods=['GET'])
def authed_user():
    # Fetch the logged in user and its timestamp
    logged_in_user = logged_in_collection.find_one()
    if logged_in_user:
        # # Get the timestamp and calculate the difference in minutes
        # timestamp = logged_in_user.get('timestamp')
        # current_time = datetime.now(timezone.utc)
        # print(current_time)
        # time_difference = current_time - timestamp
        # minutes_difference = time_difference.total_seconds() / 60
        
        # # Check if the session is expired (more than 20 minutes)
        # if minutes_difference > 20:
        #     logged_in_collection.delete_many({})
        #     return jsonify({'message': 'Session expired'})
        
        # If not expired, return the logged in user
        return jsonify({'user_name': logged_in_user.get('user_name')}), 201
    else:
        return jsonify({'message': 'No user logged in'}), 400

@app.route('/logout', methods=['POST'])
def logout_user():
    logged_in_collection.delete_many({})
    return jsonify("Logged Out!"), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
