from data_preparation import run_data_prep
from data_modelling_one import run_data_modelling_part_one
from data_modelling_two import run_data_modelling_part_two
import pandas as pd

if __name__ == '__main__':
	run_data_prep()


	# data = pd.read_csv('../match_and_form_data.csv')
	# results = run_data_modelling_part_one(data)
	# all_results = run_data_modelling_part_two(data)
