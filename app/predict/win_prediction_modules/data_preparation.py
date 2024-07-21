import pandas as pd
import numpy as np
from db_connection import SQLConnection
from collections import deque
import os
from dotenv import load_dotenv

load_dotenv()

rolling_window = int(os.environ.get("ROLLING_WINDOW"))
# TODO: NEW FEATURES - mean_goals_for, mean_goals_against,
#                    - home_team_in_europe, away_team_in_europe
# TODO: Consider how features change over time (e.g., recent team performance, fatigue)
# TODO: Identify and handle outliers in your data, as they can significantly impact model performance.

def get_rolling_stat(df: pd.DataFrame, stat: str, n: int) -> pd.DataFrame:
    """
    Calculate the rolling stat for each team in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the data.
    - n (int): The number of previous non-null values to consider for the rolling sum.

    Returns:
    - pd.DataFrame: A DataFrame with the rolling stat for each team.

    Notes:
    - The rolling stat is calculated separately for the home and away teams.
    - The rolling stat is the sum of the last `n` non-null stats for each team.
    - If a team has less than `n` non-null stats available, the rolling stat will be NaN for those periods.
    - The resulting DataFrame will have two columns: "home_rolling_{stat}_at_home" and "away_rolling_{stat}_at_away".
    - The index of the resulting DataFrame will be the same as the input DataFrame.
    """

    home_goal_diff = df[f"home_{stat}"].values
    away_goal_diff = df[f"away_{stat}"].values
    is_home = df["is_home"].values

    values = deque(maxlen=n)

    result = np.full(len(df), np.nan)

    for i in range(len(df)):
        if is_home[i]:
            if pd.notnull(home_goal_diff[i]):
                values.append(home_goal_diff[i])
        else:
            if pd.notnull(away_goal_diff[i]):
                values.append(away_goal_diff[i])

        result[i] = sum(values)
    
    result = np.concatenate(([0], result[:-1]))

    return pd.DataFrame({
        f"home_rolling_{stat}": np.where(is_home, result, np.nan),
        f"away_rolling_{stat}": np.where(~is_home, result, np.nan),
    }, index=df.index)

