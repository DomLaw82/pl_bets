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

load_dotenv()

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

# Create team form
def process_team_form(team_id, data):

    form_temp = data[(data['home_team_id'] == team_id) | (data['away_team_id'] == team_id)].copy()
    form_temp['is_home'] = form_temp['home_team_id'] == team_id
    form_temp['goal_difference'] = form_temp.apply(lambda row: row['home_goals'] - row['away_goals'] if row['is_home'] else row['away_goals'] - row['home_goals'], axis=1)
    form_temp = form_temp[['season', 'date', 'is_home', 'goal_difference']]

    form_temp = form_temp.groupby('season').filter(lambda x: len(x) >= 6)

    form_temp_home = form_temp[form_temp['is_home']].copy()
    form_temp_home['gd_form'] = form_temp_home['goal_difference'].rolling(window=6).mean() # 6 game rolling average, change to sum?
    form_temp_home['gd_form_lagged'] = form_temp_home['gd_form'].shift(1)
    form_temp_home = form_temp_home[['season', 'date', 'gd_form_lagged']]

    form_temp_away = form_temp[~form_temp['is_home']].copy()
    form_temp_away['gd_form'] = form_temp_away['goal_difference'].rolling(window=6).mean()
    form_temp_away['gd_form_lagged'] = form_temp_away['gd_form'].shift(1)
    form_temp_away = form_temp_away[['season', 'date', 'gd_form_lagged']]

    form = pd.concat([form_temp_home, form_temp_away])
    form['team'] = team_id
    form = form.sort_values(by=['season', 'date'])

    return form

# Process form for all teams
def run_data_prep():

    match_columns = ["season","date","home_team_id","away_team_id","home_goals","away_goals","closing_home_odds","closing_draw_odds","closing_away_odds"]
    data = db.get_df(f"SELECT {match_columns.join(', ')} FROM match")
    print(data.tail())

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

    print(data.tail())
    data.to_csv('match_and_form_data.csv', index=False)