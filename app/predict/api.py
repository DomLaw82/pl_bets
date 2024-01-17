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

rebar = Rebar()
registry = rebar.create_handler_registry()

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
	return jsonify('Prediction service is healthy')

@registry.handles(
	rule='/predict',
	method='POST',
	response_body_schema=match_facts_schema()
)
def make_prediction():
	request_body = request.get_json()

	home_team_id = request_body['homeTeamId']
	home_players = request_body['homePlayers']
	away_team_id = request_body['awayTeamId']
	away_players = request_body['awayPlayers']
	
	prediction = predict_match_outcome(home_team_id, home_players, away_team_id, away_players)
	prediction = list_to_list_of_objects(prediction, ['home_goals', 'away_goals', 'home_shots', 'away_shots', 'home_shots_on_target', 'away_shots_on_target', 'home_corners', 'away_corners', 'home_fouls', 'away_fouls', 'home_yellow_cards', 'away_yellow_cards', 'home_red_cards', 'away_red_cards'])[0]

	return jsonify(prediction)

@registry.handles(
	rule='/model/rebuild',
	method='POST',
	response_body_schema=''
)
def rebuild():
	rebuild_model()
	return jsonify('Model rebuilt')

@registry.handles(
	rule='/model/retune',
	method='POST',
	response_body_schema=retune_schema()
)
def retune():
	score, params = retune_and_build_model()
	params['score'] = score
	return jsonify(params)


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
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
	 app.run(debug=True, host='0.0.0.0', port="8008")
