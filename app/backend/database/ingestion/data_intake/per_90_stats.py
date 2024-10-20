import os, pandas as pd
from data_intake.utilities.unique_id import get_id_from_name
from app_logger import FluentLogger
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("intake-per_90").get_logger()

def combining_datasets(season: str) -> pd.DataFrame:
	"""
	Combines multiple datasets for a given season into a single DataFrame.

	Parameters:
		season (str): The season for which the datasets are being combined.

	Returns:
		pd.DataFrame: The combined dataset.

	"""
	columns = {
		"goalkeeping.csv": ['player', 'nation','position','team','goals_against','shots_on_target_against','saves','wins','draws','losses','clean_sheets','penalties_faced','penalties_allowed','penalties_saved','penalties_missed'],
		"passing.csv": ['player', 'nation','position','team','total_passing_distance','total_progressive_passing_distance','short_passes_completed','short_passes_attempted','medium_passes_completed','medium_passes_attempted','long_passes_completed','long_passes_attempted','expected_assisted_goals','expected_assists','assists-expected_assisted_goals','key_passes','passes_into_final_third','passes_into_penalty_area','crosses_into_penalty_area','progressive_passes'],
		"shooting.csv": ['player', 'nation', 'position','team','shots','shots_on_target','goals_per_shot','goals_per_shot_on_target','average_shot_distance','shots_from_free_kicks','penalties_made','non_penalty_expected_goals_per_shot','goals-expected_goals','non_penalty_goals-non_penalty_expected_goals'],
		"defensive_actions.csv": ['player', 'nation', 'position','team','tackles','tackles_won','defensive_third_tackles','middle_third_tackles','attacking_third_tackles','dribblers_tackled','dribbler_tackles_attempted','shots_blocked','passes_blocked','interceptions','clearances','errors_leading_to_shot'],
		"possession.csv": ['player', 'nation','position','team','touches','touches_in_defensive_penalty_area','touches_in_defensive_third','touches_in_middle_third','touches_in_attacking_third','touches_in_attacking_penalty_area','live_ball_touches','take_ons_attempted','take_ons_succeeded','times_tackled_during_take_on','carries','total_carrying_distance','progressive_carrying_distance','carries_into_final_third','carries_into_penalty_area','miscontrols','dispossessed','passes_received', "progressive_passes_received"],
		"standard.csv": ['player', 'nation', 'position','team','matches_played','starts','minutes_played','ninetys','goals','assists','direct_goal_contributions','non_penalty_goals','penalties_scored','penalties_attempted','yellow_cards','red_cards','expected_goals','non_penalty_expected_goals','non_penalty_expected_goals+expected_assisted_goals','progressive_carries']
	}
	try:
		data_folder_path = "./data/historic_player_stats"
		season_folder = os.path.join(data_folder_path, season)

		datasets = sorted(os.listdir(season_folder))
		complete = pd.DataFrame()
		for dataset in datasets:
			if dataset == ".DS_Store":
				continue
			dataset_path = os.path.join(season_folder, dataset)

			df = pd.read_csv(dataset_path)
			df = df[columns[dataset]]

			if complete.empty:
				complete = df.copy(deep=True)
			else:
				complete = complete.merge(df, on=["player", "nation", "position", "team"], how='left')

		return complete
	except Exception as e:
		logger.error(f"Error: {e}")
		return e

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
	try:
		goalkeeping_columns = ["goals_against", "shots_on_target_against", "saves", "wins", "draws", "losses", "clean_sheets", "penalties_faced", "penalties_allowed", "penalties_saved", "penalties_missed"]

		df["team"] = df["team"].apply(lambda team_name: get_id_from_name(db_connection, team_name, "team"))

		df = df.rename(columns={"team": "team_id"})
		df[goalkeeping_columns] = df[goalkeeping_columns].fillna(0)

		df["player"] = df["player"].apply(lambda player_name: get_id_from_name(db_connection, player_name, "player"))

		df = df.rename(columns={"player": "player_id"})
		df.columns = [x.replace("+", "_plus_").replace("/", "_divided_by_").replace("-", "_minus_") for x in df.columns.tolist()]

		df.loc[:, "season"] = season

		df["nation"] = df["nation"].str.split(" ").str[1]
		df = df.rename(columns={"nation": "nationality"})

		exclude_columns = ['team_id', 'player_id']
		columns_to_fill = df.columns.difference(exclude_columns)
		df[columns_to_fill] = df[columns_to_fill].fillna(0)

		df = df.drop(columns=["position", "wins", "draws", "losses"])
		# 	TODO - More granular method to impute nulls
		# 	TODO - Null and multiple player ids
	except Exception as e:
		raise Exception(e)

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
	try:
		with db_connection.connect() as conn:
			df.to_sql("historic_player_per_ninety", conn, if_exists="append", index=False)
	except Exception as e:
		raise Exception(e)
	
