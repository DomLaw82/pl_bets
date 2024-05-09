import pandas as pd
from db_connection import SQLConnection
from create_dataset import create_dataset
import os
from app_logger import FluentLogger

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))
logger = FluentLogger("predict-refresh_local_dataset").get_logger()

def recreate_local_dataset():
	try:
		df = create_dataset()
		df.to_csv("../files/final_combined_dataframe.csv", index=False)
		logger.info("Local dataset recreated successfully")
	except Exception as e:
		logger.error(f"Error recreating local dataset: {e}")
		return f"Error: {e}"

if __name__ == "__main__":
	recreate_local_dataset()