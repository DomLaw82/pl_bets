import pandas as pd
from db_connection import local_pl_stats_connector
from create_dataset import create_dataset

db = local_pl_stats_connector

def recreate_local_dataset():	
	df = create_dataset()
	df.to_csv("../files/final_combined_dataframe.csv", index=False)

if __name__ == "__main__":
	recreate_local_dataset()