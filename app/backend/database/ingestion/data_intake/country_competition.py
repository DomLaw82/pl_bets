import pandas as pd
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.utilities.save_to_database import save_to_database
from app_logger import FluentLogger
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("intake-country_competition").get_logger()

def clean_country_competition_data() -> pd.DataFrame:
	"""
	Reads and cleans the country and competition data from CSV files.

	Returns:
		pd.DataFrame: A DataFrame containing the cleaned data.
	"""
	competition_csv_path = "./data/competition.csv"
	country_csv_path = "./data/country.csv"
	try:
		paths = [country_csv_path, competition_csv_path]
		dfs = []

		for path in paths:
			dfs.append(pd.read_csv(path))
			
		return dfs
	except Exception as e:
		logger.error(f"Error: {e}")
		return f"Error: {e}"

def country_competition_main(db_connection):
	"""
	Main function for processing and saving country and competition data to the database.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""
	try:
		dfs = clean_country_competition_data()
		tables = ["country", "competition"]
		comparison_columns = [["name"], ["country_id", "name"]]
		
		for idx, df in enumerate(dfs):
			deduplicated_df = remove_duplicate_rows(db_connection, df, comparison_columns[idx], tables[idx])
			if not deduplicated_df.empty:
				save_to_database(db_connection, deduplicated_df, tables[idx])
				logger.info(f"Inserted into {tables[idx]} table.")
	except Exception as e:
		logger.error(f"Error on ingestion at country_competition: {e}")
		return f"Error on ingestion at country_competition: {e}"
		

# TODO - Add logging for more visibility of data_intake process