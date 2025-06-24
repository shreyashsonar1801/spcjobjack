from flask import Flask, request, jsonify
from database.config import DATABASE_CONFIG
from Auth.password_manager import PasswordManager
from database.db_operation import DB
import psycopg2

app = Flask(__name__)
pm = PasswordManager()
db = DB(DATABASE_CONFIG)
# Create actual database connection using the config
def get_db_connection():
    return psycopg2.connect(**DATABASE_CONFIG)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required = ['username', 'password', 'first_name', 'last_name', 'email']
    
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = pm.hash_password(data['password'])

    try:
        # Create DB instance with config
        db = DB(DATABASE_CONFIG)

        query = """
            INSERT INTO users (username, user_password, first_name, last_name, email)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data['username'].lower(),
            hashed_password,
            data['first_name'],
            data['last_name'],
            data['email']
        )

        db.execute_non_query(query, values)
        db.close_connection()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400

    try:
        db = DB(DATABASE_CONFIG)

        query = "SELECT user_password FROM users WHERE username = %s"
        values = (data['username'].lower(),)

        result = db.fetch_one(query, values)
        db.close_connection()

        if result and pm.verify_password(data['password'], result[0]):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
