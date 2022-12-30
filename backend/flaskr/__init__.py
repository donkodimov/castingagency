import os, sys
from flask import Flask, request, abort, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DataError, IntegrityError
from flask_cors import CORS, cross_origin
from functools import wraps

from models import setup_db, Movie, Actor, Performance, db, drop_and_init_db
from auth import *




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


    @app.route("/movies")
    @requires_auth('get:movies')
    def get_movies(payload):

        
        movies_info = []
        try:
            movies = db.session.query(Movie).all()
            if len(movies) == 0:
                return jsonify({
                    'success': False,
                    'message': 'No records were found'
                }), 404
            
            else:
                for movie in movies:
                    
                    #actors = Actor.query.filter(Movie.id == movie.id)
                                    
                    movies_info.append({
                        'actors:': [
                            {
                                "actor_id": x.id,
                                "actor_name": x.name,
                                "actor_age": x.age,
                                "actor_gender": x.gender
                            }
                            for x in movie.actor
                        ],
                        'movie_id': movie.id,
                        'movie_title': movie.title,
                        'movie_release_date': movie.release_date.strftime("%B %d %Y %H:%M:%S")
                    })

            return jsonify({
                "success": True,
                "movie_details": movies_info,
                "total actors": len(movies)
            }), 200
        
        except ValueError as e:
            
            db.session.rollback()
            print(sys.exc_info())
            abort(422)


    @app.route("/movies/<movie_id>")
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):

        movie = Movie.query.get(movie_id)

        return render_template('index.html',
            movies=Movie.query.order_by('id').all(),
            active_movie=Movie.query.get(movie_id),
            actors=Actor.query.order_by('id').all()
            )


    @app.route("/movies/create", methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(payload):
        error = False
        body = {}
        try:
            title = request.get_json()['title']
            release_date = request.get_json()['release_date']
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            body['id'] = movie.id
            body['title'] = movie.title
        
        except KeyError:
            error = True
            status_code = 400
            db.session.rollback()
            print(sys.exc_info())

        except ValueError:
            error = True
            status_code = 500
            db.session.rollback()
            print(sys.exc_info())
        
        finally:
            db.session.close()
        
        if error:
            abort(status_code)
        
        else:
            body['success'] = True
            return jsonify(body), 200
   

    @app.route("/movies/<movie_id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        else:
            movie.delete()
            return jsonify({
                "success": True,
                "movie": movie_id}), 200


    @app.route("/movies/<movie_id>", methods=['PATCH'])
    @requires_auth('post:movies')
    def patch_movie(payload, movie_id):
        
        error = False
        try:
            body = request.get_json()
            new_title = body.get("title", None)
            new_release_date = body.get('release_date', None)
            movie = Movie.query.filter(Movie.id == movie_id).first_or_404()
            if new_title:
                movie.title = new_title
            if new_release_date:
                movie.release_date = new_release_date
            movie.update()
        
        except KeyError:
            error = True
            status_code = 400
            db.session.rollback()
            print(sys.exc_info())

        except DataError:
            error = True
            status_code = 400
            db.session.rollback()
            print(sys.exc_info())
        
        except ValueError:
            error = True
            status_code = 500
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()
        
        if error == True:
            abort(status_code)
    
        return jsonify({
            "success": True,
            "movie": new_title,
            "release_date": new_release_date
        }), 200


#  Actors
#  ----------------------------------------------------------------


    @app.route("/actors")
    @requires_auth('get:actors')
    def get_actors(payload):

        
        actors_info = []
        try:
            actors = db.session.query(Actor).all()
            if len(actors) == 0:
                return jsonify({
                    'success': False,
                    'message': 'No records were found'
                }), 404
            
            else:
                for actor in actors:
                                    
                    actors_info.append({
                        'casting:': [
                            {
                                "movie_id": x.id,
                                "movie_title": x.title,
                                "movie_release_date": x.release_date.strftime("%B %d %Y %H:%M:%S")
                            }
                            for x in actor.movies
                        ],
                        'actor_id': actor.id,
                        'actor_name': actor.name,
                        'actor_age': actor.age,
                        'actor_gender': actor.gender
                    })

            return jsonify({
                "success": True,
                "actor_details": actors_info,
                "total_actors": len(actors)
            }), 200
        
        except ValueError as e:
            
            db.session.rollback()
            print(sys.exc_info())
            abort(422)


    @app.route("/actors/<actor_id>")
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):

        
        
        error = False
        try:
            actor = Actor.query.filter(Actor.id == actor_id).first_or_404()
        
        except ValueError as e:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        
        finally:
            db.session.close()
        if error:
            abort(404)

        return jsonify({
                "success": True,
                "id": actor.id,
                "actor": actor.name
            }), 200


    @app.route("/actors/create", methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
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
            return jsonify(body), 200


    @app.route("/actors/<actor_id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):

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
    @requires_auth('post:actors')
    def patch_actor(payload, actor_id):

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


#  Perfermance
#  ----------------------------------------------------------------

    @app.route("/performances")
    @requires_auth('get:performance')
    def get_perfermance(payload):

        
        performance_info = []
        try:
            performances = db.session.query(Performance).all()
            if len(performances) == 0:
                return jsonify({
                    'success': False,
                    'message': 'No records were found'
                })
            
            else:
                for performance in performances:
                    movie = Movie.query.filter_by(id = performance.movie_id).first()
                    actor = Actor.query.filter_by(id = performance.actor_id).first()
                
                    performance_info.append({
                        'movie_id': performance.movie_id,
                        'movie_title': movie.title,
                        'movie_release_date': movie.release_date.strftime("%B %d %Y %H:%M:%S"),
                        'actor_id': performance.actor_id,
                        'actor_name': actor.name,
                        'actor_age': actor.age,
                        'actor_gender': actor.gender
                    })

            return jsonify({
                "success": True,
                "performance_details": performance_info,
                "total perfermances": len(performances)
            }), 200
        
        except:
            abort(422)

    
    @app.route("/performance", methods=['POST'])
    @requires_auth('post:performance')
    def create_performance(payload):
        
        error = False
        body = {}
        actor_id = request.get_json()['actor_id']
        movie_id = request.get_json()['movie_id']
        print(actor_id, movie_id)

        try:

            performance = Performance.insert().values(actor_id=actor_id, movie_id=movie_id)
            db.session.execute(performance)
            db.session.commit()

        except ValueError as e:
            error = True
            db.session.rollback()
            print(sys.exc_info())

        finally:
            db.session.close()

        if error:
            abort(500)

        else:
            return jsonify({
                "success": True,
                "actor_id": actor_id,
                "movie_id": movie_id
            }), 200

        


#  Error Handling
#  ----------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def methodnotallowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code



    return app

    