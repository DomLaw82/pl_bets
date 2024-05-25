# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 23:04:59 2023

@author: antoinejwmartin
"""

# TODO: Consider features like team form, head-to-head records, home-field advantage
# TODO: Consider how features change over time (e.g., recent team performance, fatigue)
# TODO: Identify and handle outliers in your data, as they can significantly impact model performance.

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t, norm
from plotting_functions import plot_coefficients, plot_match_rating_distribution, plot_probability_by_match_rating

with_mean_gd_form = {
    'bets': [294],
    'win_rate': [0.5816326530612245],
    'profit': [11.935339467119459],
    'ror': [0.04059639274530428],
    'odds': [3.0655808815443097],
    'value': [0.7718755269602725],
    'pvalue': [0.3159623010639926]}


# Calculate sum_gd_form_home and sum_gd_form_away

pd.set_option('display.max_columns', None)

# Set up our working directory
def run_data_modelling_part_one_logistic_regression(data: pd.DataFrame, closing_odds_column_prefix: str = "closing_") -> dict: 
    """Runs the first part of the data modelling process."""

    # Separating the data into training and testing set
    data_train = data[data['season'] < data['season'].max()]
    data_test = data[data['season'] == data['season'].max()]

    # Drop rows with NaN values
    data_train = data_train.dropna(subset=['match_rating'])

    outcome_labels = ['home_win', 'draw', 'away_win']

    # Model Training
    match_rating_models = {}
    enhanced_models = {}

    match_rating_column = ['match_rating']
    feature_columns = ['match_rating', 'gd_form_home', 'gd_form_away', 'h2h_home_wins','h2h_draws','h2h_away_wins']

    for outcome in outcome_labels:
        match_rating_formula = f"{outcome} ~ " + " + ".join(match_rating_column)
        enhanced_formula = f"{outcome} ~ " + " + ".join(feature_columns)

        match_rating_model = smf.glm(match_rating_formula, data=data_train, family=sm.families.Binomial()).fit()
        enhanced_model = smf.glm(enhanced_formula, data=data_train, family=sm.families.Binomial()).fit()

        match_rating_models[outcome] = match_rating_model
        enhanced_models[outcome] = enhanced_model

    # Predict probabilities for each outcome
    data_test_match_rating = data_test.copy()
    data_test_enhanced = data_test.copy()

    for outcome in outcome_labels:

        data_test_match_rating[f"{outcome}_prob"] = match_rating_models[outcome].predict(data_test_match_rating[feature_columns])
        data_test_enhanced[f"{outcome}_prob"] = enhanced_models[outcome].predict(data_test_enhanced[feature_columns])

    # Plotting(data_test, models, outcome_labels)
    plot_coefficients(enhanced_models, outcome_labels)
    plot_match_rating_distribution(data_test_match_rating, outcome_labels)
    plot_probability_by_match_rating(data_test_match_rating, match_rating_models, outcome_labels)

    # Calculate and return the results for enhanced model
    data_test_enriched = data_test_enhanced.dropna(subset=['match_rating']).copy()

    for outcome in outcome_labels:
        fair_odds_col = f"fair_{outcome[0]}"  # Abbreviated column name (e.g., 'fair_h' for 'home_win')
        data_test_enriched[fair_odds_col] = 1 / data_test_enriched[f"{outcome}_prob"]
        closing_odds_col = f"{closing_odds_column_prefix}{outcome.split('_')[0]}_odds"
        data_test_enriched[f"value_{outcome[0]}"] = (data_test_enriched[closing_odds_col] - data_test_enriched[fair_odds_col]) / data_test_enriched[fair_odds_col]

    data_test_enriched['H'] = (data_test_enriched['value_h'] > 0).astype(int)
    data_test_enriched['D'] = (data_test_enriched['value_d'] > 0).astype(int)
    data_test_enriched['A'] = (data_test_enriched['value_a'] > 0).astype(int)

    data_test_enriched = pd.melt(data_test_enriched, id_vars=data_test_enriched.columns[:-3], 
                                value_vars=['H', 'D', 'A'], var_name='prediction', value_name='value_bet')

    data_test_enriched = data_test_enriched[data_test_enriched['value_bet'] == 1].drop(columns='value_bet')

    data_test_enriched['value'] = data_test_enriched.apply(lambda row: row['value_h'] if row['prediction'] == 'H' else (row['value_d'] if row['prediction'] == 'D' else row['value_a']), axis=1)
    data_test_enriched['odds_prediction'] = data_test_enriched.apply(lambda row: row['fair_h'] if row['prediction'] == 'H' else (row['fair_d'] if row['prediction'] == 'D' else row['fair_a']), axis=1)
    data_test_enriched['odds'] = data_test_enriched.apply(lambda row: row['fair_h'] if row['full_time_result'] == 'H' else (row['fair_a'] if row['full_time_result'] == 'A' else row['fair_d']), axis=1)
    data_test_enriched['won'] = (data_test_enriched['full_time_result'] == data_test_enriched['prediction']).astype(int)
    data_test_enriched['profit'] = data_test_enriched['odds'] * data_test_enriched['won'] - 1

    # filtered_data = data_test_enriched[(data_test_enriched['odds_prediction'] > 2) & (data_test_enriched['odds_prediction'] < 4) & (data_test_enriched['value'] < 0.05)]
    filtered_data = data_test_enriched
    bets = len(filtered_data)
    win_rate = filtered_data['won'].mean()
    profit = filtered_data['profit'].sum()
    ror = profit / bets
    odds = filtered_data['odds_prediction'].mean()
    value = filtered_data['value'].mean()
    st_d = np.sqrt((1 + ror) * (odds - 1 - ror))
    tstat = ror * (bets ** 0.5) / st_d
    pvalue = t.sf(tstat, df=bets - 1)

    result = {
        'bets': [bets],
        'win_rate': [win_rate],
        'profit': [profit],
        'ror': [ror],
        'odds': [odds],
        'value': [value],
        'pvalue': [pvalue]
    }

    return result


