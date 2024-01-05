import pandas as pd
import os, datetime
from data_intake.utilities.unique_id import get_team_id
from data_intake.team_ref_match import rename_team_name


def clean_schedule_data(db_connection, df:pd.DataFrame) -> pd.DataFrame:
	"""
	Cleans the schedule data by performing the following operations:
	1. Renames the columns of the DataFrame to lowercase with underscores instead of spaces.
	2. Renames the team names in the 'home_team' and 'away_team' columns to a standardized format.
	3. Retrieves the team IDs from the database for the 'home_team' and 'away_team' columns.
	4. Removes rows where the 'result' column is null.
	5. Renames the 'home_team' and 'away_team' columns to 'home_team_id' and 'away_team_id' respectively.
	6. Converts the 'date' column to a datetime format and formats it as 'YYYY/MM/DD HH:MM'.

	Parameters:
	- db_connection: The database connection object.
	- df: The input DataFrame containing the schedule data.

	Returns:
	- The cleaned DataFrame.
	"""
	df.columns = ["_".join(col.lower().split(" ") )for col in df.columns.to_list()]

	df.loc[:, "home_team"] = df.apply(lambda row: rename_team_name(row.home_team.title()), axis=1)
	df.loc[:, "away_team"] = df.apply(lambda row: rename_team_name(row.away_team.title()), axis=1)
	
	df.loc[:, "home_team"] = df.apply(lambda row: get_team_id(db_connection, row.home_team), axis=1)
	df.loc[:, "away_team"] = df.apply(lambda row: get_team_id(db_connection, row.away_team), axis=1)

	df = df[~df["result"].isnull()]
	df = df.rename(columns={"home_team": "home_team_id", "away_team": "away_team_id"})
	df.loc[:, "date"] = pd.to_datetime(df['date'], format="%d/%m/%Y %H:%M").dt.strftime('%Y/%m/%d %H:%M')

	return df


def save_to_database(db_connection, df: pd.DataFrame) -> None:
	"""
	Save the given DataFrame to the database.

	Parameters:
		db_connection (DBConnection): The database connection object.
		df (pd.DataFrame): The DataFrame to be saved.

	Returns:
		None
	"""
	df.to_sql("schedule", db_connection.conn, if_exists="append", index=False)

def schedule_main(db_connection) -> None:
	"""
	Main function for processing and ingesting season schedule data.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""
	season_schedule_folder_path = "./data/schedule_data"

	season_schedules = sorted(os.listdir(season_schedule_folder_path))

	for season in season_schedules:
		path = season_schedule_folder_path + "/" + season
		df = pd.read_csv(path)
		df = clean_schedule_data(db_connection, df)
		save_to_database(db_connection, df)


