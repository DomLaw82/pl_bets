import unittest
import pandas as pd
import numpy as np
# from dataset_creation.create_dataset import group_stats_by_player_for_home_and_away_teams, create_per_90_stats, create_contribution_per_90_stats, group_stats_by_team, convert_team_rows_to_single_row, combine_form_and_career_stats
from win_prediction_modules.data_preparation import get_team_form, get_last_five_head_to_head_matches_rolling_goal_difference, add_historic_head_to_head_results

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# class TestCreateDataset(unittest.TestCase):
#     def setUp(self):
#         self.df = pd.DataFrame({
#             "player_id": ["p-00001", "p-00002", "p-00003", "p-00004", "p-00005", "p-00001", "p-00002", "p-00003", "p-00004", "p-00005"],
#             "team_id": ["A", "A", "B", "B", "B", "A", "A", "B", "B", "A"],
#             "season": ["2020/2021"] * 5 + ["2021/2022"] * 5,
#             "goals": [5, 10, 7, 3, 2, 8, 6, 4, 9, 1],
#             "assists": [3, 8, 5, 2, 1, 7, 4, 6, 9, 0],
#             "penalties_scored": [1, 0, 2, 3, 1, 2, 1, 0, 4, 2],
#             "penalties_attempted": [2, 1, 2, 3, 1, 2, 2, 1, 5, 2],
#             "yellow_cards": [1, 2, 1, 0, 3, 2, 1, 0, 1, 2],
#             "red_cards": [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
#             "expected_goals": [4.5, 9.2, 6.8, 2.5, 1.7, 7.3, 5.6, 3.9, 8.4, 0.9],
#             "non_penalty_expected_goals": [3.5, 8.2, 5.8, 1.5, 0.7, 6.3, 4.6, 2.9, 7.4, 0.5],
#             "expected_assisted_goals": [2.1, 6.8, 4.2, 1.3, 0.5, 5.9, 3.4, 2.8, 6.1, 0.3],
#             "progressive_carries": [20, 45, 30, 25, 18, 33, 27, 22, 40, 15],
#             "progressive_passes": [30, 60, 45, 35, 25, 50, 40, 30, 55, 20],
#             "total_passing_distance": [1500, 3000, 2000, 1800, 1200, 2500, 2100, 1700, 2800, 1000],
#             "total_progressive_passing_distance": [1000, 2500, 1500, 1200, 800, 2000, 1700, 1400, 2300, 700],
#             "short_passes_completed": [50, 100, 70, 60, 40, 80, 65, 55, 90, 30],
#             "short_passes_attempted": [60, 120, 85, 75, 50, 95, 80, 65, 110, 40],
#             "medium_passes_completed": [40, 80, 55, 50, 30, 65, 55, 45, 70, 25],
#             "medium_passes_attempted": [50, 100, 70, 65, 40, 80, 70, 55, 90, 35],
#             "long_passes_completed": [20, 40, 30, 25, 15, 35, 30, 20, 45, 10],
#             "long_passes_attempted": [25, 50, 35, 30, 20, 45, 35, 25, 55, 15],
#             "expected_assists": [1.5, 3.2, 2.5, 1.0, 0.7, 2.8, 2.0, 1.4, 3.0, 0.5],
#             "key_passes": [5, 10, 7, 6, 4, 8, 6, 5, 9, 3],
#             "passes_into_final_third": [10, 20, 15, 12, 8, 18, 14, 11, 22, 7],
#             "passes_into_penalty_area": [5, 10, 8, 6, 3, 9, 7, 4, 12, 2],
#             "crosses_into_penalty_area": [3, 6, 4, 5, 2, 7, 5, 3, 8, 1],
#             "shots": [10, 20, 15, 12, 8, 18, 14, 11, 22, 7],
#             "shots_on_target": [7, 15, 10, 9, 6, 12, 10, 8, 16, 5],
#             "average_shot_distance": [15.0, 18.0, 14.0, 16.0, 12.0, 17.0, 15.0, 14.5, 18.5, 10.0],
#             "shots_from_free_kicks": [2, 4, 3, 2, 1, 3, 2, 2, 4, 1],
#             "touches_in_defensive_penalty_area": [5, 8, 6, 7, 4, 10, 7, 5, 9, 3],
#             "touches_in_defensive_third": [20, 30, 25, 22, 18, 28, 26, 20, 35, 15],
#             "touches_in_middle_third": [50, 80, 60, 55, 45, 70, 65, 50, 85, 40],
#             "touches_in_attacking_third": [30, 50, 35, 40, 25, 45, 40, 30, 55, 20],
#             "touches_in_attacking_penalty_area": [10, 20, 15, 12, 8, 18, 14, 11, 22, 7],
#             "live_ball_touches": [100, 150, 120, 110, 90, 140, 130, 105, 160, 80],
#             "take_ons_attempted": [10, 20, 15, 12, 8, 18, 14, 11, 22, 7],
#             "take_ons_succeeded": [7, 15, 10, 9, 6, 12, 10, 8, 16, 5],
#             "carries": [50, 80, 60, 55, 45, 70, 65, 50, 85, 40],
#             "total_carrying_distance": [300, 500, 400, 350, 250, 450, 400, 300, 550, 200],
#             "progressive_carrying_distance": [200, 350, 280, 240, 180, 320, 280, 220, 400, 150],
#             "carries_into_final_third": [10, 20, 15, 12, 8, 18, 14, 11, 22, 7],
#             "carries_into_penalty_area": [5, 10, 8, 6, 3, 9, 7, 4, 12, 2],
#             "miscontrols": [3, 5, 4, 2, 1, 4, 3, 2, 5, 1],
#             "dispossessed": [2, 4, 3, 2, 1, 3, 2, 1, 4, 1],
#             "passes_received": [50, 80, 60, 55, 45, 70, 65, 50, 85, 40],
#             "progressive_passes_received": [30, 60, 45, 35, 25, 50, 40, 30, 55, 20],
#             "tackles_won": [10, 15, 12, 11, 9, 13, 11, 10, 16, 8],
#             "defensive_third_tackles": [5, 8, 6, 7, 4, 10, 7, 5, 9, 3],
#             "middle_third_tackles": [3, 6, 5, 4, 3, 7, 5, 4, 8, 2],
#             "attacking_third_tackles": [2, 4, 3, 2, 1, 3, 2, 1, 4, 1],
#             "dribblers_tackled": [4, 8, 6, 5, 3, 7, 6, 5, 9, 3],
#             "dribbler_tackles_attempted": [6, 10, 8, 7, 5, 9, 8, 6, 11, 4],
#             "shots_blocked": [2, 4, 3, 2, 1, 4, 3, 2, 5, 1],
#             "passes_blocked": [5, 8, 6, 5, 4, 7, 6, 5, 9, 3],
#             "interceptions": [3, 5, 4, 3, 2, 6, 5, 4, 7, 2],
#             "clearances": [4, 6, 5, 4, 3, 7, 6, 4, 8, 3],
#             "errors_leading_to_shot": [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
#             "goals_against": [10, 15, 12, 11, 9, 13, 11, 10, 16, 8],
#             "shots_on_target_against": [7, 12, 10, 9, 6, 11, 10, 8, 14, 5],
#             "saves": [5, 10, 7, 6, 4, 9, 8, 6, 11, 4],
#             "clean_sheets": [3, 6, 4, 5, 2, 7, 5, 3, 8, 1],
#             "penalties_faced": [2, 4, 3, 2, 1, 4, 3, 2, 5, 1],
#             "penalties_allowed": [1, 2, 1, 1, 1, 2, 1, 1, 3, 1],
#             "penalties_saved": [0, 1, 1, 0, 0, 1, 1, 0, 2, 0],
#             "penalties_missed": [1, 1, 1, 2, 1, 2, 1, 2, 2, 1],
#             "player_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#             "minutes_played": [900, 800, 950, 1000, 870, 920, 960, 850, 890, 910],
#             "ninetys": [10, 9, 11, 11, 10, 10, 11, 9, 10, 10]
#         })

