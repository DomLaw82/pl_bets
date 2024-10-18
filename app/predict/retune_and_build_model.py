from neural_net.tune_model_params import tune_model_params
from neural_net.build_model import build_model, get_model
from dataset_creation.create_dataset import create_training_dataset
from transformation.scaling import recreate_scaler, perform_scaling
from sklearn.model_selection import train_test_split
import os
from db_connection import SQLConnection
import pandas as pd
import numpy as np
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))
X_columns = [
	"goals",
	"assists",
	"pens_made",
	"pens_att",
	"shots",
	"shots_on_target",
	"cards_yellow",
	"cards_red",
	"blocks",
	"xg",
	"npxg",
	"passes_total_distance",
	"passes_progressive_distance",
	"passes_completed_short",
	"passes_short",
	"passes_completed_medium",
	"passes_medium",
	"passes_completed_long",
	"passes_long",
	"xg_assist",
	"pass_xa",
	"assisted_shots",
	"passes_into_final_third",
	"passes_into_penalty_area",
	"crosses_into_penalty_area",
	"progressive_passes",
	"tackles",
	"tackles_won",
	"tackles_def_3rd",
	"tackles_mid_3rd",
	"tackles_att_3rd",
	"challenge_tackles",
	"challenges",
	"blocked_shots",
	"blocked_passes",
	"interceptions",
	"clearances",
	"errors",
	"touches",
	"touches_def_pen_area",
	"touches_def_3rd",
	"touches_mid_3rd",
	"touches_att_3rd",
	"touches_att_pen_area",
	"touches_live_ball",
	"take_ons",
	"take_ons_won",
	"take_ons_tackled",
	"carries",
	"carries_distance",
	"carries_progressive_distance",
	"progressive_carries",
	"carries_into_final_third",
	"carries_into_penalty_area",
	"miscontrols",
	"dispossessed",
	"passes_received",
	"progressive_passes_received",
	"sca",
	"sca_passes_live",
	"sca_passes_dead",
	"sca_take_ons",
	"sca_shots",
	"sca_fouled",
	"sca_defense",
	"gca",
	"gca_passes_live",
	"gca_passes_dead",
	"gca_take_ons",
	"gca_shots",
	"gca_fouled",
	"gca_defense",
	"gk_shots_on_target_against",
	"gk_goals_against",
	"gk_saves",
	"gk_clean_sheets",
	"gk_psxg",
	"gk_pens_att",
	"gk_pens_allowed",
	"gk_pens_saved",
	"gk_pens_missed",
	"gk_passed_completed_launched",
	"gk_passes_launched",
	"gk_passes",
	"gk_passes_throws",
	"gk_passes_length_avg",
	"gk_goal_kicks",
	"gk_goal_kicks_length_avg",
]
y_columns = [
	"home_goals", "away_goals", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
	"home_corners", "away_corners", "home_fouls", "away_fouls", "home_yellow_cards", "away_yellow_cards",
	"home_red_cards", "away_red_cards"
]


def rebuild_model(retune: bool = False) -> dict:
	"""
	Re-tunes the model parameters, builds and saves the model, and returns the score and parameters.

	Returns:
		score (float): The score of the model.
		params (dict): The tuned parameters of the model.
	"""
	try:
		dataset = create_training_dataset(db)
		dataset.to_csv("./files/final_combined_dataframe.csv", index=False)
		dataset = pd.read_csv("./files/final_combined_dataframe.csv", encoding="utf-8", index_col=False)

		X = dataset.copy()[X_columns]
		y = dataset.copy()[y_columns]
		

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=543)
		
		recreate_scaler(X)

		X_train_scaled, X_test_scaled = perform_scaling(X_train, X_test)
		X_scaled, _ = perform_scaling(X, no_train=True)
		
		if retune:
			score, params = tune_model_params(get_model, X_train_scaled, y_train)
			
		model = build_model(X_scaled, y)

		model.save("./files/stats_regression_model.h5")

		if retune:
			return {"score": score, "params": params}
		return {"message": "Model rebuilt"}
	except Exception as e:
		print(e)
		return {'error': str(e)}

if __name__ == "__main__":
	rebuild_model(retune=True)