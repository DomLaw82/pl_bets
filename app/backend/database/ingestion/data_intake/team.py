import pandas as pd
import numpy as np
from app_logger import FluentLogger
from db_connection import SQLConnection
from data_intake.utilities.save_to_database import save_to_database
from data_intake.utilities.unique_id import get_id_from_name

logger = FluentLogger("intake-team").get_logger()
PLAYER_DATA_SAVE_PATH = "./data/player_data/player_data.csv"

# Find a way to get the country_id from team name

def team_main(db_connection: SQLConnection) -> None:
	"""Ingest team data into the database"""
	all_data = pd.read_csv(PLAYER_DATA_SAVE_PATH)
	teams = all_data[["team"]]
	unique_teams = teams.drop_duplicates()
	non_null_teams = unique_teams[unique_teams["team"].notnull()]
	non_null_teams = non_null_teams.rename(columns={"team": "name"})
	non_null_teams["name"] = non_null_teams["name"].apply(lambda name: name.replace("'", "`"))
	# teams["country_id"] = teams["name"].apply(lambda x: get_id_from_name(db_connection, x, "country"))
	# set country_id to c-00001 (England) for now
	non_null_teams["country_id"] = "c-00001"

	# Add some extra Championship teams
	add_teams = [
		{"name": "Colchester United", "country_id": "c-00001"},
		{"name": "Crewe Alexandra", "country_id": "c-00001"},
		{"name": "Doncaster Rovers", "country_id": "c-00001"},
		{"name": "Gillingham", "country_id": "c-00001"},
		{"name": "Milton Keynes Dons", "country_id": "c-00001"},
		{"name": "Scunthorpe United", "country_id": "c-00001"},
		{"name": "Southend United", "country_id": "c-00001"},
		{"name": "Yeovil Town", "country_id": "c-00001"},
		{"name": "AFC Wimbledon", "country_id": "c-00001"},
		{"name": "Bradford City", "country_id": "c-00001"},
		{"name": "Oldham Athletic", "country_id": "c-00001"},
		{"name": "Port Vale", "country_id": "c-00001"},
		{"name": "Salford City", "country_id": "c-00001"},
		{"name": "Stevenage", "country_id": "c-00001"},
		{"name": "Tranmere Rovers", "country_id": "c-00001"},
		{"name": "Walsall", "country_id": "c-00001"},
		{"name": "Swindon Town", "country_id": "c-00001"},
	]
	additional_teams = pd.DataFrame(add_teams, index=list(range(0, len(add_teams))))
	teams = pd.concat([non_null_teams, additional_teams], ignore_index=True)
	teams = teams.drop_duplicates(subset=["name"], keep="last")
	all_teams = teams.sort_values(by=["name"], ascending=True)
	print(all_teams)
	save_to_database(db_connection, all_teams, "team")