from flask import Flask
from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
from schema.schemas import *
import pandas as pd
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
   rule='/predict/predict?home_team=<home_team>&away_team=<away_team>&home_squad=<home_squad>&away_squad=<away_squad>',
   method='POST',
   response_body_schema=match_facts_schema()
)
def make_prediction(home_team: str, away_team: str, home_squad: list, away_squad: list):
	# Add code to make predictions here
	return 'Prediction made'

@registry.handles(
   rule='/predict/rebuild',
   method='POST',
   response_body_schema=''
)
def rebuild():
	rebuild_model()
	return jsonify('Model rebuilt')

@registry.handles(
   rule='/predict/retune',
   method='POST',
   response_body_schema=retune_schema()
)
def retune():
	score, params = retune_and_build_model()
	params['score'] = score
	return jsonify(params)


app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8008")
