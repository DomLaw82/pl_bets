import pandas as pd
import numpy as np
from db_connection import SQLConnection
from collections import deque
import os
from dotenv import load_dotenv

load_dotenv()

rolling_window = int(os.environ.get("ROLLING_WINDOW"))

def get_rolling_goal_difference(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Sum the last n non-null values in a DataFrame
    """
    home_goal_diff = df["home_team_goal_difference"].values
    away_goal_diff = df["away_team_goal_difference"].values
    is_home = df["is_home"].values

    values = deque(maxlen=n)
    at_home_values = deque(maxlen=n)
    at_away_values = deque(maxlen=n)

    result = np.full(len(df), np.nan)
    at_home_result = np.full(len(df), np.nan)
    at_away_result = np.full(len(df), np.nan)

    for i in range(len(df)):
        if is_home[i]:
            if pd.notnull(home_goal_diff[i]):
                values.append(home_goal_diff[i])
                at_home_values.append(home_goal_diff[i])
                at_home_result[i] = sum(at_home_values)
        else:
            if pd.notnull(away_goal_diff[i]):
                values.append(away_goal_diff[i])
                at_away_values.append(away_goal_diff[i])
                at_away_result[i] = sum(at_away_values)

        result[i] = sum(values)

    result = np.concatenate(([0], result[:-1]))
    at_home_result = np.concatenate(([0], at_home_result[:-1]))
    at_away_result = np.concatenate(([0], at_away_result[:-1]))

    return pd.DataFrame({
        "home_team_rolling_goal_difference": np.where(is_home, result, np.nan),
        "away_team_rolling_goal_difference": np.where(~is_home, result, np.nan),
        "home_team_rolling_goal_difference_at_home": at_home_result,
        "away_team_rolling_goal_difference_at_away": at_away_result
    }, index=df.index)

def get_team_form(df: pd.DataFrame, team_id: str) -> float:
    """
    Calculate the form of a team based on the last 5 matches:
        - home_team_rolling_goal_difference
        - away_team_rolling_goal_difference
        - home_team_rolling_goal_difference_at_home
        - away_team_rolling_goal_difference_at_away
    """
    try:
        for season, season_data in df.groupby('season'):
            season_data = season_data.copy()
            season_data.loc[:, "is_home"] = season_data["home_team_id"] == team_id

            season_data["home_team_goal_difference"] = np.where(season_data["is_home"], season_data["home_goals"] - season_data["away_goals"], np.nan)
            season_data["away_team_goal_difference"] = np.where(~season_data["is_home"], season_data["away_goals"] - season_data["home_goals"], np.nan)

            df.update(
                get_rolling_goal_difference(
                    season_data[["is_home", "home_team_goal_difference", "away_team_goal_difference"]], rolling_window
                )
            )
        return df
    except Exception as e:
        raise e

def get_last_five_head_to_head_matches_rolling_goal_difference(data: pd.DataFrame) -> pd.DataFrame:
    try:
        data["h2h_rolling_goal_difference"] = (data["home_goals"] - data["away_goals"]).rolling(rolling_window, min_periods=1).sum().shift(1).fillna(0)
        return data
    except Exception as e:
        raise e
    
def add_historic_head_to_head_results(data: pd.DataFrame) -> pd.DataFrame:

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

# Process form for all teams
def run_data_prep(sql_connection: SQLConnection):

    match_columns = ["season","date","home_team_id","away_team_id","home_goals","away_goals","closing_home_odds","closing_draw_odds","closing_away_odds"]
    data = sql_connection.get_df(f"SELECT {', '.join(match_columns)} FROM match ORDER BY date ASC")
    print("Loaded match data successfully")

    teams = data["home_team_id"].unique().tolist()

    data[["home_team_rolling_goal_difference", "away_team_rolling_goal_difference",
            "home_team_rolling_goal_difference_at_home","away_team_rolling_goal_difference_at_away"]] = np.nan

    for team in teams:
        print(f"Processing form for {team}")
        df = data[(data["home_team_id"] == team)| (data["away_team_id"] == team)].copy()
        df = get_team_form(df, team)
        data.update(df)

    data['full_time_result'] = np.where(data['home_goals'] > data['away_goals'], 'H', np.where(data['away_goals'] > data['home_goals'], 'A', 'D'))

    data['home_win'] = (data['full_time_result'] == 'H').astype(int)
    data['draw'] = (data['full_time_result'] == 'D').astype(int)
    data['away_win'] = (data['full_time_result'] == 'A').astype(int)

    data = data.drop(columns=["full_time_result"])

    data = add_historic_head_to_head_results(data)

    print(data.head())
    print(data.tail())

    data.to_csv('match_and_form_data.csv', index=False)