from db_connection import SQLConnection
from data_intake.season_schedule import schedule_main
from data_intake.ref_match import ref_match_main
from data_intake.player import player_to_db_main
from data_intake.country_competition import country_competition_main
from data_intake.per_90_stats import per_90_main
from data_intake.download_latest_data import download_latest_data
from data_intake.managers import manager_main
from data_intake.match_logs import match_logs_main
from data_intake.team import team_main
from intake_api import app
import os
from app_logger import FluentLogger
import datetime
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("insert_latest_data").get_logger()

def insert_latest_data():

	try:
		pl_stats_connector = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

		current_year = datetime.datetime.now().year
		current_month = datetime.datetime.now().month
		season_end_year = current_year + 2 if current_month > 6 else current_year + 1 # +2 as range is used, which is exclusive

		logger.debug("---- Ingesting latest data ----")

		# [country, competition]
		country_competition_main(pl_stats_connector)
		logger.debug("\nData Intake: country COMPLETE")
		logger.debug("Data Intake: competition COMPLETE")

		# [team]
		team_main(pl_stats_connector)
		logger.debug("\nData Intake: team COMPLETE")

		# format squad data [player, player_team]
		player_to_db_main(pl_stats_connector)
		logger.debug("\nData Intake: player_team COMPLETE")
		logger.debug("Data Intake: player COMPLETE")

		# format game data [team, match, referee]
		ref_match_main(pl_stats_connector)
		logger.debug("\nData Intake: team COMPLETE")
		logger.debug("Data Intake: match COMPLETE")
		logger.debug("Data Intake: referee COMPLETE")

		# format season schedule [schedule]
		schedule_main(pl_stats_connector)
		logger.debug("\nData Intake: schedule COMPLETE")

		# format manager data [manager]
		manager_main(pl_stats_connector)
		logger.debug("\nData Intake: manager COMPLETE")

		# [historic_player_per_ninety]
		per_90_main(pl_stats_connector)
		logger.debug("\nData Intake: per_90 COMPLETE")

		# [match_logs]
		match_logs_main(pl_stats_connector)
		logger.debug("\nData Intake: match_logs COMPLETE")
		logger.debug("Data Intake: COMPLETE")

		with open("./ingestion_status.txt", "w") as file:
			file.write("Data ingestion completed successfully")

		logger.debug("Data ingestion successful")

		return "Data ingestion successful"
	
	except Exception as e:
		logger.error(f"Error: {e}")
		return f"Error while ingesting data: {e}"
	

if __name__ == "__main__":
	download_latest_data()
	insert_latest_data()
	app.run(debug=True, host="0.0.0.0", port="8009")

