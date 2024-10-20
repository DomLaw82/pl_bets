import pandas as pd
from db_connection import SQLConnection
from create_dataset import create_training_dataset
import os
from dotenv import load_dotenv
from app_logger import FluentLogger
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))
logger = FluentLogger("predict-refresh_local_dataset").get_logger()

def recreate_local_dataset():
	try:
		df = create_training_dataset(db)
		df.to_csv("../files/final_combined_dataframe.csv", index=False)
		logger.info("Local dataset recreated successfully")
		return {"message": "success", "code": 200}
	except Exception as e:
		logger.error(f"Error recreating local dataset: {e}")
		return {"message": f"Error: {e}", "code": 500}