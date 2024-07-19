from win_prediction_modules.data_preparation import run_data_prep, add_historic_head_to_head_results
import numpy as np
from db_connection import SQLConnection
import os
from dotenv import load_dotenv
from win_prediction_modules.data_modelling_one import run_data_modelling_part_one
# from win_prediction_modules.data_modelling_two import run_data_modelling_part_two
# from win_prediction_modules.weekly_outcome_prediction import predict_fixture_outcome_odds
import pandas as pd
import datetime

load_dotenv()

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), "localhost" or os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

features = os.environ.get("WIN_PREDICTION_FEATURES").split(",")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def get_current_season():
	current_date = datetime.date.today()
	current_year = current_date.year
	current_month = current_date.month

	if current_month >= 8:  # Season starts in August
		return f"{str(current_year)}-{str(current_year + 1)}"
	else:
		return f"{str(current_year - 1)}-{str(current_year)}"

def run_win_prediction(fixtures: list = []) -> list:
	"""
	Run the win prediction model to predict the outcome of the given fixtures.

	Args:
		fixtures (list): List of tuples in the format (date, home_team_id, away_team_id)

	Returns:
		list : List of tuple in the format (home_team_id, away_team_id, home_win_prob, draw_prob, away_win_prob)
	"""
	match_columns = ["home_goals","away_goals","closing_home_odds","closing_draw_odds","closing_away_odds"]
	all_columns = ["home_goals","away_goals","closing_home_odds","closing_draw_odds","closing_away_odds"] + features
	output_columns = ["home_team_id", "away_team_id", "home_win_prob", "draw_prob", "away_win_prob"]

	fixtures_df = pd.DataFrame()

	if fixtures:
		fixtures_df = pd.DataFrame(fixtures, columns=["date", "home_team_id", "away_team_id"])
		fixtures_df["date"] = pd.to_datetime(fixtures_df["date"]).dt.strftime('%Y-%m-%d')
		fixtures_df["season"] = get_current_season()
		fixtures_df[match_columns] = 10 # arbitrary value that is removed after the shift

		fixtures_df[features] = np.nan

	data = run_data_prep(db, features, fixtures_df)

	data['full_time_result'] = np.where(data['home_goals'] > data['away_goals'], 'H', np.where(data['away_goals'] > data['home_goals'], 'A', 'D'))

	data['home_win'] = np.where(data['full_time_result'] != np.nan, (data['full_time_result'] == 'H').astype(int), np.nan)
	data['draw'] = np.where(data['full_time_result'] != np.nan, (data['full_time_result'] == 'D').astype(int), np.nan)
	data['away_win'] = np.where(data['full_time_result'] != np.nan, (data['full_time_result'] == 'A').astype(int), np.nan)

	data = add_historic_head_to_head_results(data)

	data.to_csv('./files/match_and_form_data.csv', index=False)

	results = run_data_modelling_part_one("logistic_regression", data, features)
	outcome_prob = results["outcome_prob"]["dataframe"]

	output = []

	for home_team_id, away_team_id in fixtures:
		latest_row = outcome_prob[(outcome_prob["home_team_id"] == home_team_id) & (outcome_prob["away_team_id"] == away_team_id)].tail(1)
		home_win_prob = latest_row["home_win_prob"].values[0]
		draw_prob = latest_row["draw_prob"].values[0]
		away_win_prob = latest_row["away_win_prob"].values[0]
		prediction = latest_row["prediction"].values[0]

		output.append((home_team_id, away_team_id, home_win_prob, draw_prob, away_win_prob, prediction))

	# all_results = run_data_modelling_part_two(data)

	# if home_team_id and away_team_id:
	# 	fixture_odds = predict_fixture_outcome_odds(data, home_team_id=home_team_id, away_team_id=away_team_id)
	# 	return fixture_odds

if __name__ == '__main__':
	run_win_prediction()