import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import os
from joblib import load

N = 15

output_columns = [
	"home_goals", "away_goals", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
	"home_corners", "away_corners", "home_fouls", "away_fouls", "home_yellow_cards", "away_yellow_cards",
	"home_red_cards", "away_red_cards"
]
match_columns = [
	"match_id", "competition_id", "home_team_id", "away_team_id", "referee_id",
	"home_goals", "away_goals", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
	"home_corners", "away_corners", "home_fouls", "away_fouls", "home_yellow_cards", "away_yellow_cards",
	"home_red_cards", "away_red_cards"
]
stats_columns = [
	"goals","assists","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","progressive_passes_received","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed",
	"home_team_at_home_mean_goal_difference","home_team_overall_mean_goal_difference","away_team_at_away_mean_goal_difference","away_team_overall_mean_goal_difference","head_to_head_goal_difference"
]
player_stats_columns = ["player_id", "minutes_played","ninetys"] + stats_columns
pure_stats_columns = ["minutes_played"] + stats_columns
team_stats_columns = ["team_id"] + stats_columns

def get_model(hidden_layer_one, dropout, learn_rate, n_h_layers) -> tf.keras.models.Sequential:
	"""
	Creates a neural network model with the specified parameters.

	Parameters:
	hidden_layer_one (int): Number of units in the first hidden layer.
	dropout (float): Dropout rate, a fraction of the input units to drop.
	learn_rate (float): Learning rate for the optimizer.
	n_h_layers (int): Number of additional hidden layers to add.

	Returns:
	tf.keras.models.Sequential: The compiled neural network model.
	"""
	model = tf.keras.models.Sequential()
	model.add(tf.keras.layers.Dense(15, activation="relu", input_dim=15))

	for i in range(n_h_layers):
		model.add(tf.keras.layers.Dense(hidden_layer_one, activation="relu"))

	model.add(tf.keras.layers.Dropout(dropout))
	model.add(tf.keras.layers.Dense(14, activation="relu"))

	model.compile(
		optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=learn_rate),
		loss="mse",
		metrics=["accuracy"])

	return model

def x_y_split_df(df: pd.DataFrame, output_columns: list) -> tuple:
	"""
	Splits the input dataframe into X and y.

	Parameters:
	df (pd.DataFrame): The input dataframe.

	Returns:
	X (pd.DataFrame): The input dataframe with the output columns removed.
	y (pd.DataFrame): The output columns.
	"""
	X = df.drop(output_columns, axis=1)
	y = df[output_columns]
	return X, y

def perform_scaling(X_train: np.array, X_test: np.array, pred: bool = False) -> pd.DataFrame:
	"""
	Perform scaling on the input data.

	Parameters:
	X_train (list): The training data.
	X_test (list): The testing data.

	Returns:
	X_train (pd.DataFrame): The transformed training data after scaling and PCA.
	X_test (pd.DataFrame): The transformed testing data after scaling and PCA.
	"""
	scaler = load('files/prediction_scaler.bin')

	if pred:
		X_train = scaler.transform(X_train)
		# X_test = scaler.transform(X_test.reshape(1, -1))

		# # Carrying out PCA on the train data
		# feature_to_pc_map = pd.read_csv("files/feature_to_15_pcs.csv")
		# X_train = X_train * feature_to_pc_map
		# X_train = pd.DataFrame(X_train.sum(axis=1), columns=['components']).T


	else:
		X_train = scaler.transform(X_train)
		X_test = scaler.transform(X_test)
	
	return X_train, X_test

def build_and_save_model(dataframe: pd.DataFrame) -> tf.keras.models.Sequential:
	"""
	Builds and saves a machine learning model using the provided dataframe.

	Args:
		dataframe (pd.DataFrame): The input dataframe containing the training data.

	Returns:
		tf.keras.models.Sequential: The trained machine learning model.
	"""
	combined = dataframe
	# Split into X and y
	X, y = x_y_split_df(combined, output_columns)

	# Split into train and test
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=543)

	# Scale the data
	X_train, X_test = perform_scaling(X_train, X_test, N)

	# Get model parameters from environment variables
	hidden_layer_one = os.environ.get('hidden_layer_one')
	learn_rate = os.environ.get('learn_rate')
	dropout = os.environ.get('dropout')
	batch_size = os.environ.get('batch_size')
	epochs = os.environ.get('epochs')
	n_h_layers = os.environ.get('n_h_layers')

	# Define fit, and save the model
	model = get_model(hidden_layer_one, dropout, learn_rate, n_h_layers)

	model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)

	return model