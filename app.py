from flask import Flask, jsonify, request
import requests
import sqlite3
import bcrypt
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
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


# Configuration for JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', '1234')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 # 1 hour
jwt = JWTManager(app)

# Initialize database
init_db()

# Initialize Swagger (only once during app startup)
swagger = init_swagger(app)

@app.route('/')
def home():
    return jsonify({
        "service": "API Gateway"
    })

@app.route('/register', methods=['POST'])
@swag_from('swagger/docs/register.yml')
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
#@swag_from('swagger/docs/gateway.yml')
@jwt_required()
def gateway(service, path):
    if service not in MICROSERVICES:
        return jsonify({"error": "Service not found"}), 404

    # Get the full URL for the microservice
    url = f"{MICROSERVICES[service]}/{path}"

    # Prepare headers
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    # Enforce Content-Type for JSON requests
    if 'Content-Type' not in headers and request.method in ['POST', 'PUT']:
        headers['Content-Type'] = 'application/json'

    # Get the request data
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


# Helper function to forward requests
def forward_request(url):
    try:
        headers = {key: value for key, value in request.headers if key.lower() != 'host'}
        data = request.get_data()
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=data,
            cookies=request.cookies,
            allow_redirects=False
        )
        return (response.content, response.status_code, response.headers.items())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to service: {str(e)}"}), 500

#### FOR SWAGGER ####
# These endpoints are not intended to be used, but was a necessity to make the Swagger UI work

# Create Rental Contract
@app.route('/api/v1/rentals', methods=['POST'])
@swag_from('swagger/docs/create_rental.yml')
def create_rental():
    url = f"{MICROSERVICES['rental_service']}/api/v1/rentals"
    response = forward_request(url)
    return response

# Get All Rentals
@app.route('/api/v1/rentals/all', methods=['GET'])
@swag_from('swagger/docs/get_all_rentals.yml')
def get_all_rentals():
    url = f"{MICROSERVICES['rental_service']}/api/v1/rentals/all"
    response = forward_request(url)
    return response

# Get Rental by ID
@app.route('/api/v1/rentals/<int:rental_id>', methods=['GET'])
@swag_from('swagger/docs/get_rental.yml')
def get_rental_by_id(rental_id):
    url = f"{MICROSERVICES['rental_service']}/api/v1/rentals/{rental_id}"
    response = forward_request(url)
    return response

# Update Rental Contract
@app.route('/api/v1/rentals/<int:rental_id>', methods=['PATCH'])
@swag_from('swagger/docs/update_rental.yml')
def update_rental(rental_id):
    url = f"{MICROSERVICES['rental_service']}/api/v1/rentals/{rental_id}"
    response = forward_request(url)
    return response

# Delete Rental Contract
@app.route('/api/v1/rentals/<int:rental_id>', methods=['DELETE'])
@swag_from('swagger/docs/delete_rental.yml')
def delete_rental(rental_id):
    url = f"{MICROSERVICES['rental_service']}/api/v1/rentals/{rental_id}"
    response = forward_request(url)
    return response

# Get All Cars
@app.route('/api/v1/cars/all', methods=['GET'])
@swag_from('swagger/docs/get_all_cars.yml')
def get_all_cars():
    url = f"{MICROSERVICES['car_management_service']}/all"
    response = forward_request(url)
    return response

# Get Car by ID
@app.route('/api/v1/cars/<int:id>', methods=['GET'])
@swag_from('swagger/docs/get_car_by_id.yml')
def get_car_by_id(id):
    url = f"{MICROSERVICES['car_management_service']}/car/{id}"
    response = forward_request(url)
    return response

# Get Cars by Make
@app.route('/api/v1/cars/make/<int:car_make_id>', methods=['GET'])
@swag_from('swagger/docs/get_cars_by_make_id.yml')
def get_cars_by_make(car_make_id):
    url = f"{MICROSERVICES['car_management_service']}/car/make/{car_make_id}"
    response = forward_request(url)
    return response

