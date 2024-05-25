import unittest
import json
from unittest.mock import patch
from api import app

# TODO - Testing

class TestTeamFunction(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('api.db.get_dict')
    def test_get_all_teams(self, mock_get_dict):
        mock_get_dict.return_value = [{'id': 'team_one', 'name': 'Team One'}, {'id': 'team_two', 'name': 'Team Two'}]
        
        response = self.app.get('/teams')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'id': 'team_one', 'name': 'Team One'}, {'id': 'team_two', 'name': 'Team Two'}])


# create a health endpoint in the app that tests and return the status of all endpoints in the app

if __name__ == '__main__':
    unittest.main()