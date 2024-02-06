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

def get_team_name(team_id: str):
    return db.get_list(f"SELECT team_name FROM team WHERE team_id = '{team_id}'")[0][0]

def process_team_form(team, data):
  
    form_temp = data.loc[(data['home'] == team) | (data['away'] == team)]
    form_temp['is_home'] = np.where(form_temp['home'] == team, True, False)
    form_temp['goal_difference'] = np.where(form_temp['is_home'], form_temp['hg'] - form_temp['ag'], form_temp['ag'] - form_temp['hg'])
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

    # Separating the data into training and testing set
    data_train = data[data['season'] < data['season'].max()]
    latest_results = data[data['season'] == data['season'].max()]

    # Fit logistic regression models
    home_win_model = sm.formula.glm(formula="home_win ~ match_rating", data=data_train, family=sm.families.Binomial()).fit()
    draw_model = sm.formula.glm(formula="draw ~ match_rating", data=data_train, family=sm.families.Binomial()).fit()
    away_win_model = sm.formula.glm(formula="away_win ~ match_rating", data=data_train, family=sm.families.Binomial()).fit()

    teams = [home_team_id, away_team_id]
    form = pd.concat([process_team_form(team, latest_results) for team in teams], ignore_index=True)

    # Loading fixture
    home_team_name = get_team_name(home_team_id)
    away_team_name = get_team_name(away_team_id)

    fixture = (pd.read_csv('https://www.football-data.co.uk/fixtures.csv')
                .rename(columns=lambda x: x.lower())
                .query(f'div == "E0" and hometeam == {home_team_name} and awayteam == {away_team_name}')
                .rename(columns={'hometeam': 'home', 'awayteam': 'away', 'psh': 'home_odds', 'psd': 'draw_odds', 'psa': 'away_odds'})
            )

    sample_date = fixture.iloc[0]['date']
    print(pd.to_datetime(sample_date, infer_datetime_format=True))

    fixture = fixture[['date', 'time', 'home', 'away', 'home_odds', 'draw_odds', 'away_odds']]

    form_home = form[form['is_home'] == True].rename(columns={'team': 'home', 'gd_form_lagged': 'gd_form_home'}).drop(columns=['is_home'])
    form_away = form[form['is_home'] == False].rename(columns={'team': 'away', 'gd_form_lagged': 'gd_form_away'}).drop(columns=['is_home'])

    fixture = pd.merge(fixture, form_home, on='home', how='left')
    fixture = pd.merge(fixture, form_away, on='away', how='left')

    fixture['match_rating'] = fixture['gd_form_home'] - fixture['gd_form_away']

    # Predict probabilities for each outcome
    fixture['home_win_prob'] = home_win_model.predict(fixture)
    fixture['draw_prob'] = draw_model.predict(fixture)
    fixture['away_win_prob'] = away_win_model.predict(fixture)

    print(fixture.tail())

    fixture_enriched = fixture.loc[fixture['match_rating'].notna()].copy()
    fixture_enriched['fair_h'] = 1 / fixture_enriched['home_win_prob']
    fixture_enriched['fair_d'] = 1 / fixture_enriched['draw_prob']
    fixture_enriched['fair_a'] = 1 / fixture_enriched['away_win_prob']
    fixture_enriched['value_h'] = (fixture_enriched['home_odds'] - fixture_enriched['fair_h']) / fixture_enriched['fair_h']
    fixture_enriched['value_d'] = (fixture_enriched['draw_odds'] - fixture_enriched['fair_d']) / fixture_enriched['fair_d']
    fixture_enriched['value_a'] = (fixture_enriched['away_odds'] - fixture_enriched['fair_a']) / fixture_enriched['fair_a']
    fixture_enriched.drop(columns=['gd_form_home', 'gd_form_away', 'home_win_prob', 'draw_prob', 'away_win_prob'], inplace=True)
    fixture_enriched.rename(columns={'date': 'Date', 'time': 'Time', 'home': 'Home', 'away': 'Away', 'home_odds': 'HomeOdds', 'draw_odds': 'DrawOdds', 'away_odds': 'AwayOdds', 'fair_h': 'FairHomeOdds', 'fair_d': 'FairDrawOdds', 'fair_a': 'FairAwayOdds', 'match_rating': 'MatchRating', 'value_h': 'HomeValue', 'value_d': 'DrawValue', 'value_a': 'AwayValue'}, inplace=True)
    fixture_enriched[['MatchRating', 'FairHomeOdds', 'FairDrawOdds', 'FairAwayOdds', 'HomeValue', 'DrawValue', 'AwayValue']] = fixture_enriched[['MatchRating', 'FairHomeOdds', 'FairDrawOdds', 'FairAwayOdds', 'HomeValue', 'DrawValue', 'AwayValue']].round(2)

    fixture_enriched[['Date', 'Home', 'Away', 'HomeOdds', 'DrawOdds', 'AwayOdds', 'HomeValue', 'DrawValue', 'AwayValue']]
    return fixture_enriched

