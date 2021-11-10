import unittest
import json
from app import create_app
from app.database import setup_db, db
from app.models.Book import Book
from app.models.User import User
from app.models.Library import Library
import http.client
import os

class LibraryAuthTestCase(unittest.TestCase):
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
        user = User(id='gVEEvnwDwjkq63W9xpI8veG0XXxVvXwn@clients', firstName='test', lastName='name', email='test@email.com')
        book = Book(title="test_book", description='test description', author='test author')
        book2 = Book(title="test_book_2", description='test description', author='test author 2')
        db.session.add(user)
        db.session.add(book)
        db.session.add(book2)
        db.session.commit()
        db.session.close()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def getUserToken(self):
        conn = http.client.HTTPSConnection("dev-pca1g5k8.us.auth0.com")
        payload = "{\"client_id\":\"gVEEvnwDwjkq63W9xpI8veG0XXxVvXwn\",\"client_secret\":\"fv_35doQlHa1dQ6YpSCx1nkhl6S_t-I2sD-SMDqStp3Un0-fLh6VXD1fJsSR5Bne\",\"audience\":\"Capstone\",\"grant_type\":\"client_credentials\"}"
        headers = { 'content-type': "application/json" }
        conn.request("POST", "/oauth/token", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        data = json.loads(data)
        return data['access_token']

    def test_get_books_from_library_success(self):
        res = self.client().get('/library', headers= {"Authorization": "Bearer " + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_book_from_library_success(self):
        res = self.client().post('/library', json={
            "book_id": "2", 
        }, headers= {"Authorization": "Bearer " + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_book_from_library_success(self):
        res = self.client().post('/library', json={
            "book_id": "1", 
        }, headers= {"Authorization": "Bearer " + self.token})
        data = json.loads(res.data)
        res = self.client().delete('/library/' + str(data['book']['id']), headers= {"Authorization": "Bearer " + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_book_from_library_not_found(self):
        res = self.client().post('/library', json={
            "book_id": "1000", 
        }, headers= {"Authorization": "Bearer " + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_book_from_library_not_found(self):
        res = self.client().delete('/library/1000', headers= {"Authorization": "Bearer " + self.token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()