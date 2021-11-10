import unittest
import json
from app import create_app
from app.database import setup_db, db
import http.client
import os

class BookNoPermissionTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        os.environ["AUTH0_AUDIENCE"] = "Capstone"
        self.app = create_app()
        self.app.config.from_object("config.TestConfig")
        self.client = self.app.test_client
        self.token = self.getUserToken()
        setup_db(self.app)
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""

    def getUserToken(self):
        conn = http.client.HTTPSConnection("dev-pca1g5k8.us.auth0.com")
        payload = "{\"client_id\":\"gVEEvnwDwjkq63W9xpI8veG0XXxVvXwn\",\"client_secret\":\"fv_35doQlHa1dQ6YpSCx1nkhl6S_t-I2sD-SMDqStp3Un0-fLh6VXD1fJsSR5Bne\",\"audience\":\"Capstone\",\"grant_type\":\"client_credentials\"}"
        headers = { 'content-type': "application/json" }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        data = json.loads(data)
        return data['access_token']

    def test_post_book_no_permission(self):
        res = self.client().post('/books', json={
            "title": "test_book 3", 
            "description": "test description 3",
            "author": "test author 3"
        }, headers= {"Authorization": "Bearer " + self.token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_book_no_permission(self):
        res = self.client().delete('/books/1', headers= {"Authorization": "Bearer " + self.token})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_update_book_no_permission(self):
        res = self.client().patch('/books/1', json={
            "title": "test_name5", 
            "description": "test description 5"
        }, headers= {"Authorization": "Bearer " + self.token})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()