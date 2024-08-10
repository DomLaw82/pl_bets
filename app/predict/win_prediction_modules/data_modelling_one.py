import pandas as pd
import numpy as np
from scipy.stats import t
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from win_prediction_modules.plotting_functions import plot_log_reg_coefficients, plot_probability_by_feature

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

def model_testing(models: dict, model_type: str, test_data: pd.DataFrame, outcome_labels: list, feature_columns: list) -> pd.DataFrame:
    """Test the model performance and return the test data with probabilities."""

    if model_type == 'logistic_regression':
        for outcome in outcome_labels:
            positive_outcome_position = np.argmax(models[outcome].classes_)
            probabilities = models[outcome].predict_proba(test_data[feature_columns])
            test_data[f"{outcome}_prob"] = [prob[positive_outcome_position] for prob in probabilities]

    test_data["prediction"] = np.where(
        (test_data["home_win_prob"] > test_data["away_win_prob"]) & (test_data["home_win_prob"] > test_data["draw_prob"]), "H",
        np.where(
            (test_data["draw_prob"] > test_data["home_win_prob"]) & (test_data["draw_prob"] > test_data["away_win_prob"]), "D",
            "A"
        )
    )

    return test_data

def plotting(models: dict, model_type: str, test_data: pd.DataFrame, outcome_labels: list, feature_columns: list) -> None:
    """Plot the scatter graphs for each feature and outcome, and the coefficients for logistic regression."""

    if model_type == 'logistic_regression':

        # Plotting
        plot_log_reg_coefficients(models, outcome_labels)
        for feature in feature_columns:
            # plot_feature_distribution(data_test_enhanced, outcome_labels, feature)
            plot_probability_by_feature(test_data, outcome_labels, feature)

    return test_data

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
                                value_vars=['H', 'D', 'A'], var_name='pred', value_name='value_bet')
    
    df = df[df['value_bet'] == 1].drop(columns='value_bet')


    df['value'] = df.apply(lambda row: row['value_h'] if row['pred'] == 'H' else (row['value_d'] if row['pred'] == 'D' else row['value_a']), axis=1)
    df['odds_prediction'] = df.apply(lambda row: row['fair_h'] if row['pred'] == 'H' else (row['fair_d'] if row['pred'] == 'D' else row['fair_a']), axis=1)
    df['odds'] = df.apply(lambda row: row['fair_h'] if row['full_time_result'] == 'H' else (row['fair_a'] if row['full_time_result'] == 'A' else row['fair_d']), axis=1)
    df['won'] = (df['full_time_result'] == df['pred']).astype(int)
    df['profit'] = df['odds'] * df['won'] - 1

    return df


# Predicts higher win_prob, and look at fair odds and value calculations
def run_model_training(model_type: str, data: pd.DataFrame, features: list, closing_odds_column_prefix: str = "closing_") -> dict: 
    """Runs the first part of the data modelling process."""

    data = data.sort_values(by='date')
    
    outcome_labels = ['home_win', 'draw', 'away_win']

    scaler = StandardScaler()
    data[features] = scaler.fit_transform(data[features])

    # Separating the data into training and testing set
    data_train = data.iloc[:-300]
    data_test =  data.iloc[-300:]
    
    # Model Training
    models = model_training(model_type, data_train, outcome_labels, features)

    data_tested = model_testing(models, model_type, data_test, outcome_labels, features)
    plotting(models, model_type, data_test, outcome_labels, features)

    # Calculate the number of bets, win rate, profit, and return on risk based on value bet analysis
    fair_odds_data = fair_odds_calculation(data_tested, outcome_labels, closing_odds_column_prefix)
    
    # Calculate value of each bet
    value_bets_data = value_bets_analysis(fair_odds_data) 

    #Value bets
    filtered_data = value_bets_data[(value_bets_data['odds_prediction'] > 2) & (value_bets_data['odds_prediction'] < 4) & (value_bets_data['value'] < 0.05)]
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

    print(result)

    # Calculate profit and win rate based on model predictions
    data_test_output = data_tested.copy()

    data_test_output["won"] = np.where(data_test_output["full_time_result"] == data_test_output["prediction"], 1, 0)
    data_test_output["odds"] = np.where(data_test_output["full_time_result"] == "H", data_test_output["closing_home_odds"], np.where(data_test_output["full_time_result"] == "D", data_test_output["closing_draw_odds"], data_test_output["closing_away_odds"]))

    principal = 100
    data_test_output["profit"] = np.where(data_test_output["won"] == 1, (data_test_output["odds"]*principal) - principal, -principal)

    filtered_data = data_test_output
    bets = len(filtered_data)
    win_rate = filtered_data['won'].mean()
    profit = filtered_data['profit'].sum()
    ror = profit / bets

    model_result = {
        'bets': [bets],
        'win_rate': [win_rate],
        'profit': [profit],
        'ror': [ror],
    }
    print(model_result)

    return models