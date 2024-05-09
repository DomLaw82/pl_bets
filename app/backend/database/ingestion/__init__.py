from db_connection import SQLConnection
from data_intake.season_schedule import schedule_main
from data_intake.team_ref_match import team_ref_match_main
from data_intake.player import player_main
from data_intake.country_competition import country_competition_main
from data_intake.per_90_stats import per_90_main
from data_intake.download_latest_data import download_latest_data
from intake_api import app
import os
from app_logger import FluentLogger

logger = FluentLogger("insert_latest_data").get_logger()

def insert_latest_data():

	try:		
		pl_stats_connector = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

		logger.info("---- Ingesting latest data ----")

		# [country, competition]
		country_competition_main(pl_stats_connector)
		logger.info("\nData Intake: country COMPLETE")
		logger.info("Data Intake: competition COMPLETE")

		# format game data [team, match, referee]
		team_ref_match_main(pl_stats_connector)
		logger.info("\nData Intake: team COMPLETE")
		logger.info("Data Intake: match COMPLETE")
		logger.info("Data Intake: referee COMPLETE")

		# format season schedule [schedule]
		schedule_main(pl_stats_connector)
		logger.info("\nData Intake: schedule COMPLETE")
			
		# format squad data [player, player_team]
		player_main(pl_stats_connector)
		logger.info("\nData Intake: player_team COMPLETE")
		logger.info("Data Intake: player COMPLETE")
			
		# [historic_player_per_ninety]
		per_90_main(pl_stats_connector)
		logger.info("\nData Intake: per_90 COMPLETE")
		logger.info("Data Intake: COMPLETE")
	
		with open("./ingestion_status.txt", "w") as file:
			file.write("Data ingestion completed successfully")

		return "Data ingestion successful"
	
	except Exception as e:
		logger.error(f"Error: {e}")
		return f"Error while ingesting data: {e}"
	

if __name__ == "__main__":
	download_latest_data()
	insert_latest_data()
	app.run(debug=True, host="0.0.0.0", port="8009")

