# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:23:31 2023

@author: antoinejwmartin
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import t

# Start the loop for the desired seasons
def run_data_modelling_part_two(data: pd.DataFrame):
    season_results = []
    print("\n\n\ndata_\n\n\n",data)

    for season in sorted(data["season"].unique().tolist()):
        data_train = data[data['season'] < season]
        if data_train.empty:
            continue
        data_test = data[data['season'] == season]
        
        # Drop rows with NaN values
        data_train = data_train.dropna(subset=['match_rating'])
        
        # Fit logistic regression models
        home_win_model = smf.glm('home_win ~ match_rating', data=data_train, family=sm.families.Binomial()).fit()
        print(home_win_model.summary())
        draw_model = smf.glm('draw ~ match_rating', data=data_train, family=sm.families.Binomial()).fit()
        print(draw_model.summary())
        away_win_model = smf.glm('away_win ~ match_rating', data=data_train, family=sm.families.Binomial()).fit()
        print(away_win_model.summary())
        
        # Predict probabilities for each outcome
        data_test['home_win_prob'] = home_win_model.predict(data_test)
        data_test['draw_prob'] = draw_model.predict(data_test)
        data_test['away_win_prob'] = away_win_model.predict(data_test)
        
        
        data_test_enriched = data_test.dropna(subset=['match_rating']).copy()
        
        data_test_enriched['fair_h'] = 1 / data_test_enriched['home_win_prob']
        data_test_enriched['fair_d'] = 1 / data_test_enriched['draw_prob']
        data_test_enriched['fair_a'] = 1 / data_test_enriched['away_win_prob']
        
        data_test_enriched['value_h'] = (data_test_enriched['closing_home_odds'] - data_test_enriched['fair_h']) / data_test_enriched['fair_h']
        data_test_enriched['value_d'] = (data_test_enriched['closing_draw_odds'] - data_test_enriched['fair_d']) / data_test_enriched['fair_d']
        data_test_enriched['value_a'] = (data_test_enriched['closing_away_odds'] - data_test_enriched['fair_a']) / data_test_enriched['fair_a']
        
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
        
        result = pd.DataFrame({
            'bets': [bets],
            'win_rate': [win_rate],
            'profit': [profit],
            'ror': [ror],
            'odds': [odds],
            'value': [value],
            'pvalue': [pvalue]
        })
        
        result['season'] = season
        season_results.append(result)

        
    season_results_df = pd.concat(season_results, ignore_index=True)
    print(season_results_df)

    # Create a total of the four seasons
    bets = season_results_df['bets'].sum()
    win_rate = (season_results_df['win_rate']*season_results_df['bets']).sum()/season_results_df['bets'].sum()
    profit = season_results_df['profit'].sum()
    ror = profit / bets
    odds = season_results_df['odds'].mean()
    value = season_results_df['value'].mean()
    st_d = np.sqrt((1 + ror) * (odds - 1 - ror))
    tstat = ror * (bets ** 0.5) / st_d
    pvalue = t.sf(tstat, df=bets - 1)


    result_all = pd.DataFrame({
        'bets': [bets],
        'win_rate': [win_rate],
        'profit': [profit],
        'ror': [ror],
        'odds': [odds],
        'value': [value],
        'pvalue': [pvalue]
    })

    print(result_all)
    result_all['season'] = "all"

    # See overall results
    combined_season_results_df = pd.concat([season_results_df, result_all], ignore_index=True)

    return combined_season_results_df

