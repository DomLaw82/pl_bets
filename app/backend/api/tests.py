import unittest
import requests
from api import app  # Replace with the actual import for your Flask app

# Assuming you have already set up a Flask-Rebar registry
from flask_rebar import Rebar
rebar = Rebar(app)
registry = rebar.create_handler_registry()

class TestMyAPI(unittest.TestCase):
    def setUp(self):
        self.api_url = 'http://localhost:5000'  # Update with your API's URL

    def test_hello_endpoint(self):
        response = requests.get(f'{self.api_url}/api/hello')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})


# create a health endpoint in the app that tests and return the status of all endpoints in the app

if __name__ == '__main__':
    unittest.main()