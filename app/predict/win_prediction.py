from win_prediction_modules.data_preparation import run_data_prep, add_historic_head_to_head_results
import numpy as np
from db_connection import SQLConnection
import os
from dotenv import load_dotenv
from win_prediction_modules.data_modelling_one import run_model_training, model_testing
# from win_prediction_modules.data_modelling_two import run_data_modelling_part_two
# from win_prediction_modules.weekly_outcome_prediction import predict_fixture_outcome_odds
import pandas as pd
import datetime
from app_logger import FluentLogger

load_dotenv()

logger = FluentLogger("win_prediction").get_logger()

# with shots_on_target {'bets': [390], 'win_rate': [0.541025641025641], 'profit': [-337.0], 'ror': [-0.8641025641025641]}
# without shots_on_target {'bets': [390], 'win_rate': [0.558974358974359], 'profit': [2082.0], 'ror': [5.338461538461538]}

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

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
	
def get_current_date():
	return datetime.date.today().strftime('%Y-%m-%d')

def run_win_prediction() -> list:
	"""
	Run the win prediction model to predict the outcome of the given fixtures.

	Args:
		fixtures (list): List of tuples in the format (date, home_team_id, away_team_id)

	Returns:
		list : List of tuple in the format (home_team_id, away_team_id, home_win_prob, draw_prob, away_win_prob)
	"""
	try:
		match_columns = ["home_goals","away_goals","closing_home_odds","closing_draw_odds","closing_away_odds"]
		all_columns = ["home_goals","away_goals","closing_home_odds","closing_draw_odds","closing_away_odds"] + features
		output_columns = ["home_team_id", "away_team_id", "home_win_prob", "draw_prob", "away_win_prob"]
		current_date = get_current_date()

		league_schedules_present = [league[0] for league in db.get_list(f"""
			SELECT 
				DISTINCT competition_id
			FROM schedule
		""")]

		upcoming_fixtures = []
		for league in league_schedules_present:
			fixtures = db.get_list(f"""
				SELECT 
					date, home_team_id, away_team_id, home_elo, away_elo, competition_id
				FROM schedule 
				WHERE date >= '{current_date}' 
					AND round_number = (
						SELECT 
							MIN(round_number) 
						FROM schedule
						WHERE date >= '{current_date}'
					)
					AND competition_id = '{league}'
				ORDER BY date ASC
			""")
			upcoming_fixtures.extend(fixtures) if fixtures else None

		upcoming_fixtures_df = pd.DataFrame()

		if upcoming_fixtures:
			upcoming_fixtures_df = pd.DataFrame(upcoming_fixtures, columns=["date", "home_team_id", "away_team_id", "home_elo", "away_elo", "competition_id"])
			upcoming_fixtures_df["date"] = pd.to_datetime(upcoming_fixtures_df["date"]).dt.strftime('%Y-%m-%d')
			upcoming_fixtures_df["season"] = get_current_season()

			upcoming_fixtures_df[match_columns] = np.nan 
			
			features_without_elos = [feature for feature in features if feature not in ["home_elo", "away_elo"]]
			upcoming_fixtures_df[features_without_elos] = np.nan

		data = run_data_prep(db, features, upcoming_fixtures_df)

		data['full_time_result'] = np.where(data['home_goals'] > data['away_goals'], 'H', np.where(data['away_goals'] > data['home_goals'], 'A', 'D'))

		data['home_win'] = np.where(data['full_time_result'] != np.nan, (data['full_time_result'] == 'H').astype(int), 0)
		data['draw'] = np.where(data['full_time_result'] != np.nan, (data['full_time_result'] == 'D').astype(int), 0)
		data['away_win'] = np.where(data['full_time_result'] != np.nan, (data['full_time_result'] == 'A').astype(int), 0)

		data = add_historic_head_to_head_results(data)

		print(data[data.isnull().any(axis=1)])

		data.to_csv('./files/match_and_form_data.csv', index=False)

		training_data = data[data['date'] < get_current_date()]
		prediction_data = data[data['date'] >= get_current_date()]

		models = run_model_training("logistic_regression", training_data, features)

		outcomes = ["home_win", "draw", "away_win"]
		prediction_data = model_testing(models, "logistic_regression", prediction_data, outcomes, features)

		output = []

		for date, home_team_id, away_team_id, home_elo, away_elo, competition_id in upcoming_fixtures:
			latest_row = prediction_data[(prediction_data["home_team_id"] == home_team_id) & (prediction_data["away_team_id"] == away_team_id)].tail(1)
			home_win_prob = latest_row["home_win_prob"].values[0]
			draw_prob = latest_row["draw_prob"].values[0]
			away_win_prob = latest_row["away_win_prob"].values[0]
			prediction = latest_row["prediction"].values[0]

			output.append(dict(home_team_id=home_team_id, away_team_id=away_team_id, home_win_prob=home_win_prob, draw_prob=draw_prob, away_win_prob=away_win_prob, prediction=prediction, competition_id=competition_id))
		print(output)
		return output
	except Exception as e:
		raise Exception(f"An error occurred while running the win prediction model: line {e.__traceback__.tb_lineno} : {str(e)}")

	# all_results = run_data_modelling_part_two(data)

	# if home_team_id and away_team_id:
	# 	fixture_odds = predict_fixture_outcome_odds(data, home_team_id=home_team_id, away_team_id=away_team_id)
	# 	return fixture_odds

if __name__ == '__main__':
	run_win_prediction()