#     def test_group_stats_by_player_for_home_and_away_teams(self):
#         # Create a sample DataFrame with player statistics
#         df = self.df.copy()

#         home_team_id = 'A'
#         away_team_id = 'B'
#         home_team_squad_ids = [1, 2]

#         # Call the function to group the statistics by player for the home and away teams
#         grouped_df = group_stats_by_player_for_home_and_away_teams(df, home_team_id, away_team_id, home_team_squad_ids)

#         # Define the expected DataFrame with grouped player statistics
#         expected_grouped_df = pd.DataFrame({
#             'player_id': [1, 2, 3, 4],
#             'team_id': ['A', 'A', 'B', 'B'],
#             'goals': [2, 1, 3, 1.5],
#             'assists': [1, 0, 2, 0.5]
#         })

#         # Assert that the actual DataFrame with grouped player statistics matches the expected values
#         self.assertTrue(grouped_df.equals(expected_grouped_df), "Grouped player statistics are incorrect")

#     def test_create_per_90_stats(self):
#         # Create a sample DataFrame with statistics
#         df = pd.DataFrame({
#             'Goals': [76, 64, 52],
#             'Assists': [18, 12, 10],
#             'Shots': [200, 180, 150]
#         })

#         # Call the function to create per 90 minutes statistics
#         df_per_90 = create_per_90_stats(df, ["Goals", "Assists", "Shots"])

