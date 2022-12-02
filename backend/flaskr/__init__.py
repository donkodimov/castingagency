import os, sys
from flask import Flask, request, abort, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

from models import setup_db, Movie, Actor, db




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
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
            #active_movie=Movie.query.get(movie_id),
            #actors=Actor.query.filter_by(movie_id=movie_id).order_by('id').all()
            )

    @app.route("/movies/create", methods=['POST'])
    def create_movies():
        error = False
        body = {}
        try:
            title = request.get_json()['title']
            movie = Movie(title=title, genre="genre", release_date="release_date", rating=5)
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

    return app