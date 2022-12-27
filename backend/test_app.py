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

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_actor_id(self):
        res = self.client().get("/actors/1", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"]) 
    
    def test_get_all_actors(self):
        res = self.client().get("/actors", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue([data["actor_details"]])
    
    

    def test_get_performance(self):
        res = self.client().get("/performances", headers={'Authorization': 'Bearer {}'.format(self.producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["performance_details"])
        self.assertEqual(len(data["performance_details"]), 2)
        
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()