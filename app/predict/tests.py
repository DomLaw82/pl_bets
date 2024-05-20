import unittest
import pandas as pd
from dataset_creation.create_dataset import group_stats_by_player_for_home_and_away_teams, create_per_90_stats, create_contribution_per_90_stats, group_stats_by_team, convert_team_rows_to_single_row, combine_form_and_career_stats

import unittest
import pandas as pd
import numpy as np

class TestCreateDataset(unittest.TestCase):
    def test_group_stats_by_player_for_home_and_away_teams(self):
        # Create a sample DataFrame with player statistics
        df = pd.DataFrame({
            'player_id': [1, 2, 3, 4, 4],
            'season': [2020, 2020, 2020, 2019, 2020],
            'team_id': ['A', 'A', 'B', 'C', 'B'],
            'goals': [2, 1, 3, 2, 1],
            'assists': [1, 0, 2, 1, 0]
        })

        home_team_id = 'A'
        away_team_id = 'B'
        home_team_squad_ids = [1, 2]

        # Call the function to group the statistics by player for the home and away teams
        grouped_df = group_stats_by_player_for_home_and_away_teams(df, home_team_id, away_team_id, home_team_squad_ids)

        # Define the expected DataFrame with grouped player statistics
        expected_grouped_df = pd.DataFrame({
            'player_id': [1, 2, 3, 4],
            'team_id': ['A', 'A', 'B', 'B'],
            'goals': [2, 1, 3, 1.5],
            'assists': [1, 0, 2, 0.5]
        })

        # Assert that the actual DataFrame with grouped player statistics matches the expected values
        self.assertTrue(grouped_df.equals(expected_grouped_df), "Grouped player statistics are incorrect")

    def test_create_per_90_stats(self):
        # Create a sample DataFrame with statistics
        df = pd.DataFrame({
            'Goals': [76, 64, 52],
            'Assists': [18, 12, 10],
            'Shots': [200, 180, 150]
        })

        # Call the function to create per 90 minutes statistics
        df_per_90 = create_per_90_stats(df, ["Goals", "Assists", "Shots"])

        # Define the expected per 90 minutes statistics
        expected_df_per_90 = pd.DataFrame({
            'Goals': [2, 1.68, 1.37],
            'Assists': [0.47, 0.32, 0.26],
            'Shots': [5.26, 4.74, 3.95]
        })

        # Assert that the actual per 90 minutes statistics match the expected values
        self.assertTrue(df_per_90.equals(expected_df_per_90), "Per 90 minutes statistics are incorrect")

    def test_create_contribution_per_90_stats(self):
        # Create a sample DataFrame with statistics
        df = pd.DataFrame({
            'goals': [10, 5, 3],
            'assists': [2, 1, 0],
            'minutes_played': [9, 45, 90]
        })

        # Call the function to create contribution per 90 minutes statistics
        df_contribution_per_90 = create_contribution_per_90_stats(df, ['goals', 'assists', 'minutes_played'])

        # Define the expected contribution per 90 minutes statistics
        expected_df_contribution_per_90 = pd.DataFrame({
            'goals': [1, 2.5, 3],
            'assists': [0.2, 0.5, 0],
        })

        # Assert that the actual contribution per 90 minutes statistics match the expected values
        self.assertTrue(df_contribution_per_90.equals(expected_df_contribution_per_90), "Contribution per 90 minutes statistics are incorrect")
    
    def test_group_stats_by_team(self):
        # Create a sample DataFrame with player statistics
        df = pd.DataFrame({
            'player_id': [1, 2, 3, 4, 5, 6],
            'team_id': ['A', 'A', 'B', 'B', 'B', 'A'],
            'goals': [2, 1, 3, 2, 1, 7],
            'assists': [1, 0, 2, 1, 0, 3]
        })

        # Call the function to group the statistics by team
        grouped_df = group_stats_by_team(df)

        # Define the expected DataFrame with grouped team statistics
        expected_grouped_df = pd.DataFrame({
            'team_id': ['A', 'B'],
            'goals': [10, 6],
            'assists': [4, 3]
        })

        # Assert that the actual DataFrame with grouped team statistics matches the expected values
        self.assertTrue(grouped_df.equals(expected_grouped_df), "Grouped team statistics are incorrect")

    def test_convert_team_rows_to_single_row(self):
        # Create a sample DataFrame with team rows
        df = pd.DataFrame({
            'team_id': ['A', 'B'],
            'goals': [24, 15],
            'assists': [6, 13]
        })

        # Call the function to convert team rows to a single row
        converted_df = convert_team_rows_to_single_row(df, 'A', 'B', ['goals', 'assists'])

        # Define the expected DataFrame with a single row representing the teams
        expected_df = pd.DataFrame({
            'goals': [9],
            'assists': [-7]
        })

        # Assert that the actual DataFrame matches the expected values
        self.assertTrue(converted_df.equals(expected_df), "Converted team rows are incorrect")

    def test_combine_form_and_career_stats(self):
        # Create sample career and form DataFrames
        career_df = pd.DataFrame({
            'goals': [10],
            'assists': [2],
            'minutes_played': [900],
        })

        form_df = pd.DataFrame({
            'goals': [2],
            'assists': [1],
            'minutes_played': [90],
        })

        # Call the function to combine the career and form statistics
        combined_df_one = combine_form_and_career_stats((career_df, form_df), pred=True, columns_to_evaluate=['goals', 'assists', "minutes_played"])

        # Define the expected combined DataFrame
        expected_combined_df_one = pd.DataFrame({
            'goals': [6.8],
            'assists': [1.6],
            'minutes_played': [576]
        })

        # Assert that the actual combined DataFrame matches the expected values
        self.assertTrue(combined_df_one.equals(expected_combined_df_one), "Combined statistics are incorrect")


if __name__ == '__main__':
    unittest.main()