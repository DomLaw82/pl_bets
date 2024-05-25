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
from sklearn.inspection import PartialDependenceDisplay
from sklearn.linear_model import LogisticRegression

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

def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    """Adds features for team form, head-to-head records, and home advantage."""

    # Head-to-Head Records
    h2h_data = (
        data.groupby(['home_team_id', 'away_team_id'])[['home_win', 'draw', 'away_win']].sum().reset_index()
    )
    h2h_data.columns = ['home_team_id', 'away_team_id', 'h2h_home_wins', 'h2h_draws', 'h2h_away_wins']

    data = data.merge(h2h_data, on=['home_team_id', 'away_team_id'], how='left').fillna(0)

    return data

def plot_coefficients(models, outcome_labels):
    """Plots coefficients for each model."""

    plt.figure(figsize=(12, 6))

    for i, outcome in enumerate(outcome_labels):
        coefs = pd.DataFrame({
            'Feature': models[outcome].params.index,
            'Coefficient': models[outcome].params.values,
            'Outcome': outcome
        })
        plt.subplot(1, 3, i+1)
        sns.barplot(data=coefs, x='Coefficient', y='Feature', orient='h', color='skyblue')
        plt.title(f'Coefficients for {outcome.replace("_", " ").title()}')
        plt.axvline(x=0, color='black', linestyle='dashed', linewidth=1)
    plt.tight_layout()
    # plt.show()
    # plt.savefig('win_prediction/plots/model_coefficients_plot.png', dpi=300)

def plot_match_rating_distribution(data: pd.DataFrame, outcome_labels: list):
    """Plots the distribution of match ratings for each outcome."""

    plt.figure(figsize=(12, 6))
    
    for i, outcome in enumerate(outcome_labels):
        plt.subplot(1, 3, i + 1)
        sns.histplot(data=data, x='match_rating', hue=outcome, element='step', fill=True, common_norm=False, palette='muted', stat='density')
        plt.title(f'Match Rating Distribution for {outcome.replace("_", " ").title()}')

        zero_subset = data[data[outcome] == 0]
        one_subset = data[data[outcome] == 1]

        # Fit normal distribution to each subset
        mu_zero, std_zero = norm.fit(zero_subset['match_rating'])
        mu_one, std_one = norm.fit(one_subset['match_rating'])

        # Generate x values
        x_values_zero = np.linspace(zero_subset["match_rating"].min(), zero_subset["match_rating"].max(), 100)
        x_values_one = np.linspace(one_subset["match_rating"].min(), one_subset["match_rating"].max(), 100)

        # Calculate the PDF for each subset
        y_values_zero = norm.pdf(x_values_zero, mu_zero, std_zero)
        y_values_one = norm.pdf(x_values_one, mu_one, std_one)

        # Plot the PDF
        plt.plot(x_values_zero, y_values_zero, color='blue', label='Class 0 Fit')
        plt.plot(x_values_one, y_values_one, color='red', label='Class 1 Fit')
        
        plt.legend()

    plt.tight_layout()
    # plt.show()
    # plt.savefig('win_prediction/plots/match_rating_distribution_plot.png', dpi=300)

def plot_probability_by_match_rating(data: pd.DataFrame, models: dict, outcome_labels: list):
    """Plots the probability of each outcome by match rating."""
    plt.figure(figsize=(10, 6)) 

    markers = ['o', 'x', '+']
    colours = ['blue', 'orange', 'green']

    for outcome, marker, color in zip(outcome_labels, markers, colours):
        sns.regplot(x='match_rating', y=f"{outcome}_prob", data=data, logistic=True, label=outcome.replace("_", " ").title(), 
                    marker=marker, color=color, fit_reg=False, scatter_kws={'s': 50, 'alpha': 0.7})
        
        # Calculate and plot the logistic regression curve
        x_values = np.linspace(data['match_rating'].min(), data['match_rating'].max(), 100)
        y_values = models[outcome].predict(pd.DataFrame({'match_rating': x_values}))
        plt.plot(x_values, y_values, color=color)

    plt.title('Outcome Probabilities by Match Rating')
    plt.xlabel('Match Rating')
    plt.ylabel('Probability')
    plt.legend()
    # plt.show()
    # plt.savefig('win_prediction/plots/outcome_probability_by_match_rating_plot.png', dpi=300)

# Set up our working directory
def run_data_modelling_part_one_logistic_regression(data: pd.DataFrame, closing_odds_column_prefix: str = "closing_") -> dict: 
    """Runs the first part of the data modelling process."""

    # Separating the data into training and testing set
    data_train = data[data['season'] < data['season'].max()]
    data_test = data[data['season'] == data['season'].max()]

    # Drop rows with NaN values
    data_train = data_train.dropna(subset=['match_rating'])

    data_train = engineer_features(data_train)
    data_test = engineer_features(data_test)

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

    # plot_feature_effects(data_test, models, outcome_labels)
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


