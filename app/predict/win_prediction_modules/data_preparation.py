# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 23:00:11 2023

@author: antoinejwmartin
"""

import pandas as pd
from functools import partial
import numpy as np
from db_connection import SQLConnection
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), "localhost" or os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

def get_team_form(sql_connection, team_id: str, is_home: bool, match_id: str = "") -> float:
    try:
        if match_id:
            date = sql_connection.get_list(f"SELECT date FROM match WHERE id = '{match_id}'")[0][0]
        else:
            date = datetime.now().strftime("%Y-%m-%d")
        home_or_away_form_data = sql_connection.get_df(f"SELECT id, season, date, home_team_id, away_team_id, home_goals, away_goals FROM match WHERE {'home_team_id =' if is_home else 'away_team_id ='} '{team_id}' AND date <= '{date}' ORDER BY date DESC LIMIT 5")
        overall_form = sql_connection.get_df(f"SELECT id, season, date, home_team_id, away_team_id, home_goals, away_goals FROM match WHERE home_team_id = '{team_id}' OR away_team_id = '{team_id}' AND date <= '{date}' ORDER BY date DESC LIMIT 5")

        # Show the form for the last 5 home or away matches for a team, depending if they are home or away for the current match
        home_or_away_mean_goal_difference = (home_or_away_form_data["home_goals"].sum() - home_or_away_form_data["away_goals"].sum())/5 if is_home else (home_or_away_form_data["away_goals"].sum() - home_or_away_form_data["home_goals"].sum())/5
        # Show the form for the last 5 matches for a team, regardless of whether they are home or away for the current match
        overall_mean_goal_difference = ((overall_form.loc[overall_form["home_team_id"] == team_id, "home_goals"].sum() + overall_form.loc[overall_form["away_team_id"] == team_id, "away_goals"].sum()) - (overall_form.loc[overall_form["home_team_id"] != team_id, "home_goals"].sum() + overall_form.loc[overall_form["away_team_id"] != team_id, "away_goals"].sum()))/5
        return home_or_away_mean_goal_difference, overall_mean_goal_difference
    except Exception as e:
        raise e

def get_last_five_head_to_head_matches(sql_connection, home_team_id: str, away_team_id: str, match_id: str = "") -> pd.DataFrame:
    try:
        if match_id:
            date = sql_connection.get_list(f"SELECT date FROM match WHERE id = '{match_id}'")[0][0]
        else:
            date = datetime.now().strftime("%Y-%m-%d")
        # The more negative the value, the better the away team has performed w.r.t the home team in the last 5 head-to-head matches
        data = sql_connection.get_df(f"SELECT id, season, date, home_team_id, away_team_id, home_goals, away_goals FROM match WHERE ((home_team_id = '{home_team_id}' AND away_team_id = '{away_team_id}') OR (home_team_id = '{away_team_id}' AND away_team_id = '{home_team_id}')) AND date <= '{date}' ORDER BY date DESC LIMIT 5")
        head_to_head_goal_difference = (data.loc[data["home_team_id"] == home_team_id, "home_goals"].sum() + data.loc[data["away_team_id"] == home_team_id, "away_goals"].sum()) - (data.loc[data["home_team_id"] == away_team_id, "home_goals"].sum() + data.loc[data["away_team_id"] == away_team_id, "away_goals"].sum())
        return head_to_head_goal_difference
    except Exception as e:
        raise e

# Process form for all teams
def run_data_prep():

    match_columns = ["season","date","home_team_id","away_team_id","home_goals","away_goals","closing_home_odds","closing_draw_odds","closing_away_odds"]
    data = db.get_df(f"SELECT {', '.join(match_columns)} FROM match")
    print("Loaded match data successfully")
    print(data.head().to_markdown())
    print("--- --- --- --- ---")

    teams = data["home_team_id"].unique().tolist()
    process_team_form_partial = partial(process_team_form, data=data)
    form = pd.concat(map(process_team_form_partial, teams), ignore_index=True)

    # Add each team's form to the main database
    data = data.merge(form.rename(columns={'team': 'home_team_id', 'gd_form_lagged': 'gd_form_home'}), on=['home_team_id', 'season', 'date'], how='left')
    data = data.merge(form.rename(columns={'team': 'away_team_id', 'gd_form_lagged': 'gd_form_away'}), on=['away_team_id', 'season', 'date'], how='left')

    data['match_rating'] = data['gd_form_home'] - data['gd_form_away']
    data['full_time_result'] = np.where(data['home_goals'] > data['away_goals'], 'H', np.where(data['away_goals'] > data['home_goals'], 'A', 'D'))

    data['home_win'] = (data['full_time_result'] == 'H').astype(int)
    data['draw'] = (data['full_time_result'] == 'D').astype(int)
    data['away_win'] = (data['full_time_result'] == 'A').astype(int)

    # data = data.drop(columns=["full_time_result"])

    data = add_head_to_head(data)

    print(data.tail().to_markdown())
    data.to_csv('match_and_form_data.csv', index=False)