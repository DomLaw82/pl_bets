import pandas as pd
import os
from data_intake.utilities.unique_id import get_team_id
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.team_ref_match import rename_team_name
from app_logger import FluentLogger

logger = FluentLogger("intake-season_schedule").get_logger()

def clean_schedule_data(db_connection, df: pd.DataFrame) -> pd.DataFrame:
	# Rename columns to lowercase with underscores
	try:
		df.columns = df.columns.str.lower().str.replace(" ", "_")

		# Rename team names in 'home_team' and 'away_team' columns
		df["home_team"] = df["home_team"].str.title().apply(rename_team_name)
		df["away_team"] = df["away_team"].str.title().apply(rename_team_name)

		# Retrieve team IDs from the database
		df["home_team"] = df["home_team"].apply(lambda team: get_team_id(db_connection, team))
		df["away_team"] = df["away_team"].apply(lambda team: get_team_id(db_connection, team))

		# Replace null values in 'result' column with "-"
		df["result"] = df["result"].fillna("-")

		# Drop unnecessary columns
		df = df.drop(columns=["location", "match_number"])

		# Rename columns and add competition_id
		df = df.rename(columns={"home_team": "home_team_id", "away_team": "away_team_id"})
		df["competition_id"] = "x-00001"

		# Convert 'date' column to datetime format
		df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y %H:%M").dt.strftime("%Y/%m/%d %H:%M")

		deduplicated_df = remove_duplicate_rows(db_connection, df, ["round_number", "date", "home_team_id", "away_team_id"], "schedule")


		return deduplicated_df
	except Exception as e:
		raise e


def save_to_database(db_connection, df: pd.DataFrame) -> None:
	"""
	Save the given DataFrame to the database.

	Parameters:
		db_connection (DBConnection): The database connection object.
		df (pd.DataFrame): The DataFrame to be saved.

	Returns:
		None
	"""
	try:
		with db_connection.connect() as conn:
			df.to_sql("schedule", conn, if_exists="append", index=False)
	except Exception as e:
		raise e

def schedule_main(db_connection) -> None:
	"""
	Main function for processing and ingesting season schedule data.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""
	season_schedule_folder_path = "./data/schedule_data"
	try:
		for season_schedule_file in os.scandir(season_schedule_folder_path):
			if season_schedule_file.is_file() and season_schedule_file.name.endswith(".csv"):
				file_path = os.path.join(season_schedule_folder_path, season_schedule_file.name)
				df = pd.read_csv(file_path)
				df = clean_schedule_data(db_connection, df)
				
				if not df.empty:
					save_to_database(db_connection, df)
					logger.info(f"Inserted into schedule table for {season_schedule_file.name}")
	except Exception as e:
		logger.error(f"Error: {e}")

# TODO - Add logging for more visibility of data_intake process