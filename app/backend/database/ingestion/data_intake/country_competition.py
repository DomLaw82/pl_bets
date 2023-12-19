import pandas as pd
from data_intake.team_ref_match import rename_team_name
from data_intake.utilities.unique_id import get_team_id
import os

def clean_country_competition_data() -> pd.DataFrame:
	competition_csv_path = "./app/data/competition.csv"
	country_csv_path = "./app/data/country.csv"

	paths = [competition_csv_path, country_csv_path]
	dfs = []

	for path in paths:
		dfs.append(pd.read_csv(path))
		
	return dfs
	
def save_to_database(db_connection, df: pd.DataFrame, team_name: str) -> None:
	df.to_sql(team_name, db_connection.conn, if_exists="append", index=False)

def country_competition_main(db_connection):
	dfs = clean_country_competition_data()
	tables = ["competition", "country"]
	
	for idx, df in enumerate(dfs):
		save_to_database(db_connection, df, tables[idx])