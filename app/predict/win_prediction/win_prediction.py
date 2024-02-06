from data_preparation import run_data_prep
from data_modelling_one import run_data_modelling_part_one
from data_modelling_two import run_data_modelling_part_two
from outcome_prediction import predict_fixture_outcome_odds
import pandas as pd

def run_win_prediction(home_team_id: str, away_team_id: str):
	run_data_prep()
	data = pd.read_csv('match_and_form_data.csv')
	results = run_data_modelling_part_one(data)
	print(results)
	all_results = run_data_modelling_part_two(data)
	print(all_results)
	fixture_odds = predict_fixture_outcome_odds(data, home_team_id=home_team_id, away_team_id=away_team_id)
	return fixture_odds