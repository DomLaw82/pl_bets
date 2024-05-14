from flask import Flask
from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
from schema.schemas import *
import pandas as pd
import sys
from predict_match_outcome import predict_match_outcome
from rebuild_model import rebuild_model
from retune_and_build_model import retune_and_build_model
from app_logger import FluentLogger

rebar = Rebar()
registry = rebar.create_handler_registry()

logger = FluentLogger("predict-api").get_logger()

def list_to_list_of_objects(list_of_tuples:list, column_names: list) -> list:
	"""
	Convert a list of tuples to a dict

	Args:
			list_of_tuples (list): list of tuples
			column_names (list): list of column names in the order they appear in the tuples

	Returns:
			list: list of dicts
	"""
	result_list = []
	for row in list_of_tuples:
		entry = {}
		for index_b, col in enumerate(row):
			entry[column_names[index_b]] = str(col)
		result_list.append(entry)
	return result_list

@registry.handles(
	rule='/predict/health',
	method='GET',
	response_body_schema=''
)
def health_check():
	try:
		return jsonify({'status': 'Prediction service is healthy'})
	except Exception as e:
		logger.error(f"An error occurred while checking the health of the prediction service: {str(e)}")
		return jsonify({'error': 'An error occurred while checking the health of the prediction service'})

@registry.handles(
	rule='/predict',
	method='POST',
	response_body_schema=match_facts_schema()
)
def make_prediction():
	try:
		request_body = request.get_json()

		home_team_id = request_body.get('homeTeamId')
		home_players = request_body.get('homePlayers')
		away_team_id = request_body.get('awayTeamId')
		away_players = request_body.get('awayPlayers')
		
		prediction = predict_match_outcome(home_team_id, home_players, away_team_id, away_players)
		prediction = list_to_list_of_objects(prediction, ['home_goals', 'away_goals', 'home_shots', 'away_shots', 'home_shots_on_target', 'away_shots_on_target', 'home_corners', 'away_corners', 'home_fouls', 'away_fouls', 'home_yellow_cards', 'away_yellow_cards', 'home_red_cards', 'away_red_cards'])[0]

		logger.info(f"Prediction made: {prediction}")
		return jsonify(prediction)
	except Exception as e:
		logger.error(f"An error occurred while predicting the match outcome: {str(e)}")
		return jsonify({'error': 'An error occurred while predicting the match outcome'})

@registry.handles(
	rule='/model/rebuild',
	method='GET',
	response_body_schema=''
)
def rebuild():
	try:
		rebuild_model()
		logger.info("Model rebuilt")
		return jsonify('Model rebuilt')
	except Exception as e:
		logger.error(f"An error occurred while rebuilding the model: {str(e)}")
		return jsonify({'error': 'An error occurred while rebuilding the model'})

@registry.handles(
	rule='/model/retune',
	method='GET',
	response_body_schema=retune_schema()
)
def retune():
	try:
		output = retune_and_build_model()
		
		score = output["score"]
		params = output["params"]

		params['score'] = score

		logger.info(f"Model retuned with params {params} and score: {score}")
		return jsonify(params)
	except Exception as e:
		logger.error(f"An error occurred while retuning the model: {str(e)}")
		return jsonify({'error': 'An error occurred while retuning the model'})


# Create functions to remake pca and scaler models
@registry.handles(
	rule='/transformation/scaling',
	method='POST',
	response_body_schema=retune_schema()
)
def recreate_scaler():
	pass

@registry.handles(
	rule='/transformation/pca',
	method='POST',
	response_body_schema=retune_schema()
)
def recreate_pca_object():
	pass

app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000", "http://localhost:3001", "http://frontend:3001"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
	 app.run(debug=True, host='0.0.0.0', port="8008")
