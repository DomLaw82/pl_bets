# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 13:57:43 2023

@author: antoinejwmartin
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from db_connection import local_pl_stats_connector as db
from fuzzywuzzy import process

def find_most_similar(player, options):
    result, score = process.extractOne(player, options)
    return result, score

def get_team_id(connector, team_name: str) -> str:
    team_name = team_name.replace("'", " ")

    # Fetch data from the database for comparison
    database_data = connector.get_list(f"SELECT id, name FROM team")

    team_names = [pair[1] for pair in database_data]
    best_match = find_most_similar(team_name, team_names)

    if best_match:
        return [pair[0] for pair in database_data if pair[1] == best_match[0]][0]  # Assuming the first column is id
    else:
        return None

def get_team_name(team_id: str):
    return db.get_list(f"SELECT name FROM team WHERE id = '{team_id}'")[0][0]

def process_team_form(team, data):
  
    form_temp = data.loc[(data['home'] == team) | (data['away'] == team)]
    form_temp['is_home'] = np.where(form_temp['home'] == team, True, False)
    form_temp['goal_difference'] = np.where(form_temp['is_home'], form_temp['home_goals'] - form_temp['away_goals'], form_temp['away_goals'] - form_temp['home_goals'])
    form_temp = form_temp.loc[:, ['date', 'is_home', 'goal_difference']]
    form_temp = form_temp.loc[form_temp.groupby('is_home').cumcount() >= 5]
  
    form_temp_home = form_temp.loc[form_temp['is_home']].copy()
    form_temp_home['gd_form'] = form_temp_home['goal_difference'].rolling(window=6, min_periods=6).mean()
    form_temp_home['gd_form_lagged'] = form_temp_home['gd_form'].shift(1)
    form_temp_home = form_temp_home.loc[:, ['gd_form_lagged', 'is_home']].tail(n=1)
  
    form_temp_away = form_temp.loc[~form_temp['is_home']].copy()
    form_temp_away['gd_form'] = form_temp_away['goal_difference'].rolling(window=6, min_periods=6).mean()
    form_temp_away['gd_form_lagged'] = form_temp_away['gd_form'].shift(1)
    form_temp_away = form_temp_away.loc[:, ['gd_form_lagged', 'is_home']].tail(n=1)
  
    form = pd.concat([form_temp_home, form_temp_away], ignore_index=True)
    form['team'] = team
  
    return form


def predict_fixture_outcome_odds(data: pd.DataFrame, home_team_id: str, away_team_id: str) -> pd.DataFrame:
    data = data.rename(columns={"home_team_id": "home", "away_team_id": "away"})
    # Separating the data into training and testing set
    data_train = data[data['season'] < data['season'].max()]
    latest_results = data[data['season'] == data['season'].max()]

    # Fit logistic regression models
    home_win_model = sm.formula.glm(formula="home_win ~ match_rating", data=data_train, family=sm.families.Binomial()).fit()
    draw_model = sm.formula.glm(formula="draw ~ match_rating", data=data_train, family=sm.families.Binomial()).fit()
    away_win_model = sm.formula.glm(formula="away_win ~ match_rating", data=data_train, family=sm.families.Binomial()).fit()

    teams = [home_team_id, away_team_id] if home_team_id and away_team_id else data['home'].unique()
    form = pd.concat([process_team_form(team, latest_results) for team in teams], ignore_index=True)

    # Loading fixtures
    home_team_name = ""
    away_team_name = ""
    query = 'div == "E0"'

    if home_team_id and away_team_id:
        home_team_name = get_team_name(home_team_id)
        away_team_name = get_team_name(away_team_id)
        query += f' and hometeam == "{home_team_name}" and awayteam == "{away_team_name}"'

    fixtures = (pd.read_csv('https://www.football-data.co.uk/fixtures.csv')
                .rename(columns=lambda x: x.lower())
                .query(query)
                .rename(columns={'hometeam': 'home', 'awayteam': 'away', 'psh': 'home_odds', 'psd': 'draw_odds', 'psa': 'away_odds'})
            )
    
    if home_team_id and away_team_id:
        fixtures["home"] = home_team_id
        fixtures["away"] = away_team_id
    else:
        fixtures["home"] = fixtures["home"].apply(lambda x: get_team_id(db, x))
        fixtures["away"] = fixtures["away"].apply(lambda x: get_team_id(db, x))

    sample_date = fixtures.iloc[0]['date']
    print(pd.to_datetime(sample_date))

    fixtures = fixtures[['date', 'time', 'home', 'away', 'home_odds', 'draw_odds', 'away_odds']]

    form_home = form[form['is_home'] == True].rename(columns={'team': 'home', 'gd_form_lagged': 'gd_form_home'}).drop(columns=['is_home'])
    form_away = form[form['is_home'] == False].rename(columns={'team': 'away', 'gd_form_lagged': 'gd_form_away'}).drop(columns=['is_home'])

    fixtures = pd.merge(fixtures, form_home, on='home', how='left')
    fixtures = pd.merge(fixtures, form_away, on='away', how='left')

    fixtures['match_rating'] = fixtures['gd_form_home'] - fixtures['gd_form_away']

    # Predict probabilities for each outcome
    fixtures['home_win_prob'] = home_win_model.predict(fixtures)
    fixtures['draw_prob'] = draw_model.predict(fixtures)
    fixtures['away_win_prob'] = away_win_model.predict(fixtures)

    print(fixtures.tail())

    fixtures_enriched = fixtures.loc[fixtures['match_rating'].notna()].copy()
    fixtures_enriched['fair_h'] = 1 / fixtures_enriched['home_win_prob']
    fixtures_enriched['fair_d'] = 1 / fixtures_enriched['draw_prob']
    fixtures_enriched['fair_a'] = 1 / fixtures_enriched['away_win_prob']
    fixtures_enriched['value_h'] = (fixtures_enriched['home_odds'] - fixtures_enriched['fair_h']) / fixtures_enriched['fair_h']
    fixtures_enriched['value_d'] = (fixtures_enriched['draw_odds'] - fixtures_enriched['fair_d']) / fixtures_enriched['fair_d']
    fixtures_enriched['value_a'] = (fixtures_enriched['away_odds'] - fixtures_enriched['fair_a']) / fixtures_enriched['fair_a']
    fixtures_enriched.drop(columns=['gd_form_home', 'gd_form_away', 'home_win_prob', 'draw_prob', 'away_win_prob'], inplace=True)
    fixtures_enriched.rename(columns={'date': 'Date', 'time': 'Time', 'home': 'Home', 'away': 'Away', 'home_odds': 'HomeOdds', 'draw_odds': 'DrawOdds', 'away_odds': 'AwayOdds', 'fair_h': 'FairHomeOdds', 'fair_d': 'FairDrawOdds', 'fair_a': 'FairAwayOdds', 'match_rating': 'MatchRating', 'value_h': 'HomeValue', 'value_d': 'DrawValue', 'value_a': 'AwayValue'}, inplace=True)
    fixtures_enriched[['MatchRating', 'FairHomeOdds', 'FairDrawOdds', 'FairAwayOdds', 'HomeValue', 'DrawValue', 'AwayValue']] = fixtures_enriched[['MatchRating', 'FairHomeOdds', 'FairDrawOdds', 'FairAwayOdds', 'HomeValue', 'DrawValue', 'AwayValue']].round(2)

    fixtures_enriched[['Date', 'Home', 'Away', 'HomeOdds', 'DrawOdds', 'AwayOdds', 'HomeValue', 'DrawValue', 'AwayValue']]
    return fixtures_enriched

