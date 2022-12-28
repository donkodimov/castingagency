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

#__________Test for success behavior of endpoint GET /movies___________________#

    def test_get_all_movies(self):
        res = self.client().get("/movies", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["movie_details"]])

#__________Test for error behavior of endpoint GET /movies_____________________#

    def test_get_all_movies_404(self):
        self.client().delete("/movies/1", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        self.client().delete("/movies/2", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        self.client().delete("/movies/3", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        res = self.client().get("/movies", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        drop_and_init_db(self.app)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint DELETE /movies/<movie_id>_____#

    def test_delete_one_movie(self):
        res = self.client().delete("/movies/1", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        drop_and_init_db(self.app)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual([data["movie"]], ['1'])

#__________Test for error behavior of endpoint DELETE /movies/<movie_id>_______#

    def test_delete_one_movie_404(self):
        res = self.client().delete("/movies/111234", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue([data["message"]])

#__________Test for success behavior of endpoint GET /actor/<actor_id>_________#

    def test_get_actor_id(self):
        res = self.client().get("/actors/1", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"]) 
    
#__________Test for success behavior of endpoint GET /actors___________________#

    def test_get_all_actors(self):
        res = self.client().get("/actors", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["actor_details"]])
    
#__________Test for success behavior of endpoint GET /performance______________#

    def test_get_performance(self):
        res = self.client().get("/performances", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["performance_details"])
        self.assertEqual(len(data["performance_details"]), 2)
        
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()