#         # Define the expected per 90 minutes statistics
#         expected_df_per_90 = pd.DataFrame({
#             'Goals': [2, 1.68, 1.37],
#             'Assists': [0.47, 0.32, 0.26],
#             'Shots': [5.26, 4.74, 3.95]
#         })

#         # Assert that the actual per 90 minutes statistics match the expected values
#         self.assertTrue(df_per_90.equals(expected_df_per_90), "Per 90 minutes statistics are incorrect")

#     def test_create_contribution_per_90_stats(self):
#         # Create a sample DataFrame with statistics
#         df = pd.DataFrame({
#             'goals': [10, 5, 3],
#             'assists': [2, 1, 0],
#             'minutes_played': [9, 45, 90]
#         })

#         # Call the function to create contribution per 90 minutes statistics
#         df_contribution_per_90 = create_contribution_per_90_stats(df, ['goals', 'assists', 'minutes_played'])

#         # Define the expected contribution per 90 minutes statistics
#         expected_df_contribution_per_90 = pd.DataFrame({
#             'goals': [1, 2.5, 3],
#             'assists': [0.2, 0.5, 0],
#         })

#         # Assert that the actual contribution per 90 minutes statistics match the expected values
#         self.assertTrue(df_contribution_per_90.equals(expected_df_contribution_per_90), "Contribution per 90 minutes statistics are incorrect")
    
#     def test_group_stats_by_team(self):
#         # Create a sample DataFrame with player statistics
#         df = pd.DataFrame({
#             'player_id': [1, 2, 3, 4, 5, 6],
#             'team_id': ['A', 'A', 'B', 'B', 'B', 'A'],
#             'goals': [2, 1, 3, 2, 1, 7],
#             'assists': [1, 0, 2, 1, 0, 3]
#         })

#         # Call the function to group the statistics by team
#         grouped_df = group_stats_by_team(df)

#         # Define the expected DataFrame with grouped team statistics
#         expected_grouped_df = pd.DataFrame({
#             'team_id': ['A', 'B'],
#             'goals': [10, 6],
#             'assists': [4, 3]
#         })

#         # Assert that the actual DataFrame with grouped team statistics matches the expected values
#         self.assertTrue(grouped_df.equals(expected_grouped_df), "Grouped team statistics are incorrect")

#     def test_convert_team_rows_to_single_row(self):
#         # Create a sample DataFrame with team rows
#         df = pd.DataFrame({
#             'team_id': ['A', 'B'],
#             'goals': [24, 15],
#             'assists': [6, 13]
#         })

#         # Call the function to convert team rows to a single row
#         converted_df = convert_team_rows_to_single_row(df, 'A', 'B', ['goals', 'assists'])

#         # Define the expected DataFrame with a single row representing the teams
#         expected_df = pd.DataFrame({
#             'goals': [9],
#             'assists': [-7]
#         })

#         # Assert that the actual DataFrame matches the expected values
#         self.assertTrue(converted_df.equals(expected_df), "Converted team rows are incorrect")

#     def test_combine_form_and_career_stats(self):
#         # Create sample career and form DataFrames
#         career_df = pd.DataFrame({
#             'goals': [10],
#             'assists': [2],
#             'minutes_played': [900],
#         })

#         form_df = pd.DataFrame({
#             'goals': [2],
#             'assists': [1],
#             'minutes_played': [90],
#         })

#         # Call the function to combine the career and form statistics
#         combined_df_one = combine_form_and_career_stats((career_df, form_df), pred=True, columns_to_evaluate=['goals', 'assists', "minutes_played"])

#         # Define the expected combined DataFrame
#         expected_combined_df_one = pd.DataFrame({
#             'goals': [6.8],
#             'assists': [1.6],
#             'minutes_played': [576]
#         })

#         # Assert that the actual combined DataFrame matches the expected values
#         self.assertTrue(combined_df_one.equals(expected_combined_df_one), "Combined statistics are incorrect")

