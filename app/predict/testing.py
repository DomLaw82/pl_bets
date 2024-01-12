import pandas as pd
from dataset_creation.create_dataset import *
import unittest


class TestCreateDataset(unittest.TestCase):

    def test_get_match_column_values(self):
        # Create a sample DataFrame of matches
        all_matches = pd.DataFrame({
            "home_team_id": [1, 2, 3],
            "away_team_id": [4, 5, 6],
            "season": [2019, 2020, 2021],
            "id": [101, 102, 103]
        })

        # Call the function
        result = get_match_column_values(all_matches)

        # Define the expected output
        expected_output = [
            [1, 4, 2019, 101],
            [2, 5, 2020, 102],
            [3, 6, 2021, 103]
        ]

        # Compare the result with the expected output
        self.assertEqual(result, expected_output)

    def test_group_stats_by_player_for_home_and_away_teams(self):
        # Create a sample DataFrame for testing
        df = pd.DataFrame({
            'player_id': [1, 2, 3, 2, 5],
            'team_id': ['A', 'B', 'A', 'B', 'A'],
            'season': [2020, 2020, 2021, 2021, 2021],
            'goals': [10, 5, 8, 3, 6],
            'assists': [5, 3, 4, 2, 3]
        })
        df_2 = pd.DataFrame({
            'player_id': [1, 2, 2, 4, 5],
            'team_id': ['A', 'B', 'A', 'B', 'A'],
            'season': [2020, 2020, 2021, 2021, 2021],
            'goals': [10, 5, 8, 3, 6],
            'assists': [5, 3, 4, 2, 3]
        })

        home_team_id = 'A'
        away_team_id = 'B'

        # Call the function
        result = group_stats_by_player_for_home_and_away_teams(df, home_team_id, away_team_id)
        result_2 = group_stats_by_player_for_home_and_away_teams(df_2, home_team_id, away_team_id)

        # Define the expected result for default behavior (pred=False)
        expected_result_default = pd.DataFrame({
            'player_id': [1, 2, 3, 5],
            'team_id': ['A', 'B', 'A', 'A'],
            'goals': [10, 8, 8, 6],
            'assists': [5, 5, 4, 3]
        })
        expected_result_default_2 = pd.DataFrame({
            'player_id': [1, 2, 4, 5],
            'team_id': ['A', 'A', 'B', 'A'],
            'goals': [10, 13, 3, 6],
            'assists': [5, 7, 2, 3]
        })

        # Assert that the actual result matches the expected result for default behavior
        self.assertTrue(result.equals(expected_result_default))
        self.assertTrue(result_2.equals(expected_result_default_2))

        # Call the function with pred=True
        result_pred = group_stats_by_player_for_home_and_away_teams(df, home_team_id, away_team_id, pred=True)

        # Define the expected result for pred=True
        expected_result_pred = pd.DataFrame({
            'player_id': [1, 2, 3, 4, 5],
            'team_id': ['A', 'B', 'A', 'B', 'A'],
            'goals': [18, 5, 14, 5, 6],
            'assists': [8, 3, 4, 2, 3]
        })

        # Assert that the actual result matches the expected result for pred=True
        self.assertTrue(result_pred.equals(expected_result_pred))
        
		

if __name__ == '__main__':
    unittest.main()
    
def test_create_per_90_stats():
    # Create a sample DataFrame with statistics
    df = pd.DataFrame({
        'Goals': [76, 64, 52],
        'Assists': [18, 12, 10],
        'Shots': [200, 180, 150]
    })

    # Call the function to create per 90 minutes statistics
    df_per_90 = create_per_90_stats(df)

    # Define the expected per 90 minutes statistics
    expected_df_per_90 = pd.DataFrame({
        'Goals': [2, 1.68, 1.37],
        'Assists': [0.47, 0.32, 0.26],
        'Shots': [5.26, 4.74, 3.95]
    })

    # Assert that the actual per 90 minutes statistics match the expected values
    assert df_per_90.equals(expected_df_per_90), "Per 90 minutes statistics are incorrect"
    
def test_create_contribution_per_90_stats():
    # Create a sample DataFrame with statistics
    df = pd.DataFrame({
        'Goals': [76, 64, 52],
        'Assists': [18, 12, 10],
        'Shots': [200, 180, 150],
        'minutes_played': [2700, 2400, 2000]
    })

    # Call the function to create contribution per 90 minutes statistics
    df_contribution_per_90 = create_contribution_per_90_stats(df)

    # Define the expected contribution per 90 minutes statistics
    expected_df_contribution_per_90 = pd.DataFrame({
        'Goals': [2.53, 2.40, 2.34],
        'Assists': [0.60, 0.45, 0.45],
        'Shots': [6.67, 6.00, 6.00]
    })

    # Assert that the actual contribution per 90 minutes statistics match the expected values
    assert df_contribution_per_90.equals(expected_df_contribution_per_90), "Contribution per 90 minutes statistics are incorrect"

def test_group_stats_by_team():
    # Create a sample DataFrame with player statistics
    df = pd.DataFrame({
        'player_id': [1, 2, 3, 4, 5],
        'team_id': ['A', 'A', 'B', 'B', 'A'],
        'goals': [2, 1, 3, 2, 1],
        'assists': [1, 0, 2, 1, 0]
    })

    # Call the function to group the statistics by team
    df_grouped = group_stats_by_team(df)

    # Define the expected DataFrame with team statistics
    expected_df_grouped = pd.DataFrame({
        'team_id': ['A', 'B'],
        'goals': [4, 5],
        'assists': [1, 3]
    })

    # Assert that the actual DataFrame with team statistics matches the expected values
    assert df_grouped.equals(expected_df_grouped), "Grouped team statistics are incorrect"
    
def test_convert_team_rows_to_single_row():
    # Create a sample DataFrame with team rows
    df = pd.DataFrame({
        'team_id': ['A', 'B', 'C'],
        'home_team_id': ['A', 'B', 'C'],
        'away_team_id': ['D', 'E', 'F'],
        'goals': [2, 1, 3],
        'assists': [1, 0, 2]
    })

    # Call the function to convert team rows to a single row
    single_row_df = convert_team_rows_to_single_row(df)

    # Define the expected DataFrame with a single row representing the teams
    expected_single_row_df = pd.DataFrame({
        'team_id': ['A'],
        'home_team_id': ['A'],
        'away_team_id': ['D'],
        'goals': [1],
        'assists': [1]
    })

    # Assert that the actual DataFrame with a single row matches the expected values
    assert single_row_df.equals(expected_single_row_df), "Conversion to single row is incorrect"