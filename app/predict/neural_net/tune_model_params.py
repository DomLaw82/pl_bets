import pandas as pd
import numpy as np
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import GridSearchCV
import tensorflow as tf
import os
from typing import Callable
from app_logger import FluentLogger
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("tune_model_params").get_logger()

def scoring(estimator, test_x: np.ndarray, test_y: pd.DataFrame) -> float:
	"""
	Calculate the average under rate for a given estimator using test data.

	Parameters:
	estimator (object): The estimator object used for prediction.
	test_x (np.ndarray): The input features for testing.
	test_y (pd.DataFrame): The actual output values for testing.

	Returns:
	float: The average under rate.

	"""
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

def tune_model_params(get_model_fn: Callable[[int,int,int,float,float,int],tf.keras.models.Sequential], X_train: np.ndarray, y_train: np.ndarray) -> tuple:
	"""
	Tune the parameters of a model using grid search and return the best score and parameters.

	Parameters:
	get_model_fn (Callable): The function that returns the model.
	X_train (np.ndarray): The input features for training.
	y_train (np.ndarray): The actual output values for training.


	Returns:
		tuple: A tuple containing the best score and best parameters found during grid search.
	"""

	model = KerasRegressor(model=get_model_fn, verbose=0, input_length=X_train.shape[1], output_length=y_train.shape[1], hidden_layers=[100, 75, 50, 25], learn_rate=0.01, dropout=0.05);
	
	hidden_layers = [
		# [84, 70, 56, 42],
		# [100, 70, 50, 30], # loss: 51.1779 - accuracy: 0.3213 loss: 40.1592 - accuracy: 0.2843
		[84, 84, 84, 84], # loss: 43.8117 - accuracy: 0.2729 loss: 42.6110 - accuracy: 0.2470 loss: 49.9276 - accuracy: 0.2377 loss: 41.6125 - accuracy: 0.3479
	]
	learn_rate = [1e-5]
	dropout = [0.4]
	batch_size = [64]
	epochs = [20]

	grid = dict(
		hidden_layers=hidden_layers,
		learn_rate=learn_rate,
		dropout=dropout,
		batch_size=batch_size,
		epochs=epochs,
	)

	searcher = GridSearchCV(estimator=model, n_jobs=-2, param_grid=grid, scoring=scoring, verbose=4, cv=3)

	searchResults = searcher.fit(X_train, y_train)

	best_score = searchResults.best_score_
	best_params = searchResults.best_params_

	logger.info("[INFO] best score is {:.5f} using {}".format(best_score,best_params))

	for key, value in best_params.items():
		os.environ[key] = str(value)
	
	return best_score, best_params