# Get Cars by Fuel Type
@app.route('/api/v1/cars/fuel/<int:fuel_type_id>', methods=['GET'])
@swag_from('swagger/docs/get_cars_by_fuel_type.yml')
def get_cars_by_fuel_type(fuel_type_id):
    url = f"{MICROSERVICES['car_management_service']}/car/fuel/{fuel_type_id}"
    response = forward_request(url)
    return response

# Get Cars by Pickup Location
@app.route('/api/v1/cars/location/<int:pickup_location_id>', methods=['GET'])
@swag_from('swagger/docs/get_cars_by_pickup_location_id.yml')
def get_cars_by_pickup_location(pickup_location_id):
    url = f"{MICROSERVICES['car_management_service']}/car/location/{pickup_location_id}"
    response = forward_request(url)
    return response

# Add a New Car
@app.route('/api/v1/cars', methods=['POST'])
@swag_from('swagger/docs/add_new_car.yml')
def add_car():
    url = f"{MICROSERVICES['car_management_service']}/car"
    response = forward_request(url)
    return response

# Delete Car by ID
@app.route('/api/v1/cars/<int:id>', methods=['DELETE'])
@swag_from('swagger/docs/delete_car_by_id.yml')
def delete_car(id):
    url = f"{MICROSERVICES['car_management_service']}/car/{id}"
    response = forward_request(url)
    return response

# Get All Damage Reports
@app.route('/api/v1/damages/all', methods=['GET'])
@swag_from('swagger/docs/get_all_damage_reports.yml')
def get_all_damage_reports():
    url = f"{MICROSERVICES['damage_management_service']}/all"
    response = forward_request(url)
    return response

# Get Damage Report by ID
@app.route('/api/v1/damages/report/<int:report_id>', methods=['GET'])
@swag_from('swagger/docs/get_damage_report_by_id.yml')
def get_damage_report_by_id(report_id):
    url = f"{MICROSERVICES['damage_management_service']}/report/{report_id}"
    response = forward_request(url)
    return response

# Add a New Damage Report
@app.route('/api/v1/damages/report', methods=['POST'])
@swag_from('swagger/docs/add_damage_report.yml')
def add_damage_report():
    url = f"{MICROSERVICES['damage_management_service']}/report"
    response = forward_request(url)
    return response

# Update Damage Report by ID
@app.route('/api/v1/damages/report/<int:report_id>', methods=['PUT'])
@swag_from('swagger/docs/update_damage_report.yml')
def update_damage_report(report_id):
    url = f"{MICROSERVICES['damage_management_service']}/report/{report_id}"
    response = forward_request(url)
    return response

# Delete Damage Report by ID
@app.route('/api/v1/damages/report/<int:report_id>', methods=['DELETE'])
@swag_from('swagger/docs/delete_damage_report.yml')
def delete_damage_report(report_id):
    url = f"{MICROSERVICES['damage_management_service']}/report/{report_id}"
    response = forward_request(url)
    return response

# Get Damage Reports by Car ID
@app.route('/api/v1/damages/report/car/<int:car_id>', methods=['GET'])
@swag_from('swagger/docs/get_damage_reports_by_car_id.yml')
def get_damage_reports_by_car_id(car_id):
    url = f"{MICROSERVICES['damage_management_service']}/report/car/{car_id}"
    response = forward_request(url)
    return response

# Update Pickup Location
@app.route('/api/v1/cars/<int:id>', methods=['PATCH'])
@swag_from('swagger/docs/update_car_location.yml')
def update_car_location(id):
    url = f"{MICROSERVICES['car_management_service']}/car/{id}"
    response = forward_request(url)
    return response

#### END OF SWAGGER ENDPOINTS ####

@app.errorhandler(404)
def not_found(e):
    return jsonify({"Error": "Endpoints not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"Error": "Internal server error"}), 500
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
