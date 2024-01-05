import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scikeras.wrappers import KerasRegressor
import tensorflow as tf
from sklearn.model_selection import GridSearchCV
import os

output_columns = [
	"home_goals", "away_goals", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
	"home_corners", "away_corners", "home_fouls", "away_fouls", "home_yellow_cards", "away_yellow_cards",
	"home_red_cards", "away_red_cards"
]

player_stats_columns = [
	"player_id", "minutes_played","ninetys","goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]
pure_stats_columns = [
	"minutes_played","goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]
team_stats_columns = [
	"team_id", "goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]
pure_stats_columns_no_minutes = [
	"goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]

def get_mlp_model(hidden_layer_one=13, dropout=0.2, learn_rate=0.01, n_h_layers=1):

	model = tf.keras.models.Sequential()

	# input
	model.add(tf.keras.layers.Dense(15, activation="relu", input_dim=15))

	for i in range(n_h_layers):
		model.add(tf.keras.layers.Dense(hidden_layer_one, activation="relu"))

	# dropout layer to remove redundant nodes
	model.add(tf.keras.layers.Dropout(dropout))
	
	# output
	model.add(tf.keras.layers.Dense(14, activation="relu"))

	model.compile(
		optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=learn_rate),
		loss="mse",
		metrics=["accuracy"])

	return model

model = KerasRegressor(model=get_mlp_model, verbose=0, hidden_layer_one=10, learn_rate=0.01, dropout=0.05, n_h_layers=1);

# define a grid of the hyperparameter search space
hidden_layer_one = [10, 12, 15]
learn_rate = [1e-3, 1e-4, 1e-5]
dropout = [0.2, 0.3, 0.4]
batch_size = [32, 64, 128]
epochs = [12, 15, 17]
n_h_layers = [1, 2, 3, 4]

# create a dictionary from the hyperparameter grid
grid = dict(
	hidden_layer_one=hidden_layer_one,
	learn_rate=learn_rate,
	dropout=dropout,
	batch_size=batch_size,
	epochs=epochs,
	n_h_layers=n_h_layers
)

def scoring(estimator, test_x: np.ndarray, test_y: pd.DataFrame) -> float:
	test_y = test_y.to_numpy()
	
	estimator.fit(test_x, test_y);
	y_hat = estimator.predict(test_x)
	
	average_under_rate = 0

	total_shots_under = 0
	total_shots_on_target_under = 0
	total_booking_points_under = 0
	total_corners_under = 0
	total_fouls_under = 0
	goals_under = 0

	total_tested = len(y_hat)
	
	for idx, y in enumerate(y_hat):

		home_goals_hat, away_goals_hat, home_shots_hat, away_shots_hat, home_shots_on_target_hat, away_shots_on_target_hat, home_corners_hat, away_corners_hat, home_fouls_hat, away_fouls_hat, home_yellow_cards_hat, away_yellow_cards_hat, home_red_cards_hat, away_red_cards_hat = y
		home_goals, away_goals, home_shots, away_shots, home_shots_on_target, away_shots_on_target, home_corners, away_corners, home_fouls, away_fouls, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards = test_y[idx]

		total_shots_under += 1 if np.floor(home_shots_hat)+np.floor(away_shots_hat) < home_shots+away_shots else 0
		total_shots_on_target_under += 1 if np.floor(home_shots_on_target_hat)+np.floor(away_shots_on_target_hat) < home_shots_on_target+away_shots_on_target else 0
		total_booking_points_under += 1 if (np.floor(home_yellow_cards_hat)+np.floor(away_yellow_cards_hat))*10+(np.floor(home_red_cards_hat)+np.floor(away_red_cards_hat))*25 < (home_yellow_cards+away_yellow_cards)*10+(home_red_cards+away_red_cards)*25 else 0
		total_corners_under += 1 if np.floor(home_corners_hat) + np.floor(away_corners_hat) < home_corners + away_corners else 0
		total_fouls_under += 1 if np.floor(home_fouls_hat) + np.floor(away_fouls_hat) < home_fouls+ away_fouls else 0
		goals_under += 1 if np.floor(home_goals_hat) + np.floor(away_goals_hat) < home_goals + away_goals else 0

		average_under_rate += ((total_shots_under/total_tested)+(total_shots_on_target_under/total_tested)+(total_booking_points_under/total_tested)+(total_fouls_under/total_tested)+(total_corners_under/total_tested)+(goals_under/total_tested))/6

	average_under_rate = average_under_rate/total_tested
	
	return average_under_rate

def tune_model_params():
	combined = pd.read_csv("../final_combined_dataframe.csv")

	X = combined[pure_stats_columns_no_minutes]
	y = combined[output_columns]

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=543)

	X_scaler = StandardScaler(copy=True).fit(X_train)
	y_scaler = StandardScaler(copy=True).fit(y_train)

	X_train = X_scaler.transform(X_train)
	X_test = X_scaler.transform(X_test)

	n=15

	pca = PCA(n_components = n, random_state=576)
	pca.fit(X_train)

	X_train = pca.transform(X_train)
	X_test = pca.transform(X_test)

	searcher = GridSearchCV(estimator=model, n_jobs=-2, 
		param_grid=grid, scoring=scoring, verbose=4, cv=3)

	searchResults = searcher.fit(X_train, y_train)

	best_score = searchResults.best_score_
	best_params = searchResults.best_params_
	print("[INFO] best score is {:.5f} using {}".format(best_score,best_params))

	for key, value in best_params.items():
		os.environ[key] = str(value)
	
	return best_score, best_params
