from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
import pandas as pd
import os
from app_logger import FluentLogger
from data_intake.per_90_stats import per_90_update
from db_connection import SQLConnection

logger = FluentLogger("data_ingestion-api").get_logger()
db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

rebar = Rebar()
registry = rebar.create_handler_registry()


@registry.handles(
    rule='/upload/health',
    method='GET',
    response_body_schema=''
)
def health_check():
    return jsonify('Upload service is healthy')


from flask import request, jsonify
import pandas as pd
import os
import logging

@registry.handles(
    rule="/upload/upload-file",
    method="POST",
)
def upload_historic_player_data():
    path_root = "./data"  # Base directory for saving files
    try:
        folder = request.form['folder']
        season = request.form['season']
        files = request.files.getlist('files')
        names = request.form.getlist('names')

        # Ensure the directory structure exists
        os.makedirs(os.path.join(path_root, folder, season), exist_ok=True)

        files_uploaded = []

        logger.info(f"Uploading files: {', '.join(names)}")

        for name, file in list(zip(names, files)):

            # Validate file type
            if not file.filename.endswith('.csv'):
                logger.warning("Invalid file type. Only CSV files are allowed.")
                return jsonify("Invalid file type. Only CSV files are allowed."), 400

            # Construct the full save path
            save_route = os.path.join(path_root, folder, season, f"{name}.csv")
            
            # Save the file to the specified path
            file.save(save_route)
            logger.info(f"File {name} saved to {save_route}")
            files_uploaded.append(name)

        per_90_update(db, season)

        return jsonify(f"Files uploaded successfully: {', '.join(files_uploaded)}"), 200

    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}")
        return jsonify(f"Error uploading files: {str(e)}"), 500




app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000", "http://localhost:3001", "http://frontend:3001"],  supports_credentials=True)
rebar.init_app(app)

