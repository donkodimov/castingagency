# Casting agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

The app provides basic frontend. For extended access API endpoints can be used to add, update and delete items.

## Geting started
### Installing Dependancies

#### Python 3.x
Follow instructions to install the latest version of python for your platform in the python docs

#### Virtual Enviornment
Working within a virtual environment is recommended.
```bash
python3 -m venv venv
source venv/bin/activate
```

#### PIP Dependencies
Navigate to the root directory and run:

```bash
pip install -r requirements.txt
```
This will install all of the required packages in the requirements.txt file.

#### Key Dependencies
* Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

* SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

* Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```
### Running the server
From within the backend directory

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing

# API Reference

## Getting Started

* Backend Base URL: ```http://127.0.0.1:5000/```

### Authentication

There are 3 type of accounts based on the actions a user can perform:

* Casting Assitant ( can GET requests)
* Casting Director ( can GET, POST, PATCH requests)
* Managing Director ( can GET, POST, PATCH, DELETE requests)

### Error Handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 404,
    "message": "Resource Not Found"
}
```
The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

## Endpoints

### Get all movies

#### Request

`GET /movies``

    curl http://127.0.0.1:5000/movies

#### Response

```json
{
    "movies": {
        ...
    }
}
```