# API Gateway

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

A Flask-based API Gateway that integrates multiple microservices and provides centralized authentication, routing, and documentation.

## Project Overview

The API Gateway Service serves as a central access point for interacting with various microservices, providing features such as user authentication, request forwarding, and detailed Swagger documentation. It is designed to simplify communication between services while ensuring security and scalability.

---

## Key Features

### Technical Highlights
- **Microservice Integration**: Connects with car management, rental, and damage management services.
- **JWT Authentication**: Secure user authentication with JSON Web Tokens.
- **Dynamic Request Forwarding**: Routes requests to appropriate microservices based on user input.
- **Swagger Documentation**: Easy-to-use interactive API documentation.
- **Database for User Management**: SQLite database for storing user credentials.

### Functional Capabilities
- User registration with hashed passwords.
- User login with token generation.
- Proxy requests to microservices with proper authentication.
- Flexible error handling and standard JSON responses.

---

## Architectural Design

### System Components

1. **Web Framework**: Flask
   - Provides routing and request handling.

2. **Database**: SQLite
   - Stores user credentials securely.

3. **Authentication**: Flask-JWT-Extended
   - Implements secure token-based authentication.

4. **Request Forwarding**: Requests Library
   - Routes client requests to appropriate microservices.

5. **Documentation**: Flasgger
   - Provides Swagger/OpenAPI documentation for the API.

---

## 📂 Project Structure
```
api-gateway-service/
│
├── app.py                   # Main application entry point
├── database/
│   └── initialize.py        # Database setup and initialization
│
├── swagger/
│   ├── config.py            # Swagger configuration
│   └── docs/                # Swagger documentation specs
│
└── .env                     # Environment variables
```

## API Endpoints

### Base URL: `/api/v1`

| Method | Endpoint                                       | Description                              | Microservice              |
|--------|-----------------------------------------------|------------------------------------------|---------------------------|
| POST   | /api/v1/auth/login                            | User Login                               | gateway                   |
| POST   | /api/v1/auth/register                         | User Registration                        | gateway                   |
| POST   | /api/v1/rentals                               | Create Rental Contract (JWT Required)    | rental_service            |
| GET    | /api/v1/rentals/all                           | Get All Rentals                          | rental_service            |
| GET    | /api/v1/rentals/<int:rental_id>               | Get Rental by ID                         | rental_service            |
| PATCH  | /api/v1/rentals/<int:rental_id>               | Update Rental Contract (JWT Required)    | rental_service            |
| DELETE | /api/v1/rentals/<int:rental_id>               | Delete Rental Contract (JWT Required)    | rental_service            |
| GET    | /api/v1/cars/all                              | Get All Cars                             | car_management_service    |
| GET    | /api/v1/cars/<int:id>                         | Get Car by ID                            | car_management_service    |
| GET    | /api/v1/cars/make/<int:car_make_id>           | Get Cars by Make                         | car_management_service    |
| GET    | /api/v1/cars/fuel/<int:fuel_type_id>          | Get Cars by Fuel Type                    | car_management_service    |
| GET    | /api/v1/cars/location/<int:pickup_location_id>| Get Cars by Pickup Location              | car_management_service    |
| POST   | /api/v1/cars                                  | Add a New Car (JWT Required)             | car_management_service    |
| DELETE | /api/v1/cars/<int:id>                         | Delete Car by ID (JWT Required)          | car_management_service    |
| PATCH  | /api/v1/cars/<int:id>                         | Update Pickup Location (JWT Required)    | car_management_service    |
| GET    | /api/v1/damages/all                           | Get All Damage Reports                   | damage_management_service |
| GET    | /api/v1/damages/report/<int:report_id>        | Get Damage Report by ID                  | damage_management_service |
| POST   | /api/v1/damages/report                        | Add a New Damage Report (JWT Required)   | damage_management_service |
| PUT    | /api/v1/damages/report/<int:report_id>        | Update Damage Report by ID (JWT Required)| damage_management_service |
| DELETE | /api/v1/damages/report/<int:report_id>        | Delete Damage Report by ID (JWT Required)| damage_management_service |
| GET    | /api/v1/damages/report/car/<int:car_id>       | Get Damage Reports by Car ID             | damage_management_service |

---

## Documentation

### Swagger UI
Interactive API documentation available at: `https://group-h-api-gateway-h9g7egage5a7dmd8.northeurope-01.azurewebsites.net/api/v1/docs`

---
