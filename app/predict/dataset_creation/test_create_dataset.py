import pandas as pd
from create_dataset import get_all_players_in_match



test_get_all_players_in_match()
import pandas as pd
from create_dataset import group_stats_by_player_for_home_and_away_teams



# Run the test
test_group_stats_by_player_for_home_and_away_teams()

import pandas as pd
from create_dataset import create_per_90_stats

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

# Run the test
test_create_per_90_stats()
import pandas as pd
from create_dataset import create_contribution_per_90_stats

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

# Run the test
test_create_contribution_per_90_stats()

import pandas as pd
from create_dataset import group_stats_by_team

def test_group_stats_by_team():
    # Create a sample DataFrame with player statistics
    df = pd.DataFrame({
        'player_id': [1, 2, 3, 4, 5],
        'team_id': ['A', 'A', 'B', 'B', 'C'],
        'goals': [2, 1, 3, 2, 1],
        'assists': [1, 0, 2, 1, 0]
    })

    # Call the function to group the statistics by team
    df_grouped = group_stats_by_team(df)

    # Define the expected DataFrame with team statistics
    expected_df_grouped = pd.DataFrame({
        'team_id': ['A', 'B', 'C'],
        'goals': [3, 5, 1],
        'assists': [1, 3, 0]
    })

    # Assert that the actual DataFrame with team statistics matches the expected values
    assert df_grouped.equals(expected_df_grouped), "Grouped team statistics are incorrect"

# Run the test
test_group_stats_by_team()

import pandas as pd
from create_dataset import convert_team_rows_to_single_row

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

# Run the test
test_convert_team_rows_to_single_row()

import pandas as pd
from create_dataset import convert_team_rows_to_single_row



# Run the test
test_convert_team_rows_to_single_row()