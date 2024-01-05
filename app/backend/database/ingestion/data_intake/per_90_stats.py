import os, pandas as pd
from data_intake.utilities.unique_id import get_player_id_per_ninety, get_team_id

def combining_datasets(season: str) -> pd.DataFrame:
	"""
	Combines multiple datasets for a given season into a single DataFrame.

	Parameters:
		season (str): The season for which the datasets are being combined.

	Returns:
		pd.DataFrame: The combined dataset.

	"""
	data_folder_path = "./data/historic_player_stats"
	season_folder = data_folder_path + "/" + season

	datasets = sorted(os.listdir(season_folder))
	complete = pd.DataFrame()
	for dataset in datasets:
		dataset_path = season_folder + "/" + dataset

		df = pd.read_csv(dataset_path)
		if complete.empty:
			complete = df.copy(deep=True)
		else:
			complete = complete.merge(df, on=["player", "position", "team"], how='left')

	return complete

def clean_historic_stats_df(db_connection, df: pd.DataFrame, season: str) -> pd.DataFrame:
	"""
	Cleans the historic stats dataframe by removing unnecessary columns, 
	transforming column names, filling missing values, and renaming columns.

	Args:
		db_connection: The database connection object.
		df (pd.DataFrame): The input dataframe containing the historic stats.
		season (str): The season for which the stats are being cleaned.

	Returns:
		pd.DataFrame: The cleaned dataframe.
	"""
	goalkeeping_columns = ["goals_against", "shots_on_target_against", "saves", "wins", "draws", "losses", "clean_sheets", "penalties_faced", "penalties_allowed", "penalties_saved", "penalties_missed"]

	columns_to_remove = ["position"]
	df = df.drop(columns=columns_to_remove)

	df["team"] = df.apply(lambda row: get_team_id(db_connection, row.team), axis=1)

	df = df.drop(columns=["goals_y", "expected_assisted_goals_y", "progressive_passes_y"])
	df = df.rename(columns={"team": "team_id", "goals_x": "goals", "expected_assisted_goals_x": "expected_assisted_goals", "progressive_passes_x": "progressive_passes"})
	df[goalkeeping_columns] = df[goalkeeping_columns].fillna(0)

	df[["first_name", "last_name"]] = df["player"].str.split(pat=" ", n=1, expand=True).fillna('').astype(str)
	df.loc[:, "player"] = df.apply(lambda row: get_player_id_per_ninety(db_connection, row), axis=1)

	df = df.rename(columns={"player": "player_id", "90s": "ninetys"})
	df.columns = [x.replace("+", "_plus_").replace("/", "_divided_by_").replace("-", "_minus_") for x in df.columns.tolist()]

	df.loc[:, "season"] = season

	df = df.drop(columns=["first_name", "last_name", "starts", "matches_played", "wins", "draws", "losses"])
	# 	TODO - More granular method to impute nulls
	# 	TODO - Null and multiple player ids
	df = df.fillna({col: 0 for col in df.columns if col not in ['player_id', 'team_id']})

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
	df.to_sql("historic_player_per_ninety", db_connection.conn, if_exists="append", index=False)

def per_90_main(db_connection):
	"""
	Main function for processing and ingesting per 90 stats data into the database.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""
	data_folder_path = "./data/historic_player_stats"

	seasons = sorted(os.listdir(data_folder_path))

	for season in seasons:

		df = combining_datasets(season)
		df = clean_historic_stats_df(db_connection, df, season)
		save_to_database(db_connection, df)