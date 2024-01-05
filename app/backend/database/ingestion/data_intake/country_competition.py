import pandas as pd
from data_intake.team_ref_match import rename_team_name
from data_intake.utilities.unique_id import get_team_id
import os

def clean_country_competition_data() -> pd.DataFrame:
	"""
	Reads and cleans the country and competition data from CSV files.

	Returns:
		pd.DataFrame: A DataFrame containing the cleaned data.
	"""
	competition_csv_path = "./data/competition.csv"
	country_csv_path = "./data/country.csv"

	paths = [country_csv_path, competition_csv_path]
	dfs = []

	for path in paths:
		dfs.append(pd.read_csv(path))
		
	return dfs
	
def save_to_database(db_connection, df: pd.DataFrame, team_name: str) -> None:
	"""
	Saves the given DataFrame to the database.

	Parameters:
		db_connection (DBConnection): The connection to the database.
		df (pd.DataFrame): The DataFrame to be saved.
		team_name (str): The name of the team.

	Returns:
		None
	"""
	df.to_sql(team_name, db_connection.conn, if_exists="append", index=False)

def country_competition_main(db_connection):
	"""
	Main function for processing and saving country and competition data to the database.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""
	dfs = clean_country_competition_data()
	tables = ["country", "competition"]
	
	for idx, df in enumerate(dfs):
		save_to_database(db_connection, df, tables[idx])