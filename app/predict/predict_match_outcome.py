from dataset_creation.create_dataset import create_prediction_dataset
from win_prediction.data_modelling_one import run_data_modelling_part_one
from neural_net.build_and_save_model import perform_scaling
from win_prediction.win_prediction import run_win_prediction
import tensorflow as tf
import pandas as pd
import numpy as np
from joblib import load

# Description: Predict the outcome of a match based on the trained model

# Input: Home team, away team, available players (home and away)
# Output: Predicted match stats (goals, shots, shots on target, corners, fouls, yellow cards, red cards)

# Remove injured/unavailable players from consideration
# Use dataset_creation.create_dataset modules to create a dataset for both teams involved in the game, minus injured/unavailable players
# Read in the model: stats_regression_model.h5
# Use the model to predict the match stats for the game
# Return these stats to the user

def predict_match_outcome(home_team_id: str, home_players: list, away_team_id: str, away_players: list) -> dict:
	"""
	Predicts the outcome of a match between two teams based on the given home team, home players, away team, and away players.

	Parameters:
	home_team (str): The name of the home team.
	home_players (list): A list of home players.
	away_team (str): The name of the away team.
	away_players (list): A list of away players.

	Returns:
	dict: A dictionary containing the predicted match facts.
	"""

	# Neural network prediction
	pd.set_option('display.max_columns', 10)
	df = create_prediction_dataset(home_team_id, home_players, away_team_id, away_players)
	
	if df.empty:
		return None

	X, _ = perform_scaling(df, np.array([]), pred=True)
	

	model = tf.keras.models.load_model("stats_regression_model.h5")
	prediction = model.predict(X)

	# Logistic regression prediction
	odds = run_win_prediction(home_team_id, away_team_id)

	return prediction, odds