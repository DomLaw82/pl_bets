from db_connection import local_pl_stats_connector
from data_intake.season_schedule import schedule_main
from data_intake.team_ref_match import team_ref_match_main
from data_intake.player import player_main
from data_intake.country_competition import country_competition_main
from data_intake.per_90_stats import per_90_main
from data_intake.download_latest_data import download_latest_data

def download_and_insert_latest_data():

	download_latest_data()

	print("\n")
	print("--- --- --- --- --- --- --- ---")
	print("---- Ingesting latest data ----")
	print("--- --- --- --- --- --- --- ---")
	print("\n")

	# [country, competition]
	country_competition_main(local_pl_stats_connector)
	print("Data Intake: country COMPLETE")
	print("Data Intake: competition COMPLETE")
	print("--- --- --- --- --- --- --- ---")

	# format game data [team, match, referee]
	team_ref_match_main(local_pl_stats_connector)
	print("Data Intake: team COMPLETE")
	print("Data Intake: match COMPLETE")
	print("Data Intake: referee COMPLETE")
	print("--- --- --- --- --- --- --- ---")

	# format season schedule [schedule]
	schedule_main(local_pl_stats_connector)
	print("Data Intake: schedule COMPLETE")
	print("--- --- --- --- --- --- --- ---")
		
	# format squad data [player, player_team]
	player_main(local_pl_stats_connector)
	print("Data Intake: player_team COMPLETE")
	print("Data Intake: player COMPLETE")
	print("--- --- --- --- --- --- --- ---")
		
	# [historic_player_per_ninety]
	per_90_main(local_pl_stats_connector)
	print("Data Intake: per_90 COMPLETE")
	print("Data Intake: COMPLETE")
	print("--- --- --- --- --- --- --- ---")
	print("--- --- --- --- --- --- --- ---")

if __name__ == "__main__":
	download_and_insert_latest_data()