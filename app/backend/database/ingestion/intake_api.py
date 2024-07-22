from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
import pandas as pd
import os
from app_logger import FluentLogger
from data_intake.per_90_stats import per_90_update
from data_intake.download_latest_data import download_csv_for_all_fixtures_in_a_season, download_csv_for_all_games_in_a_season, download_html_for_squad_player_data
from data_intake.team_ref_match import clean_match_data
from data_intake.player import player_main_by_season
from data_intake.season_schedule import clean_schedule_data
from db_connection import SQLConnection
import datetime

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
    return jsonify('Upload service is healthy'), 200

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


def get_current_season():
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    if current_month >= 8:  # Season starts in August
        return f"{str(current_year)}-{str(current_year + 1)}"
    else:
        return f"{str(current_year - 1)}-{str(current_year)}"


# /refresh/game-data
@registry.handles(
    rule="/refresh/game-data",
    method="GET",
)
def refresh_game_data():
    try:
        current_season = get_current_season()

        game_data_download_root = os.environ.get("GAME_DATA_DOWNLOAD_ROOT")
        game_data_save_root = os.environ.get("GAME_DATA_SAVE_ROOT")
        
        two_digit_season = "".join([str(year)[-2:] for year in current_season.split("-")])
        download_csv_for_all_games_in_a_season(two_digit_season, game_data_download_root, game_data_save_root)
        
        save_path = os.path.join(game_data_save_root, f"E0 - {two_digit_season}.csv")
        game_data_df = pd.read_csv(save_path)

        clean_match_data_df = clean_match_data(db, "match", current_season, game_data_df)
        clean_team_data_df = clean_match_data(db, "team", current_season, game_data_df)
        clean_referee_data_df = clean_match_data(db, "referee", current_season, game_data_df)
        
        with db.connect() as conn:
            clean_match_data_df.to_sql("match", conn, if_exists="append", index=False) if not clean_match_data_df.empty else None
            clean_team_data_df.to_sql("team", conn, if_exists="append", index=False) if not clean_team_data_df.empty else None
            clean_referee_data_df.to_sql("referee", conn, if_exists="append", index=False) if not clean_referee_data_df.empty else None

            logger.info(f"Game data for season {current_season} updated and inserted successfully")
            return jsonify(f"Game data for season {current_season} updated and inserted successfully"), 200

    except Exception as e:
        logger.error(f"Error refreshing game data: {str(e)}")
        return jsonify(f"Error refreshing game data: {str(e)}"), 500


# refresh/squad-data
@registry.handles(
    rule="/refresh/squad-data",
    method="GET",
)
def refresh_squad_data():
    try:
        current_season = get_current_season()
        
        squad_data_download_root = os.environ.get("PLAYER_DOWNLOAD_ROOT")
        squad_data_save_root = os.environ.get("PLAYER_SAVE_PATH_ROOT")
        download_html_for_squad_player_data(current_season+"/", squad_data_download_root, squad_data_save_root)
        player_main_by_season(db, current_season, squad_data_save_root)

        logger.info(f"Squad data for season {current_season} updated and inserted successfully")
        return jsonify(f"Game data for season {current_season} updated and inserted successfully"), 200
        
    except Exception as e:
        logger.error(f"Error refreshing squad data: {str(e)}")
        return jsonify(f"Error refreshing squad data: {str(e)}"), 500


# refresh/schedule-data
@registry.handles(
    rule="/refresh/schedule-data",
    method="GET",
)
def refresh_schedule_data():
    try:
        current_season = get_current_season()
        
        schedule_data_download_root = os.environ.get("DOWNLOAD_FIXTURE_URL_ROOT")
        schedule_data_save_root = os.environ.get("SCHEDULE_SAVE_PATH_ROOT")
        logger.info(f"Downloading schedule data for season {current_season}")
        
        download_csv_for_all_fixtures_in_a_season(str(current_season.split("-")[0]), schedule_data_download_root, schedule_data_save_root)
        season_schedule_file_path = os.path.join(schedule_data_save_root, f"epl_{str(current_season.split('-')[0])}-{str(current_season.split('-')[1][-2:])}.csv")
        
        df = pd.read_csv(season_schedule_file_path)
        if df.empty:
            logger.error(f"No schedule data found for season {current_season}")
            return jsonify(f"No schedule data found for season {current_season}"), 404
        
        df = clean_schedule_data(db, df)
        
        if not df.empty:
            with db.connect() as conn:
                logger.info(f"Inserting schedule data for season {current_season}")
                df.to_sql("schedule", conn, if_exists="append", index=False)
                logger.info(f"Inserted into schedule table for {current_season}")

                logger.info(f"Schedule data for season {current_season} updated and inserted successfully")
                return jsonify(f"Schedule data for season {current_season} updated and inserted successfully"), 200

        logger.info(f"Schedule data for season {current_season}/{str(int(current_season)+1)} up to date")
        return jsonify(f"Schedule data for season {current_season}/{str(int(current_season)+1)} up to date"), 200

    except Exception as e:
        logger.error(f"Error refreshing schedule data: {str(e)}")
        return jsonify(f"Error refreshing schedule data: {str(e)}"), 500

app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000", "http://localhost:3001", "http://frontend:3001"],  supports_credentials=True)
rebar.init_app(app)

