from flask import Flask, jsonify, request
import requests
import sqlite3
import bcrypt
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from flasgger import swag_from
from swagger.config import init_swagger
from database.initialize import init_db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', '/home/users.db')
MICROSERVICES = {
    "car_management_service": os.getenv("CAR_MANAGEMENT_SERVICE_URL", "https://group-h-car-management-service-fhaeddg8agfddvdu.northeurope-01.azurewebsites.net"),
    "rental_service": os.getenv("RENTAL_SERVICE_URL", "https://group-h-rental-service-emdqb2fjdzh7ddg2.northeurope-01.azurewebsites.net"),
    "damage_management_service": os.getenv("DAMAGE_MANAGEMENT_SERVICE_URL", "https://group-h-damage-management-service-ejh4byctd4hvh9dr.northeurope-01.azurewebsites.net"),
}

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', '1234')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 # 1 hour
jwt = JWTManager(app)

# Initialize database
init_db()

# Initialize Swagger
init_swagger(app, MICROSERVICES)

@app.route('/')
def home():
    return jsonify({
        "service": "API Gateway"
    })

@app.route('/register', methods=['POST'])
@swag_from('swagger/register.yml')
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    username = data['username']
    password = data['password']
    
    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                 (username, hashed))
        connection.commit()
        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f'Username already exists {e}'}), 409
    finally:
        connection.close()

@app.route('/login', methods=['POST'])
@swag_from('swagger/docs/login.yml')
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400
    
    username = data['username']
    password = data['password']
    
    connection = sqlite3.connect(SQLITE_DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    connection.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        access_token = create_access_token(identity=username)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        })
    
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def gateway(service, path):
    if service not in MICROSERVICES:
        return jsonify({"error": "Service not found"}), 404

    # Get the full URL for the microservice
    url = f"{MICROSERVICES[service]}/{path}"
    app.logger.debug(f"Forwarding request to {url}")

    # Prepare headers
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    # Enforce Content-Type for JSON requests
    if 'Content-Type' not in headers and request.method in ['POST', 'PUT']:
        headers['Content-Type'] = 'application/json'

    # Handle body for POST/PUT
    data = None
    if request.method in ['POST', 'PUT']:
        if request.content_type == 'application/json':
            try:
                # Use get_data() to forward raw JSON as is
                data = request.get_data()
            except Exception as e:
                return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400
        else:
            # For non-JSON content types, use raw data
            data = request.get_data()

    # Forward the request
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=data,
            cookies=request.cookies,
            allow_redirects=False
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to {service}: {str(e)}"}), 500

    # Pass response back to the client
    return (response.content, response.status_code, response.headers.items())


@app.errorhandler(404)
def not_found(e):
    return jsonify({"Error": "Endpoints not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"Error": "Internal server error"}), 500
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
