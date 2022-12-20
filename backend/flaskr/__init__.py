import os, sys
from flask import Flask, request, abort, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from models import setup_db, Movie, Actor, db, drop_and_init_db




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    drop_and_init_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


    @app.route("/")
    def index():
        return redirect(url_for('get_movie', movie_id=1))
       

#  Movies
#  ----------------------------------------------------------------


    @app.route("/movies/<movie_id>")
    def get_movie(movie_id):

        movie = Movie.query.get(movie_id)

        return render_template('index.html',
            movies=Movie.query.order_by('id').all(),
            active_movie=Movie.query.get(movie_id),
            actors=Actor.query.order_by('id').all()
            )


    @app.route("/movies/create", methods=['POST'])
    def create_movies():
        error = False
        body = {}
        try:
            title = request.get_json()['title']
            release_date = request.get_json()['release_date']
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            body['id'] = movie.id
            body['title'] = movie.title

        except ValueError as e:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            abort(500)
        else:
            return jsonify(body)
   

    @app.route("/movies/<movie_id>", methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            movie.delete()
            return jsonify({
                "success": True,
                "movie": movie_id})


    @app.route("/movies/<movie_id>", methods=['PATCH'])
    def patch_movie(movie_id):

        body = request.get_json()
        new_title = body.get("title", None)
        movie = Movie.query.filter(Movie.id == movie_id).first_or_404()

        try:
            if new_title:
                movie.title = new_title
            movie.update()
        
        except Exception as e:
            print(e)
            abort(422)
    
        return jsonify({
            "success": True,
            "movie": movie.title
        }), 200


#  Actors
#  ----------------------------------------------------------------


    @app.route("/actors/<actor_id>")
    def get_actor(actor_id):

        actor = Actor.query.get(actor_id)

        return jsonify({
                "success": True,
                "id": actor.id,
                "actor": actor.name
            }), 200


    @app.route("/actors/create", methods=['POST'])
    def create_actor():
        error = False
        body = {}
        try:
            name = request.get_json()['name']
            age = request.get_json()['age']
            gender = request.get_json()['gender']
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            body['id'] = actor.id
            body['name'] = actor.name
            print(body)

        except ValueError as e:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            abort(500)
        else:
            return jsonify(body)


    @app.route("/actors/<actor_id>", methods=['DELETE'])
    def delete_actor(actor_id):

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        else:
            actor.delete()
            return jsonify({
                "success": True,
                "actor": actor_id
            }), 200

    
    @app.route("/actors/<actor_id>", methods=['PATCH'])
    def patch_actor(actor_id):

        body = request.get_json()
        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)
        actor = Actor.query.filter(Actor.id == actor_id).first_or_404()

        try:
            if new_name:
                actor.name = new_name
            if new_age:
                actor.age = new_age
            if new_gender:
                actor.gender = new_gender
            actor.update()
        
        except Exception as e:
            print(e)
            abort(422)
    
        return jsonify({
            "success": True,
            "name": actor.name,
            "age": actor.age,
            "gender": actor.gender
        }), 200


    return app

    