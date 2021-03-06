import unittest
import json
from app import create_app
from app.api.v2.models.user_model import Users


class TestRegistration(unittest.TestCase):
    """Authentication TestCases Class"""

    def setUp(self):
        """ Define tests variables"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            # create all tables
            db = Users()
            db.create_table_user()

        self.data = {
            'name': 'Jane Doe',
            'username': 'jdoe',
            'email': 'jdoe@gmail.com',
            'password': 'jdoepass',
            'gender': 'female',
            'role': 'admin'
        }
        self.data_login = {
            'username': 'admin',
            'password': 'adminpass'
        }

    def test_registration(self):
        """Test registration of new users"""

        # user login
        response_login = self.client.post(
                                    '/api/v2/auth/login', 
                                    data=json.dumps(self.data_login),
                                    content_type='application/json')
        result_login = json.loads(response_login.data)
        print(result_login)
        token = result_login['access_token']

        response = self.client.post(
                            '/api/v2/auth/signup',
                            headers=dict(Authorization='Bearer '+token), 
                            data=json.dumps(self.data),
                            content_type='application/json')
        
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User created successfully')
        self.assertEqual(response.status_code, 201)

    def test_empty_fields(self):
        """Test registration with missing username"""

        # user login
        response_login = self.client.post(
                                    '/api/v2/auth/login', 
                                    data=json.dumps(self.data_login),
                                    content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        # user signup
        response = self.client.post(
                                '/api/v2/auth/signup',
                                headers=dict(Authorization='Bearer '+token),
                                data=json.dumps({
                                    'name': 'Jane Doe',
                                    'email': 'jdoe@gmail.com',
                                    'password': 'jdoepass',
                                    'gender': 'female',
                                    'role': 'admin'}),
                                content_type='application/json')

        result = json.loads(response.data)
        self.assertEqual(
            result['message'], {"username": "This field cannot be blank"})
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        """Test registration with invalid email"""

        # user login
        response_login = self.client.post(
                                    '/api/v2/auth/login', 
                                    data=json.dumps(self.data_login),
                                    content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        # user signup
        response = self.client.post(
                                '/api/v2/auth/signup',
                                headers=dict(Authorization='Bearer '+token), 
                                data=json.dumps({
                                    'name': 'Jane Doe',
                                    'username': 'jdoe',
                                    'email': 'jdoegmail.com',
                                    'password': 'jdoepass',
                                    'gender': 'female',
                                    'role': 'admin'}),
                                content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['message'], "Invalid Email")
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test if API can GET all users"""

        # user login
        response_login = self.client.post(
                                    '/api/v2/auth/login',
                                    data=json.dumps(self.data_login),
                                    content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']
        
        # user signup
        response = self.client.post(
                                '/api/v2/auth/signup',
                                headers=dict(Authorization='Bearer '+token),
                                data=json.dumps(self.data),
                                content_type='application/json')       
    
        response = self.client.get(
                                '/api/v2/users',
                                headers=dict(Authorization='Bearer '+token))
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Users successfully retrieved')
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        """Test if API can GET single user by id"""

        # user login
        response_login = self.client.post(
                                    '/api/v2/auth/login',
                                    data=json.dumps(self.data_login),
                                    content_type='application/json')
        result_login = json.loads(response_login.data)
        token = result_login['access_token']

        # user signup
        response = self.client.post(
                                '/api/v2/auth/signup',
                                headers=dict(Authorization='Bearer '+token), 
                                data=json.dumps(self.data),
                                content_type='application/json')        

        response = self.client.get(
                            '/api/v2/users/2',
                            headers=dict(Authorization='Bearer '+token))
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'User successfully retrieved')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """Removes all initialised variables and Drops table"""
        self.app_context.pop()
        db = Users()
        db.drop_table_user()

