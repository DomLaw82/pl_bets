from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
import pandas as pd
import sys

rebar = Rebar()
registry = rebar.create_handler_registry()


@registry.handles(
	rule='/upload/health',
	method='GET',
	response_body_schema=''
)
def health_check():
	return jsonify('Upload service is healthy')


@registry.handles(
	rule="/upload/upload-file",
	method="POST",
)
def upload_historic_player_data():
	print("Uploading historic player data")
	try:
		request_body = request.get_json()

		path_root = "./data/historic_player_stats"

		season = request_body['season']
		name = request_body['name']
		file = request_body['file']

		if not file.filename.endswith('.csv'):
			raise TypeError("Invalid file type. Only CSV files are allowed.")
		
		save_route = f"{path_root}/{season}/{name}.csv"
		file.save(save_route)
	except Exception as e:
		return jsonify("Error uploading file: " + str(e))

	return jsonify("File uploaded successfully")


app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000", "http://localhost:3001", "http://frontend:3001"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port="8009")