def check_existing_player_for_team(db_connection, player_id: str, team_id: str, season: str) -> bool:
	"""
	Check if the player exists in the database with a different team id than the one provided.

	Parameters:
		db_connection (DBConnection): The database connection object.
		player_id (str): The player id.
		team_id (str): The team id.
		season (str): The season.

	Returns:
		bool: True if the player exists with a different team id, False otherwise.
	"""
	try:
		# Checking to see if the team_id provided is the team_id for the players current team
		teams_played_for_in_season = db_connection.get_list(f"""
			SELECT team_id FROM historic_player_per_ninety
			WHERE player_id = '{player_id}' AND season = '{season}'
		""")
		teams_played_for_in_season = [team[0] for team in teams_played_for_in_season]

		if team_id not in teams_played_for_in_season:
			return False
		
		return True
	except Exception as e:
		raise Exception(e)

def update_database(db_connection, data: list[dict]):
	"""
	Update the per 90 stats in the database.

	Parameters:
		db_connection (DBConnection): The database connection object.
		data (list[dict]): The list of dictionaries containing the data to be updated.

	Returns:
		None
	"""
	try:
		for row in data:
			player_id = row["player_id"]
			team_id = row["team_id"]
			season = row["season"]

			existing_player_for_team = check_existing_player_for_team(db_connection, player_id, team_id, season)

			if existing_player_for_team:
				for key, value in row.items():
					if key in ["player_id", "team_id", "season"]:
						continue
					db_connection.execute(f"""
						UPDATE historic_player_per_ninety
						SET {key} = {value}
						WHERE player_id = '{player_id}' AND season = '{season}'
					""")
			else:
				# 	TODO - Handle this case
				number_of_teams_played_for_this_season = db_connection.get_list(f"""
					SELECT MAX(number_team_in_season) FROM player_team
					WHERE player_id = '{player_id}' AND season = '{season}'
				""")[0][0]
				db_connection.execute(f"""
					INSERT INTO player_team VALUES ('{player_id}', '{team_id}', '{season}', {int(number_of_teams_played_for_this_season) + 1})
				""")
				df_row = pd.DataFrame([row])
				save_to_database(db_connection, df_row)
	except Exception as e:
		raise Exception(e)

def per_90_main(db_connection):
	"""
	Main function for processing and ingesting per 90 stats data into the database.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""

	try:
		data_folder_path = "./data/historic_player_stats"

		seasons = sorted(os.listdir(data_folder_path))
		
		for season in seasons:
			if season == ".DS_Store":
				continue
			df = combining_datasets(season)
			df = clean_historic_stats_df(db_connection, df, season)
			df = df.drop_duplicates()
			duplicates = df[df.duplicated(subset=["player_id", "team_id", "season"], keep=False)]
			if not duplicates.empty:
				logger.info("Duplicates found:")
				logger.info(duplicates)
				print(duplicates)
			else:
				logger.info("No duplicates found.")
			save_to_database(db_connection, df)
			logger.info(f"Inserted into historic_player_per_ninety table for {season}.")
	except Exception as e:
		logger.error(f"Error with per 90 stats: {e}")
		raise Exception(e)

def per_90_update(db_connection, season: str) -> None:
	"""
	Update function for processing and ingesting per 90 stats data into the database.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""
	try:
		df = combining_datasets(season)
		df = clean_historic_stats_df(db_connection, df, season)
		data = df.to_dict(orient='records')
		update_database(db_connection, data)
		logger.info(f"Inserted into historic_player_per_ninety table for {season}.")
	except Exception as e:
		logger.error(f"Error with per 90 stats: {e}")
		raise Exception(e)