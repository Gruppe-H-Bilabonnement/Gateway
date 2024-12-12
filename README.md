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

| Method | Endpoint                                   | Description                                      |
|--------|-------------------------------------------|--------------------------------------------------|
| POST   | `/register`                               | Register a new user                             |
| POST   | `/login`                                  | Authenticate user and generate JWT token        |
| ANY    | `/<service>/<path>`                       | Forward request to the specified microservice   |

---

## Documentation

### Swagger UI
Interactive API documentation available at: `.../api/v1/docs`

---