class TestWinPrediction(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "season": ['2017-2018', '2017-2018', '2017-2018', '2017-2018', '2017-2018', '2018-2019', '2018-2019', '2018-2019', '2018-2019', '2018-2019'],
            "date": ['2017-09-09', '2017-10-01', '2018-01-15', '2018-03-30', '2018-04-05', '2018-09-01', '2018-10-20', '2018-12-15', '2019-02-10', '2019-03-15'],
            "home_team_id": ['t-00001', 't-00002', 't-00001', 't-00002', 't-00003', 't-00002', 't-00001', 't-00003', 't-00001', 't-00002'],
            "away_team_id": ['t-00002', 't-00003', 't-00003', 't-00001', 't-00002', 't-00001', 't-00003', 't-00002', 't-00002', 't-00003'],
            "home_goals": [2, 3, 1, 2, 4, 1, 3, 2, 1, 3],
            "away_goals": [1, 0, 2, 1, 1, 3, 0, 2, 3, 1],
            "closing_home_odds": [1.5, 2.1, 1.7, 2.5, 1.3, 3.0, 1.4, 2.2, 1.8, 2.8],
            "closing_draw_odds": [3.4, 3.6, 3.2, 3.8, 3.0, 4.0, 3.5, 3.7, 3.1, 3.9],
            "closing_away_odds": [5.5, 4.8, 5.1, 4.3, 6.0, 3.5, 5.6, 4.2, 4.7, 3.6]
        })

    def test_get_team_form(self):
        df = self.df.copy()
        teams = ['t-00001', 't-00002', 't-00003']

        df[["home_team_rolling_goal_difference", "away_team_rolling_goal_difference",
            "home_team_rolling_goal_difference_at_home","away_team_rolling_goal_difference_at_away"]] = np.nan

        for team in teams:
            data = df[(df["home_team_id"] == team)| (df["away_team_id"] == team)].copy()
            data = get_team_form(data, team)
            df.update(data)

        df[["home_team_rolling_goal_difference", "away_team_rolling_goal_difference",
            "home_team_rolling_goal_difference_at_home","away_team_rolling_goal_difference_at_away"]] = df[["home_team_rolling_goal_difference", "away_team_rolling_goal_difference",
            "home_team_rolling_goal_difference_at_home","away_team_rolling_goal_difference_at_away"]].astype(int)

        expected_df = pd.DataFrame({
            "season": ['2017-2018', '2017-2018', '2017-2018', '2017-2018', '2017-2018', '2018-2019', '2018-2019', '2018-2019', '2018-2019', '2018-2019'],
            "date": ['2017-09-09', '2017-10-01', '2018-01-15', '2018-03-30', '2018-04-05', '2018-09-01', '2018-10-20', '2018-12-15', '2019-02-10', '2019-03-15'],
            "home_team_id": ['t-00001', 't-00002', 't-00001', 't-00002', 't-00003', 't-00002', 't-00001', 't-00003', 't-00001', 't-00002'],
            "away_team_id": ['t-00002', 't-00003', 't-00003', 't-00001', 't-00002', 't-00001', 't-00003', 't-00002', 't-00002', 't-00003'],
            "home_goals": [2, 3, 1, 2, 4, 1, 3, 2, 1, 3],
            "away_goals": [1, 0, 2, 1, 1, 3, 0, 2, 3, 1],
            "closing_home_odds": [1.5, 2.1, 1.7, 2.5, 1.3, 3.0, 1.4, 2.2, 1.8, 2.8],
            "closing_draw_odds": [3.4, 3.6, 3.2, 3.8, 3.0, 4.0, 3.5, 3.7, 3.1, 3.9],
            "closing_away_odds": [5.5, 4.8, 5.1, 4.3, 6.0, 3.5, 5.6, 4.2, 4.7, 3.6],
            "home_team_rolling_goal_difference": [0, -1, 1, 2, -2, 0, 2, -3, 5, 0],
            "away_team_rolling_goal_difference": [0, 0, -3, 0, 3, 0, 0, -2, -2, -3],
            "home_team_rolling_goal_difference_at_home": [0, 0, 1, 3, 0, 0, 0, 0, 3, -2],
            "away_team_rolling_goal_difference_at_away": [0, 0, -3, 0, -1, 0, 0, 0, 0, -3]
        })

        comparison = df != expected_df
        different_rows = comparison.any(axis=1)

        expected_df_error = expected_df.loc[different_rows]
        df_error = df.loc[different_rows]

        self.assertTrue(df.equals(expected_df), "Team form statistics are incorrect\n\nExpected:\n{}\n\nActual:\n{}".format(expected_df_error, df_error))    

if __name__ == '__main__':
    unittest.main()