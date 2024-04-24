from win_prediction.data_preparation import run_data_prep
from win_prediction.data_modelling_one import run_data_modelling_part_one
from win_prediction.data_modelling_two import run_data_modelling_part_two
from win_prediction.outcome_prediction import predict_fixture_outcome_odds
import pandas as pd

def run_win_prediction(home_team_id: str = None, away_team_id: str = None):
	run_data_prep()
	data = pd.read_csv('files/match_and_form_data.csv')
	results = run_data_modelling_part_one(data)
	all_results = run_data_modelling_part_two(data)
	fixture_odds = predict_fixture_outcome_odds(data, home_team_id=home_team_id, away_team_id=away_team_id)
	return fixture_odds