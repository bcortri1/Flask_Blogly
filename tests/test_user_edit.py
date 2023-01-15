from unittest import TestCase
from app import app
from models import db, User, connect_db
from seed import seed_data

class UserEdit(TestCase):

    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        
        seed_data()
        
        
    def test_edit_user(self):
        with self.client:
            response = self.client.post("/users/1/edit",json = {"first-name": "Patrick","last-name":"Stewart"})
            patrick = User.query.get(1)
            self.assertEqual(patrick.first_name, "Patrick")
            self.assertEqual(patrick.last_name, "Stewart")
            self.assertEqual(patrick.full_name, "Patrick Stewart")