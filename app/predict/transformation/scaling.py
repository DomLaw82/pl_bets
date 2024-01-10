import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import dump


pure_stats_columns_no_minutes = [
	"goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]

def recreate_scaler():
	df = pd.read_csv("../final_combined_dataframe.csv")

	scaler = StandardScaler(copy=True).fit(df[pure_stats_columns_no_minutes])

	dump(scaler, '../prediction_scaler.bin', compress=True)