def get_rolling_goal_difference_at_location(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Calculates the rolling goal difference at a specific location (home or away) for each team in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing match data.
        n (int): The number of previous matches to consider for calculating the rolling goal difference.

    Returns:
        pd.DataFrame: A DataFrame with two columns:
            - 'home_rolling_goal_difference_at_home': Rolling goal difference at home for each match.
            - 'away_rolling_goal_difference_at_away': Rolling goal difference away for each match.

    Example:
        df = pd.DataFrame({
            'is_home': [True, False, True, False, True],
            'home_goal_difference': [1, -2, 3, 0, -1],
            'away_goal_difference': [-1, 0, 2, -3, 1]
        })
        result = get_rolling_goal_difference_at_location(df, 3)
        print(result)

        Output:
            home_rolling_goal_difference_at_home  away_rolling_goal_difference_at_away
        0                                          NaN                                      NaN
        1                                          NaN                                      NaN
        2                                          4.0                                      NaN
        3                                          1.0                                      NaN
        4                                          2.0                                      1.0
    """
    is_home = df["is_home"].values

    at_home_values = deque(maxlen=n)
    at_away_values = deque(maxlen=n)

    at_home_result = np.full(len(df[df["is_home"]]), np.nan)
    at_away_result = np.full(len(df[~df["is_home"]]), np.nan)

    home_df = df[df["is_home"]].copy()
    away_df = df[~df["is_home"]].copy()
    
    home_df_home_diff = home_df["home_goal_difference"].values
    away_df_away_diff = away_df["away_goal_difference"].values

    at_home_result_indices = home_df.index.values
    at_away_result_indices = away_df.index.values

    for i in range(len(home_df)):
        if pd.notnull(home_df_home_diff[i]):
            at_home_values.append(home_df_home_diff[i])
            at_home_result[i] = sum(at_home_values)
    
    for i in range(len(away_df)):
        if pd.notnull(away_df_away_diff[i]):
            at_away_values.append(away_df_away_diff[i])
            at_away_result[i] = sum(at_away_values)

    at_home_result = np.concatenate(([0], at_home_result[:-1]))
    at_away_result = np.concatenate(([0], at_away_result[:-1]))

    at_home_combined = list(zip(at_home_result_indices, at_home_result))
    at_away_combined = list(zip(at_away_result_indices, at_away_result))

    at_location_combined = at_home_combined + at_away_combined

    at_location_combined_sorted = sorted(at_location_combined, key=lambda x: x[0])

    at_location_indices, at_location_values = zip(*at_location_combined_sorted)

    at_location_indices = list(at_location_indices)
    at_location_values = list(at_location_values)

    return pd.DataFrame({
        "home_rolling_goal_difference_at_home": np.where(is_home, at_location_values, np.nan),
        "away_rolling_goal_difference_at_away": np.where(~is_home, at_location_values, np.nan),
    }, index=df.index)

def get_team_form(df: pd.DataFrame, team_id: str) -> pd.DataFrame:
    """
    Calculate the form of a team based on the last 5 matches:
        - home_rolling_goal_difference
        - away_rolling_goal_difference
        - home_rolling_goal_difference_at_home
        - away_rolling_goal_difference_at_away
        - home_rolling_shots_on_target
        - away_rolling_shots_on_target

    Args:
        df (pd.DataFrame): The DataFrame containing the match data.
        team_id (str): The ID of the team for which to calculate the form.

    Returns:
        pd.DataFrame: The dataframe with the calculated columns

    """
    try:
        for season, season_data in df.groupby('season'):
            season_data = season_data.copy()
            season_data.loc[:, "is_home"] = season_data["home_team_id"] == team_id

            season_data["home_goal_difference"] = np.where(season_data["is_home"], season_data["home_goals"] - season_data["away_goals"], np.nan)
            season_data["away_goal_difference"] = np.where(~season_data["is_home"], season_data["away_goals"] - season_data["home_goals"], np.nan)
            
            df.update(
                get_rolling_stat(
                    season_data[["is_home", "home_goal_difference", "away_goal_difference"]], "goal_difference", rolling_window
                )
            )
            df.update(
                get_rolling_goal_difference_at_location(
                    season_data[["is_home", "home_goal_difference", "away_goal_difference"]], rolling_window
                )
            )
            # df.update(
            #     get_rolling_stat(
            #         season_data[["is_home", "home_shots_on_target", "away_shots_on_target"]], "shots_on_target", rolling_window
            #     )
            # )

        return df
    except Exception as e:
        raise e

def get_last_five_head_to_head_matches_rolling_goal_difference(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the rolling goal difference for the last five head-to-head matches.

    Args:
        data (pd.DataFrame): The input DataFrame containing the match data.

    Returns:
        pd.DataFrame: The input DataFrame with an additional column 'h2h_rolling_goal_difference' 
                      representing the rolling goal difference for the last five head-to-head matches.

    """
    try:
        data["h2h_rolling_goal_difference"] = (data["home_goals"] - data["away_goals"]).rolling(rolling_window, min_periods=1).sum().shift(1).fillna(0)
        return data
    except Exception as e:
        raise e
    
def add_historic_head_to_head_results(data: pd.DataFrame) -> pd.DataFrame:
    """
    Adds historic head-to-head results to the given DataFrame.
    - h2h_home_wins: The number of home wins in the head-to-head matches.
    - h2h_draws: The number of draws in the head-to-head matches.
    - h2h_away_wins: The number of away wins in the head-to-head matches.
    - h2h_rolling_goal_difference: The rolling goal difference for the last five head-to-head matches.

    Args:
        data (pd.DataFrame): The DataFrame containing the match data.

    Returns:
        pd.DataFrame: The DataFrame with the added historic head-to-head results.
    """

    data["h2h_home_wins"] = np.nan
    data["h2h_draws"] = np.nan
    data["h2h_away_wins"] = np.nan
    data["h2h_rolling_goal_difference"] = np.nan

    for teams, matches in data.groupby(["home_team_id", "away_team_id"]):
        home_team_id, away_team_id = teams
        
        matches["h2h_home_wins"] = matches["home_win"].cumsum().shift(1).fillna(0)
        matches["h2h_draws"] = matches["draw"].cumsum().shift(1).fillna(0)
        matches["h2h_away_wins"] = matches["away_win"].cumsum().shift(1).fillna(0)

        matches = get_last_five_head_to_head_matches_rolling_goal_difference(matches)

        data.update(matches)

    return data

def get_days_since_last_league_game(data: pd.DataFrame, team_id: str) -> pd.DataFrame:
    """
    Calculate the number of days since the last league game for a team

    Args:
        data (pd.DataFrame): The input DataFrame containing the match data
        team_id (str): The ID of the team for which to calculate the days since the last league game

    Returns:
        pd.DataFrame: The updated DataFrame with the added columns for days since the last league game

    """
    try:

        for season, season_data in data.groupby('season'):

            season_data = season_data.copy()
            season_data["is_home"] = season_data["home_team_id"] == team_id

            match_differences = pd.to_datetime(season_data["date"], format="%Y-%m-%d").diff().dt.days.fillna(0).values

            season_data["home_days_since_last_league_game"] = np.where(season_data["is_home"], match_differences, np.nan)
            season_data["away_days_since_last_league_game"] = np.where(~season_data["is_home"], match_differences, np.nan)

            data.update(season_data)

        return data
    except Exception as e:
        raise e

# Process form for all teams
def run_data_prep(sql_connection: SQLConnection, features: list, fixtures: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
    """
    Runs the data preparation process for predicting match outcomes.

    Args:
        sql_connection (SQLConnection): An instance of the SQLConnection class for connecting to the database.
        features (list): A list of features to be added to the dataset.
        fixtures (pd.DataFrame, optional): A DataFrame containing fixture data, to add fixtures for weekly prediction. Defaults to an empty DataFrame.

    Returns:
        pd.DataFrame: The prepared dataset with added features.

    """
    match_columns = ["season","date","home_team_id","away_team_id","home_goals","away_goals", "home_shots_on_target", "away_shots_on_target", "closing_home_odds","closing_draw_odds","closing_away_odds"]
    model_features = ["home_rolling_goal_difference", "away_rolling_goal_difference", "home_rolling_goal_difference_at_home","away_rolling_goal_difference_at_away",
                    #   "home_rolling_shots_on_target", "away_rolling_shots_on_target"
                    ]
    
    data = sql_connection.get_df(f"SELECT {', '.join(match_columns)} FROM match ORDER BY date ASC")

    teams = data["home_team_id"].unique().tolist()

    data[features] = np.nan

    if not fixtures.empty:
        data = pd.concat([data, fixtures], ignore_index=True)

    for team in teams:
        df = data[(data["home_team_id"] == team)| (data["away_team_id"] == team)].copy()
        df = get_team_form(df, team)
        df = get_days_since_last_league_game(df, team)
        data.update(df)

    data[model_features] = data[model_features].astype(int)

    return data