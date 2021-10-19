import unittest
import json
from .test_config import DB_PATH
from app import create_app
from database import setup_db, db
from Models.User import User

class UserTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, DB_PATH)
        db.drop_all()
        db.create_all()
        db.session.add(User(username="test_name", email='test@email.com'))
        db.session.commit()
        db.session.close()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    '''
    Tests retrieving paginated questions successfully
    '''
    def test_get_all_users(self):
        res = self.client().get('/users')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['users']) >= 0)

    '''
    Tests getting a question by ID successfully
    '''
    def test_get_user_success(self):
        res = self.client().get('/users/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['user'],  None)

    '''
    Tests getting a question by ID that doesn't exist in the database
    '''
    def test_get_user_not_found(self):
        res = self.client().get('/users/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Tests adding new question successfully
    '''
    def test_post_user_success(self):
        res = self.client().post('/users', json={
            "username": "test_name2", 
            "email": "test2@email.com"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['user'], None)

    '''
    Tests deleting a question by ID successfully
    '''
    def test_delete_user_success(self):
        res = self.client().delete('/users/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user']['id'], 1)

    '''
    Tests deleting a question by ID that doesn't exist in the database
    '''
    def test_delete_user_not_found(self):
        res = self.client().delete('/users/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''
    Tests deleting a question by ID successfully
    '''
    def test_update_user_success(self):
        res = self.client().patch('/users/1', json={
            "username": "test_name2", 
            "email": "test2@email.com"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user']['username'], 'test_name2')
        self.assertEqual(data['user']['email'], 'test2@email.com')

    '''
    Tests deleting a question by ID that doesn't exist in the database
    '''
    def test_update_user_not_found(self):
        res = self.client().patch('/users/1000', json={
            "username": "test_name2", 
            "email": "test2@email.com"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()