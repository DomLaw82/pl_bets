from dataset_creation.create_dataset import create_prediction_dataset
from transformation.scaling import perform_scaling
import tensorflow as tf
import pandas as pd
import numpy as np
import os
from db_connection import SQLConnection
from app_logger import FluentLogger
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("predict").get_logger()

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

# Description: Predict the outcome of a match based on the trained model

# Input: Home team, away team, available players (home and away)
# Output: Predicted match stats (goals, shots, shots on target, corners, fouls, yellow cards, red cards)

# Remove injured/unavailable players from consideration
# Use dataset_creation.create_dataset modules to create a dataset for both teams involved in the game, minus injured/unavailable players
# Read in the model: stats_regression_model.h5
# Use the model to predict the match stats for the game
# Return these stats to the user

def predict_match_outcome(home_team_id: str, away_team_id: str, **kwargs) -> dict:
	"""
	Predicts the outcome of a match between two teams based on the given home team, home players, away team, and away players.

	Parameters:
	home_team (str): The name of the home team.
	away_team (str): The name of the away team.

	Returns:
	dict: A dictionary containing the predicted match facts.
	"""
	try:
		home_squad_ids = kwargs.get("home_squad_ids", [])
		away_squad_ids = kwargs.get("away_squad_ids", [])
		# Neural network prediction
		pd.set_option('display.max_columns', 10)
		df = create_prediction_dataset(db, home_team_id, away_team_id)
		print(f"Prediction dataset:\n\n{df}")
		if df.empty:
			return None

		X, _ = perform_scaling(df, np.array([]), no_train=True)
		
		model: tf.keras.models.Sequential = tf.keras.models.load_model("files/stats_regression_model.h5")
		prediction = model.predict(X)
		return prediction
	except Exception as e:
		logger.error(f"An error occurred while predicting the match outcome: {str(e)}")
		return None