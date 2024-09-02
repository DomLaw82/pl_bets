import pandas as pd
from app_logger import FluentLogger
from db_connection import SQLConnection

log_class = FluentLogger("intake-save_to_database")
logger = log_class.get_logger()

def save_to_database(db_connection: SQLConnection, df: pd.DataFrame, table_name: str) -> None:
	"""
	Saves a DataFrame to a database table.

	Args:
		db_connection: The database connection object.
		df: The DataFrame to be saved.
		table_name: The name of the table to save the DataFrame to.

	Returns:
		None
	"""
	try:
		with db_connection.connect() as conn:
			logger.debug(f"Inserting into table {table_name}, Dataframe shape: {df.shape}")
			df.to_sql(table_name, conn, if_exists="append", index=False)
	except Exception as e:
		log_class.log_error(e)
		raise e