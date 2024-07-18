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
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from win_prediction_modules.plotting_functions import plot_log_reg_coefficients, plot_feature_distribution, plot_probability_by_feature

with_mean_gd_form = {
    'bets': [294],
    'win_rate': [0.5816326530612245],
    'profit': [11.935339467119459],
    'ror': [0.04059639274530428],
    'odds': [3.0655808815443097],
    'value': [0.7718755269602725],
    'pvalue': [0.3159623010639926]}


# TODO: Calculate sum_gd_form_home and sum_gd_form_away

pd.set_option('display.max_columns', None)

def model_training(model_type: str, training_data: pd.DataFrame, outcome_labels: list, feature_columns: list) -> dict:
    """Trains a model using the specified training data and returns the results."""

    models = {}

    if model_type == 'logistic_regression':
        for outcome in outcome_labels:
            X = training_data[feature_columns]
            y = training_data[outcome]

            model = LogisticRegression()
            model.fit(X, y)
            
            models[outcome] = model
    
    elif model_type == 'logistic_regression_multi':
        X = training_data[feature_columns]
        y = training_data[outcome_labels]

        model = LogisticRegression(multi_class="auto")
        model.fit(X, y)
        
        models["multi"] = model

    elif model_type == 'random_forest':
        for outcome in outcome_labels:
            X_train = training_data[feature_columns]
            y_train = training_data[outcome]

            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            models[outcome] = model

    return models

def fair_odds_calculation(df: pd.DataFrame, outcome_labels: list, closing_odds_column_prefix: str) -> pd.DataFrame:
    for outcome in outcome_labels:
        fair_odds_col = f"fair_{outcome[0]}"  # Abbreviated column name (e.g., 'fair_h' for 'home_win')
        df[fair_odds_col] = 1 / df[f"{outcome}_prob"]
        closing_odds_col = f"{closing_odds_column_prefix}{outcome.split('_')[0]}_odds"
        df[f"value_{outcome[0]}"] = (df[closing_odds_col] - df[fair_odds_col]) / df[fair_odds_col]

    return df

def value_bets_analysis(df: pd.DataFrame) -> dict:
    
    df['H'] = (df['value_h'] > 0).astype(int)
    df['D'] = (df['value_d'] > 0).astype(int)
    df['A'] = (df['value_a'] > 0).astype(int)

    df = pd.melt(df, id_vars=df.columns[:-3], 
                                value_vars=['H', 'D', 'A'], var_name='prediction', value_name='value_bet')

    df = df[df['value_bet'] == 1].drop(columns='value_bet')

    df['value'] = df.apply(lambda row: row['value_h'] if row['prediction'] == 'H' else (row['value_d'] if row['prediction'] == 'D' else row['value_a']), axis=1)
    df['odds_prediction'] = df.apply(lambda row: row['fair_h'] if row['prediction'] == 'H' else (row['fair_d'] if row['prediction'] == 'D' else row['fair_a']), axis=1)
    df['odds'] = df.apply(lambda row: row['fair_h'] if row['full_time_result'] == 'H' else (row['fair_a'] if row['full_time_result'] == 'A' else row['fair_d']), axis=1)
    df['won'] = (df['full_time_result'] == df['prediction']).astype(int)
    df['profit'] = df['odds'] * df['won'] - 1

    return df


# Predicts higher win_prob, and look at fair odds and value calculations
def run_data_modelling_part_one(model_type: str, data: pd.DataFrame, features: list, closing_odds_column_prefix: str = "closing_") -> dict: 
    """Runs the first part of the data modelling process."""
    
    outcome_labels = ['home_win', 'draw', 'away_win']
    enhanced_feature_columns = features

    scaler = StandardScaler()
    data[enhanced_feature_columns] = scaler.fit_transform(data[enhanced_feature_columns])

    # Separating the data into training and testing set
    data_train = data[data['season'] < data['season'].max()]
    data_test = data[data['season'] == data['season'].max()]
    
    # Model Training
    enhanced_models = model_training(model_type, data_train, outcome_labels, enhanced_feature_columns)

    # Predict probabilities for each outcome
    data_test_enhanced = data_test.copy()

    if model_type == 'logistic_regression':
        for outcome in outcome_labels:
            positive_outcome_position = np.argmax(enhanced_models[outcome].classes_)
            probabilities = enhanced_models[outcome].predict_proba(data_test_enhanced[enhanced_feature_columns])
            data_test_enhanced[f"{outcome}_prob"] = [prob[positive_outcome_position] for prob in probabilities]
        plot_log_reg_coefficients(enhanced_models, outcome_labels)
        for feature in enhanced_feature_columns:
            # plot_feature_distribution(data_test_enhanced, outcome_labels, feature)
            plot_probability_by_feature(data_test_enhanced, outcome_labels, feature)

    print(data_test_enhanced.head(50).to_markdown())

    data_test_enriched = fair_odds_calculation(data_test_enhanced, outcome_labels, closing_odds_column_prefix)
    
    # Calculate value of each bet
    data_test_enriched = value_bets_analysis(data_test_enriched) 

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