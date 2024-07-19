from win_prediction_modules.data_preparation import run_data_prep
from db_connection import SQLConnection
import os
from dotenv import load_dotenv
from win_prediction_modules.data_modelling_one import run_data_modelling_part_one
# from win_prediction_modules.data_modelling_two import run_data_modelling_part_two
# from win_prediction_modules.weekly_outcome_prediction import predict_fixture_outcome_odds
import pandas as pd

load_dotenv()

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), "localhost" or os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

features = os.environ.get("WIN_PREDICTION_FEATURES").split(",")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def run_win_prediction(home_team_id: str = None, away_team_id: str = None):
	data = run_data_prep(db, features)
	results = run_data_modelling_part_one("logistic_regression", data, features)

	# all_results = run_data_modelling_part_two(data)

	# if home_team_id and away_team_id:
	# 	fixture_odds = predict_fixture_outcome_odds(data, home_team_id=home_team_id, away_team_id=away_team_id)
	# 	return fixture_odds

if __name__ == '__main__':
	run_win_prediction()