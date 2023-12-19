import pandas as pd
import os
from utilities.unique_id import get_team_id
from team_ref_match import rename_team_name


def clean_schedule_data(db_connection) -> pd.DataFrame:
	season_schedule_folder_path = "./app/data/schedule_data"

	season_schedules = sorted(os.listdir(season_schedule_folder_path))

	for season in season_schedules:
		path = season_schedule_folder_path + "/" + season
		df = pd.read_csv(path)
		df.columns = ["_".join(col.lower().split(" ") )for col in df.columns.to_list()]

		df.loc[:, "home_team"] = df.apply(lambda row: rename_team_name(row.home_team.title()), axis=1)
		df.loc[:, "away_team"] = df.apply(lambda row: rename_team_name(row.away_team.title()), axis=1)
		
		df.loc[:, "home_team"] = df.apply(lambda row: get_team_id(db_connection, row.home_team), axis=1)
		df.loc[:, "away_team"] = df.apply(lambda row: get_team_id(db_connection, row.away_team), axis=1)

def save_to_database(db_connection, df: pd.DataFrame) -> None:
	df.to_sql("schedule", db_connection.conn, if_exists="append", index=False)

def schedule_main(db_connection) -> None:
	df = clean_schedule_data(db_connection)
	save_to_database(db_connection, df)


