import unittest
import json
from app import create_app
from app.database import setup_db, db
from app.models.Book import Book


class BookNoAuthTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.config.from_object("config.TestConfig")
        self.client = self.app.test_client
        setup_db(self.app)
        db.drop_all()
        db.create_all()
        db.session.add(Book(title="test_book", description='test description', author='test author'))
        db.session.add(Book(title="test_book 2", description='test description 2', author='test author 2'))
        db.session.commit()
        db.session.close()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_books_success(self):
        res = self.client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['books']) == 2)

    def test_get_book_success(self):
        res = self.client().get('/books/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['book'],  None)

    def test_get_book_not_found(self):
        res = self.client().get('/books/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_book_no_auth(self):
        res = self.client().post('/books', json={
            "title": "test_book 3", 
            "description": "test description 3",
            "author": "test author 3"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_book_no_auth(self):
        res = self.client().delete('/books/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_book_no_auth(self):
        res = self.client().patch('/books/1', json={
            "title": "test_name5", 
            "description": "test description 5"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()