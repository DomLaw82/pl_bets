import pandas as pd
from db_connection import SQLConnection
from create_dataset import create_dataset
import os

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

def recreate_local_dataset():	
	df = create_dataset()
	df.to_csv("../files/final_combined_dataframe.csv", index=False)

if __name__ == "__main__":
	recreate_local_dataset()