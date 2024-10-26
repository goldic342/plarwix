# PLARWIX BACKEND

FASTAPI backend for PLARWIX

## Features

- Auth: Auth system with jwt token
- Admin: Admin system, admin can crud user and request, subject, class
- Task: User can create task within class
- Caching: Caching with redis

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or later
- pip

## Installation

Install libraries in **requirements** folder with following command:
    `pip install -r requirements.txt`

## Configuration
You define settings in .env file, for example you have .env.example file

 - Postgresql: db name, username, password, host, port
 - Redis: host, port
 - Admin: login, password
 - JWT: secret key, algorithm, access token expire minutes, refresh token expire days
 - ENVIRONMENT: like dev or test, if test then jwt token will be off

## Running the Application
To start the FastAPI application, run following command in src folder:
    `uvicorn app.main:app --reload`
* The --reload flag enables automatic reload on code changes (useful for development).
Once the server is running, you can access the API at http://127.0.0.1:8000

## API Documentation
FastAPI automatically generates interactive API documentation. You can view it at:
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc