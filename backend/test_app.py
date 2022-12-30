import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, drop_and_init_db, Actor, Movie, Performance
from config import settings


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = settings.POSTGRES_DB_TEST
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.producer_token = settings.PRODUCER
        self.director_token = settings.DIRECTOR
        self.assistant_token = settings.ASSISTANT
        
        setup_db(self.app, self.database_path)
        #drop_and_init_db(self.app)

        self.delete_movies = {

        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

#================MOVIES TESTS==================================================#

#__________Test for success behavior of endpoint GET /movies___________________#

    def test_get_all_movies(self):
        res = self.client().get("/movies", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["movie_details"]])

#__________Test for error behavior of endpoint GET /movies_____________________#

    def test_get_all_movies_404(self):
        [self.client().delete(
            "/movies/" + str(x),
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
            for x in [1,2,3]]
        res = self.client().get(
            "/movies",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        drop_and_init_db(self.app)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint DELETE /movies/<movie_id>_____#

    def test_delete_one_movie(self):
        res = self.client().delete(
            "/movies/1",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        drop_and_init_db(self.app)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual([data["movie"]], ['1'])

#__________Test for error behavior of endpoint DELETE /movies/<movie_id>_______#

    def test_delete_one_movie_404(self):
        res = self.client().delete(
            "/movies/111234",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for error behavior of endpoint DELETE /movies/<movie_id>_______#

    def test_delete_one_movie_403(self):
        res = self.client().delete(
            "/movies/1",
            headers={'Authorization': 'Bearer {}'.format(self.assistant_token)}
            )
        drop_and_init_db(self.app)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint POST /movies/create___________#

    def test_create_one_movie(self):
        res = self.client().post(
            "/movies/create",
            json={"title":"Casablanca", "release_date":"2023-01-25 15:20:00"}, 
            headers={'Authorization': 'Bearer {}'.format(self.director_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["title"]])

#__________Test for error behavior of endpoint POST /movies/create_____________#

    def test_create_one_movie_400(self):
        res = self.client().post(
            "/movies/create",
            json={"title":"Casablanca"}, 
            headers={'Authorization': 'Bearer {}'.format(self.director_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for error behavior of endpoint POST /movies/create_____________#

    def test_create_one_movie_403(self):
        res = self.client().post(
            "/movies/create",
            json={"title":"Casablanca"}, 
            headers={'Authorization': 'Bearer {}'.format(self.assistant_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint PATCH /movies/<movie_id>______#

    def test_update_one_movie(self):
        res = self.client().patch(
            "/movies/1",
            json={"title":"Casablanca", "release_date":"2025-01-25 15:20:00"}, 
            headers={'Authorization': 'Bearer {}'.format(self.director_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["movie"]])

#__________Test for error behavior of endpoint PATCH /movies/<movie_id>______#

    def test_update_one_movie_400(self):
        res = self.client().patch(
            "/movies/1",
            json={"title":"Casablanca", "release_date":"2025"}, 
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#================ACTORS TESTS==================================================#

#__________Test for success behavior of endpoint GET /actor/<actor_id>_________#

    def test_get_actor_id(self):
        res = self.client().get(
            "/actors/1", 
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

#__________Test for error behavior of endpoint GET /actor/<actor_id>_________#

    def test_get_actor_id(self):
        res = self.client().get(
            "/actors/101010101", 
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])
    
#__________Test for success behavior of endpoint GET /actors___________________#

    def test_get_all_actors(self):
        res = self.client().get(
            "/actors",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["actor_details"]])

#__________Test for error behavior of endpoint GET /actors_____________________#

    def test_get_all_actors_404(self):
        actors_res = self.client().get(
            "/actors",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data_actors = json.loads(actors_res.data)
        actors_list = [*range(1, data_actors["total_actors"] + 1)]
        [self.client().delete(
            "/actors/" + str(x),
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
            for x in actors_list]
        res = self.client().get(
            "/actors",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint DELETE /actors/<actor_id>_____#

    def test_delete_one_actor(self):
        res = self.client().delete(
            "/actors/1",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        drop_and_init_db(self.app)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual([data["actor"]], ['1'])

#__________Test for error behavior of endpoint DELETE /actors/<actor_id>_______#

    def test_delete_one_actor_404(self):
        res = self.client().delete(
            "/actors/111234",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for error behavior of endpoint DELETE /actors/<actor_id>_______#

    def test_delete_one_actor_403(self):
        res = self.client().delete(
            "/actors/1",
            headers={'Authorization': 'Bearer {}'.format(self.director_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint POST /actors/create___________#

    def test_create_one_actor(self):
        res = self.client().post(
            "/actors/create",
            json={"name": "Alexa Colins", "age": 27, "gender": "female"}, 
            headers={'Authorization': 'Bearer {}'.format(self.director_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["name"]])

#__________Test for error behavior of endpoint POST /actors/create_____________#

    def test_create_one_actor_400(self):
        res = self.client().post(
            "/actors/create",
            json={"name":"Cisco Valmaro"}, 
            headers={'Authorization': 'Bearer {}'.format(self.director_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for error behavior of endpoint POST /actors/create_____________#

    def test_create_one_actor_403(self):
        res = self.client().post(
            "/actors/create",
            json={"name": "Maxim Gorski", "age": 37, "gender": "male"}, 
            headers={'Authorization': 'Bearer {}'.format(self.assistant_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint PATCH /actors/<actor_id>______#

    def test_update_one_actor(self):
        res = self.client().patch(
            "/actors/1",
            json={"name": "John River", "age": 24, "gender": "male"}, 
            headers={'Authorization': 'Bearer {}'.format(self.director_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["name"]])

#__________Test for error behavior of endpoint PATCH /actors/<actor_id>______#

    def test_update_one_actor_422(self):
        res = self.client().patch(
            "/actors/1",
            json={"name": "Alexa Colins", "age": "some age", "gender": 4}, 
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#================PERFORMANCE TESTS=============================================#
    
#__________Test for success behavior of endpoint GET /performance______________#

    def test_get_performance(self):
        res = self.client().get("/performances", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["performance_details"])
        self.assertEqual(len(data["performance_details"]), 2)
        
#__________Test for error behavior of endpoint GET /performance________________#

    def test_get_performance_404(self):
        actors_res = self.client().get(
            "/actors",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data_actors = json.loads(actors_res.data)
        actors_list = [*range(1, data_actors["total_actors"] + 1)]
        [self.client().delete(
            "/actors/" + str(x),
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
            for x in actors_list]
        res = self.client().get(
            "/performances",
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        drop_and_init_db(self.app)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["message"])
        self.assertEqual(data["success"], False)

#__________Test for success behavior of endpoint POST /performance_____________#

    def test_create_one_performance(self):
        res = self.client().post(
            "/performance",
            json={"actor_id": 1, "movie_id": 2}, 
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["actor_id"]])
        self.assertTrue([data["movie_id"]])

#__________Test for error behavior of endpoint POST /performance_______________#

    def test_create_one_performance_400(self):
        res = self.client().post(
            "/performance",
            json={"actor_id": 1}, 
            headers={'Authorization': 'Bearer {}'.format(self.producer_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for error behavior of endpoint POST /performance_______________#

    def test_create_one_performance_403(self):
        res = self.client().post(
            "/performance",
            json={"actor_id": 1, "movie_id": 3}, 
            headers={'Authorization': 'Bearer {}'.format(self.assistant_token)}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()