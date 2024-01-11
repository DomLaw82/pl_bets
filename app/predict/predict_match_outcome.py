from dataset_creation.create_dataset import create_prediction_dataset
from neural_net.build_and_save_model import perform_scaling_and_pca
import tensorflow as tf
import pandas as pd
import numpy as np

# Description: Predict the outcome of a match based on the trained model

# Input: Home team, away team, available players (home and away)
# Output: Predicted match stats (goals, shots, shots on target, corners, fouls, yellow cards, red cards)

# Remove injured/unavailable players from consideration
# Use dataset_creation.create_dataset modules to create a dataset for both teams involved in the game, minus injured/unavailable players
# Read in the model: stats_regression_model.h5
# Use the model to predict the match stats for the game
# Return these stats to the user

def predict_match_outcome(home_team: str, home_players: list, away_team: str, away_players: list) -> dict:

	pd.set_option('display.max_columns', None)
	df = create_prediction_dataset(home_team, home_players, away_team, away_players)
	
	if df.empty:
		return None

	X, _ = perform_scaling_and_pca(df.values, np.array([]), pred=True)
	
	# Load the model
	model = tf.keras.models.load_model('stats_regression_model.h5')
	prediction = model.predict(X)
	return prediction