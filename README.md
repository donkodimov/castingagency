# Casting Agency API

This project is a web application that allows users to view and manage data for a casting agency, including actors and movies. The application has a Python API backend and a basic frontend with functionality for logging in, logging out, and calling three API endpoints.

Features:

* View a list of actors and movies
* Add new actors and movies
* Update existing actors and movies
* Delete actors and movies
* Assign actors to movies

Endpoints:

* GET /actors: returns a list of all actors
* GET /actors/<actor_id>: returns a list of all actors
* POST /actors: creates a new actor
* PATCH /actors/<actor_id>: updates an existing actor
* DELETE /actors/<actor_id>: deletes an existing actor
* GET /movies: returns a list of all movies
* POST /movies: creates a new movie
* PATCH /movies/<movie_id>: updates an existing movie
* DELETE /movies/<movie_id>: deletes an existing movie
* POST /performance: assigns an actor to a movie
* DELETE /performance: removes an actor from a movie

Frontend Functionality

The frontend of the application has the following functionality:

1. Login: users can log in to the application using their credentials.
2. Logout: users can log out of the application.
3. View actors and movies: users can view a list of actors or movies and their details by calling the appropriate API endpoint.

Authentication with Auth0 and RBAC

1. Sign up for a free account on the Auth0 website (https://auth0.com/).
2. Create a new application in your Auth0 dashboard. You will need to choose a name for your application and select the "Single Page Web Applications" option.
3. Configure the application settings. In the "Allowed Callback URLs" field, enter the URL of your application where users will be redirected after logging in. You should also specify any other URLs that will be used as part of the authentication process, such as the URL for logging out.
4. In the application settings, enable the "RBAC" toggle. This will enable role-based access control for the application.
5. In the "Roles" tab, create any roles that you want to use in your application. For example, you might create a "Producer" role for users with administrative privileges, a "Director" role for regular users and an "Assitant" role for restricted access only.
6. In the "Users" tab, create any users that you want to use in your application. Assign each user the appropriate role(s).
7. You will also need to implement the login and logout functionality, and protect any routes or resources that should only be accessible to authenticated users. Change the login and logout link in the index.html with your AUTH0_DOMAIN, Allowed Callback URL(redirect_uri for login button), Allowed Logout URL(redirect_uri for logout button), audience, client_id.


Once you have completed these steps, your application will be able to authenticate users using the Auth0 platform. Users will be able to log in using the login flow you have configured, and your application will be able to validate their JWTs to ensure that they are authenticated.

## Geting started
### Installing Dependancies

#### Python 3.10
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
With Postgres running, create empty database and restore a database using the castingagency.psql file provided. From the backend folder in terminal run:

```bash
createdb castingagency
psql trivia < castingagency.psql
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
The API will return these error types when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error

## Endpoints

### Get all movies

#### Request

`GET /movies`
```bash
    curl http://127.0.0.1:5000/movies
```

#### Success Response:

* Code: 200
* Content:

```json
{
    "success": true,
    "movie_details": [
        {
            "actors": [
                {
                    "actor_id": 1,
                    "actor_name": "John Doe",
                    "actor_age": 30,
                    "actor_gender": "Male"
                },
                {
                    "actor_id": 2,
                    "actor_name": "Jane Doe",
                    "actor_age": 25,
                    "actor_gender": "Female"
                }
            ],
            "movie_id": 1,
            "movie_title": "Movie 1",
            "movie_release_date": "January 01 2020 00:00:00"
        },
        {
            "actors": [
                {
                    "actor_id": 3,
                    "actor_name": "Bob Smith",
                    "actor_age": 35,
                    "actor_gender": "Male"
                }
            ],
            "movie_id": 2,
            "movie_title": "Movie 2",
            "movie_release_date": "February 01 2020 00:00:00"
        }
    ],
    "total actors": 2
}
```

#### Error Response:

* Code: 404
* Content:

```json
{
    "error": 404,
    "success": false,
    "message": "No records were found"
}
```


### Get one movies

#### Request

`GET /movies/<movie_id>`
```bash
    curl http://127.0.0.1:5000/movies/<movie_id>
```

#### Success Response:

* Code: 200
* Content:

```json
{
    "success": true,
    "id": 5,
    "title": "Jurasic Park"
}
```

#### Error Response:

* Code: 400
* Content:

```json
{
    "error": 400,
    "success": false,
    "message": "Bad request"
}
```

### Edit movie

#### Request

`POST /movies/create`
```bash
  curl -X POST \
    http://localhost:5000/movies/create \
    -H 'Authorization: Bearer <YOUR_JWT>' \
    -H 'Content-Type: application/json' \
    -d '{
	    "title": "Movie 1",
	    "release_date": "2020-01-01"
    }'
```


#### Success Response:

* Code: 200
* Content:

```json
{
    "success": true,
    "id": 5,
    "title": "Jurasic Park"
}
```

#### Error Response:

* Code: 400
* Content:

```json
{
    "error": 400,
    "success": false,
    "message": "Bad request"
}
```

* Code: 500
* Content:

```json
{
    "error": 500,
    "success": false,
    "message": "Internal Server Error"
}
```

### Delete movie

#### Request

`DELETE /movies/<movie_id>`
```bash
  curl -X DELETE \
    http://localhost:5000/movies/<movie_id> \
    -H 'Authorization: Bearer <YOUR_JWT>'
```


#### Success Response:

* Code: 200
* Content:

```json
{
    "success": true,
    "movie": 5
}
```

#### Error Response:

* Code: 404
* Content:

```json
{
    "error": 404,
    "success": false,
    "message": "No records were found"
}
```

### Update movie

#### Request

`PATCH /movies/<movie_id>`
```bash
  curl -X PATCH \
    http://localhost:5000/movies/<movie_id> \
    -H 'Authorization: Bearer <YOUR_JWT>' \
    -H 'Content-Type: application/json' \
    -d '{
        "title": "Water7"
        }'
```


#### Success Response:

* Code: 200
* Content:

```json
{
    "success": true,
    "movie": "New Movie name",
    "release_date": "2022-09-09"
}
```

#### Error Response:

* Code: 400
* Content:

```json
{
    "error": 400,
    "success": false,
    "message": "Bad request"
}
```

* Code: 500
* Content:

```json
{
    "error": 500,
    "success": false,
    "message": "Internal Server Error"
}
```