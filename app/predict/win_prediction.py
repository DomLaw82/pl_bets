from win_prediction.data_preparation import run_data_prep
from win_prediction.data_modelling_one import run_data_modelling_part_one_logistic_regression
from win_prediction.data_modelling_two import run_data_modelling_part_two
from win_prediction.weekly_outcome_prediction import predict_fixture_outcome_odds
import pandas as pd

def run_win_prediction(home_team_id: str = None, away_team_id: str = None):
	run_data_prep()
	data = pd.read_csv('../files/match_and_form_data.csv')
	
	results = run_data_modelling_part_one_logistic_regression(data)
	print(results)

	all_results = run_data_modelling_part_two(data)

	if home_team_id and away_team_id:
		fixture_odds = predict_fixture_outcome_odds(data, home_team_id=home_team_id, away_team_id=away_team_id)
		return fixture_odds

if __name__ == '__main__':
	run_win_prediction()