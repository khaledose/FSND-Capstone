import unittest
import json
from app import create_app
from app.database import setup_db, db
from app.models.Book import Book


class LibraryNoAuthTestCase(unittest.TestCase):
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

    def test_post_book_no_auth(self):
        res = self.client().post('/library', json={
            "book_id": "1", 
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_book_no_auth(self):
        res = self.client().delete('/library/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()