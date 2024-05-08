from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
import pandas as pd
import sys
from app_logger import FluentLogger

logger = FluentLogger("data_ingestion_api").get_logger()

rebar = Rebar()
registry = rebar.create_handler_registry()


@registry.handles(
	rule='/upload/health',
	method='GET',
	response_body_schema=''
)
def health_check():
	logger.info("Upload service is healthy")
	return jsonify('Upload service is healthy')


@registry.handles(
	rule="/upload/upload-file",
	method="POST",
)
def upload_historic_player_data():
	try:

		path_root = "./data"

		file = request.files['file']
		folder = request.form['folder']
		name = request.form['name']
		season = request.form['season']

		if not file.filename.endswith('.csv'):
			logger.warning("Invalid file type. Only CSV files are allowed.")
			raise TypeError("Invalid file type. Only CSV files are allowed.")
		
		save_route = f"{path_root}/{folder}/{season}/{name}.csv"
		file.save(save_route)
		
		logger.info(f"File {name} for season {season} uploaded successfully to route {save_route}")
		return jsonify("File uploaded successfully")
	
	except Exception as e:
		logger.error(f"Error uploading file {name} for season {season} to route {save_route}: {str(e)}")
		return jsonify("Error uploading file: " + str(e))



app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000", "http://localhost:3001", "http://frontend:3001"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port="8009")

