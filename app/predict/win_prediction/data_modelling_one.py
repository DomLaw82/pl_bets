# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 23:04:59 2023

@author: antoinejwmartin
"""

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t

# Set up our working directory
def run_data_modelling_part_one(data: pd.DataFrame) -> dict: 

    # Separating the data into training and testing set
    data_train = data[data['season'] < data['season'].max()]
    data_test = data[data['season'] == data['season'].max()]

    # Drop rows with NaN values
    data_train = data_train.dropna(subset=['match_rating'])

    # Fit logistic regression models
    home_win_model = smf.glm('home_win ~ match_rating', data=data_train, family=sm.families.Binomial()).fit()
    print(home_win_model.summary())
    draw_model = smf.glm('draw ~ match_rating', data=data_train, family=sm.families.Binomial()).fit()
    print(draw_model.summary())
    away_win_model = smf.glm('away_win ~ match_rating', data=data_train, family=sm.families.Binomial()).fit()
    print(away_win_model.summary())

    # Create a predicted home win probabilities plot
    sns.regplot(x='match_rating', y='home_win', data=data_train, logistic=True)
    plt.title('Home win probability plot')
    plt.xlabel('Match Rating')
    plt.ylabel('Probability')
    plt.savefig('plots/home_win_probability_plot.png', dpi=300)

    # Create a predicted draw probabilities plot
    sns.regplot(x='match_rating', y='draw', data=data_train, logistic=True)
    plt.title('Draw probability plot')
    plt.xlabel('Match Rating')
    plt.ylabel('Probability')
    plt.savefig('plots/draw_probability_plot.png', dpi=300)

    # Create a predicted away win probabilities plot
    sns.regplot(x='match_rating', y='away_win', data=data_train, logistic=True)
    plt.title('Away win probability plot')
    plt.xlabel('Match Rating')
    plt.ylabel('Probability')
    plt.savefig('plots/away_win_probability_plot.png', dpi=300)

    # Predict probabilities for each outcome
    data_test['home_win_prob'] = home_win_model.predict(data_test)
    data_test['draw_prob'] = draw_model.predict(data_test)
    data_test['away_win_prob'] = away_win_model.predict(data_test)


    data_test_enriched = data_test.dropna(subset=['match_rating']).copy()

    data_test_enriched['fair_h'] = 1 / data_test_enriched['home_win_prob']
    data_test_enriched['fair_d'] = 1 / data_test_enriched['draw_prob']
    data_test_enriched['fair_a'] = 1 / data_test_enriched['away_win_prob']

    data_test_enriched['value_h'] = (data_test_enriched['home_odds'] - data_test_enriched['fair_h']) / data_test_enriched['fair_h']
    data_test_enriched['value_d'] = (data_test_enriched['draw_odds'] - data_test_enriched['fair_d']) / data_test_enriched['fair_d']
    data_test_enriched['value_a'] = (data_test_enriched['away_odds'] - data_test_enriched['fair_a']) / data_test_enriched['fair_a']

    data_test_enriched['H'] = (data_test_enriched['value_h'] > 0).astype(int)
    data_test_enriched['D'] = (data_test_enriched['value_d'] > 0).astype(int)
    data_test_enriched['A'] = (data_test_enriched['value_a'] > 0).astype(int)

    data_test_enriched = pd.melt(data_test_enriched, id_vars=data_test_enriched.columns[:-3], 
                                value_vars=['H', 'D', 'A'], var_name='prediction', value_name='value_bet')

    data_test_enriched = data_test_enriched[data_test_enriched['value_bet'] == 1].drop(columns='value_bet')

    data_test_enriched['value'] = data_test_enriched.apply(lambda row: row['value_h'] if row['prediction'] == 'H' else (row['value_d'] if row['prediction'] == 'D' else row['value_a']), axis=1)
    data_test_enriched['odds_prediction'] = data_test_enriched.apply(lambda row: row['fair_h'] if row['prediction'] == 'H' else (row['fair_d'] if row['prediction'] == 'D' else row['fair_a']), axis=1)
    data_test_enriched['odds'] = data_test_enriched.apply(lambda row: row['fair_h'] if row['ftr'] == 'H' else (row['fair_a'] if row['ftr'] == 'A' else row['fair_d']), axis=1)
    data_test_enriched['won'] = (data_test_enriched['ftr'] == data_test_enriched['prediction']).astype(int)
    data_test_enriched['profit'] = data_test_enriched['odds'] * data_test_enriched['won'] - 1

    print(data_test_enriched.head())

    filtered_data = data_test_enriched[(data_test_enriched['odds_prediction'] > 2) & (data_test_enriched['odds_prediction'] < 4) & (data_test_enriched['value'] < 0.05)]
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


