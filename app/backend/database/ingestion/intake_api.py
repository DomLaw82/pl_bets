from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
import pandas as pd
import os
from app_logger import FluentLogger
from date_functions import get_current_season
from data_intake.per_90_stats import per_90_update
from data_intake.download_latest_data import download_all_fixture_data, download_all_game_data
from data_intake.ref_match import clean_ref_match_data
from data_intake.player import get_player_fbref_data, player_to_db_main
from data_intake.season_schedule import clean_schedule_data
from db_connection import SQLConnection
import datetime
from update_match_logs import update_match_logs_main
from data_intake.utilities.save_to_database import save_to_database
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

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
        download_all_game_data(two_digit_season, game_data_download_root, game_data_save_root)
        
        save_path = os.path.join(game_data_save_root, f"E0 - {two_digit_season}.csv")
        game_data_df = pd.read_csv(save_path)

        clean_match_data_df = clean_ref_match_data(db, "match", current_season, game_data_df)
        clean_referee_data_df = clean_ref_match_data(db, "referee", current_season, game_data_df)
        
        with db.connect() as conn:
            clean_match_data_df.to_sql("match", conn, if_exists="append", index=False) if not clean_match_data_df.empty else None
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
        logs_location = "./data/fbref_data/player_data.csv"
        current_season = get_current_season()
        url = f'https://fbref.com/en/comps/9/{current_season}/stats/{current_season}-Premier-League-Stats'

        newest_entries = get_player_fbref_data(url, current_season)
        if newest_entries is None:
            logger.error(f"Error fetching player data for season {current_season}")
            return jsonify(f"Error fetching player data for season {current_season}"), 500
        current_entries_df = pd.read_csv(logs_location)
        newest_entries_df = pd.DataFrame(newest_entries)[current_entries_df.columns]
        updated_df = pd.concat([current_entries_df, newest_entries_df], ignore_index=True)
        updated_df.drop_duplicates(subset=["fbref_id", "season"], keep="last", inplace=True)
        updated_df.to_csv(logs_location, index=False)
        player_to_db_main(db)

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
        
        download_all_fixture_data(str(current_season.split("-")[0]), schedule_data_download_root, schedule_data_save_root)
        season_schedule_file_path = os.path.join(schedule_data_save_root, f"epl_{str(current_season.split('-')[0])}-{str(current_season.split('-')[1][-2:])}.csv")
        
        df = pd.read_csv(season_schedule_file_path)
        if df.empty:
            logger.error(f"No schedule data found for season {current_season}")
            return jsonify(f"No schedule data found for season {current_season}"), 404
        
        df = clean_schedule_data(db, df)
        
        if not df.empty:
            with db.connect() as conn:
                logger.info(f"Inserting schedule data for season {current_season}")
                print("Schedule_df\n")
                print(df)
                df.to_sql("schedule", conn, if_exists="append", index=False)
                logger.info(f"Inserted into schedule table for {current_season}")

                logger.info(f"Schedule data for season {current_season} updated and inserted successfully")
                return jsonify(f"Schedule data for season {current_season} updated and inserted successfully"), 200

        logger.info(f"Schedule data for season {current_season} up to date")
        return jsonify(f"Schedule data for season {current_season} up to date"), 200

    except Exception as e:
        logger.error(f"Error refreshing schedule data: {str(e)}")
        return jsonify(f"Error refreshing schedule data: {str(e)}"), 500

@registry.handles(
    rule="/refresh/match-logs",
    method="GET",
)
def update_match_logs():
    try:
        current_season = get_current_season()
        result = update_match_logs_main(current_season)
        if not result.empty:
            save_to_database(db, result, "match_logs")
            return jsonify("Match logs updated successfully"), 200
    except Exception as e:
        logger.error(f"An error occurred while updating match logs: line {e.__traceback__.tb_lineno} : {str(e)}")
        return jsonify(f"An error occurred while updating match logs: line {e.__traceback__.tb_lineno} : {str(e)}"), 500
    

app = Flask(__name__)
CORS(app, origins=["http://api:8080", "http://localhost:8080", "http://localhost:3000", "http://frontend:3000", "http://localhost:3001", "http://frontend:3001"],  supports_credentials=True)
rebar.init_app(app)

