from flask import Flask
from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
from schema.schemas import *
import pandas as pd
import json
from predict_match_outcome import predict_match_outcome
from rebuild_model import rebuild_model
from retune_and_build_model import retune_and_build_model

rebar = Rebar()
registry = rebar.create_handler_registry()

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
def make_prediction(home_team: str, away_team: str, home_squad: list, away_squad: list):
	request_body = request.get_json()
	player_dict = json.load(request_body)
	
	home_team = player_dict['homeTeam']
	home_players = player_dict['homePlayers']
	away_team = player_dict['awayTeam']
	away_players = player_dict['awayPlayers']
	
	prediction = predict_match_outcome(home_team, home_players, away_team, away_players)

	return 'Prediction made'

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


app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8008")
