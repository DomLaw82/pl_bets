import pandas as pd
from sklearn.decomposition import PCA
from joblib import dump
import numpy as np


pure_stats_columns_no_minutes = [
	"goals","assists","direct_goal_contributions","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"penalties_made","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","progressive_passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]


def create_pca_object(n:int, df:pd.DataFrame) -> PCA:
	pca = PCA(n_components = n, random_state=938)
	pca.fit(df)
	return pca

def recreate_pca_object(n:int = 15, data:np.array = None):
	df = data
	pca_obj = create_pca_object(n, df)
	feature_to_pc_map = pd.DataFrame(pca_obj.components_, columns=pure_stats_columns_no_minutes)
	feature_to_pc_map.to_csv("../files/feature_to_15_pcs.csv", index=False)

if __name__ == "__main__":
	recreate_pca_object()