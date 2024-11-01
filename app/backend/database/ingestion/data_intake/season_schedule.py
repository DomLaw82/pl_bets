import pandas as pd
import numpy as np
import os, time
from data_intake.utilities.unique_id import get_id_from_name, get_name_from_database
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from app_logger import FluentLogger
from db_connection import SQLConnection
from datetime import datetime
from elo_ratings import get_team_elo_rating
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("intake-season_schedule").get_logger()
SCHEDULE_SAVE_PATH_ROOT = "data/schedule_data/"
SEASON_END_YEAR = datetime.now().year + 2 if datetime.now().month > 8 else datetime.now().year + 1
FIXTURE_SEASON_ARRAY = [str(year) for year in range(2017, SEASON_END_YEAR, 1)]
LEAGUES = ["epl", "championship"]


competition_name_conversion = {
    "epl": "English Premier League",
    "championship" : "EFL Championship"
}

def download_all_fixture_data():
	"""
	Downloads match facts for every game for the specified season data as a single csv

	Arguments:
		season (str): last 2 digits of each year the season encompasses, e.g. "16/17"
	"""

	for season in FIXTURE_SEASON_ARRAY:
		time.sleep(0.2)
		for league in LEAGUES:
			time.sleep(0.2)
			DOWNLOAD_FIXTURE_URL_ROOT = f"https://fixturedownload.com/download/{league}-" # add on the year the season starts in, i.e. 2024
			try:
				GMT_URL = f"{DOWNLOAD_FIXTURE_URL_ROOT}{season}-GMTStandardTime.csv"
				UTC_URL = f"{DOWNLOAD_FIXTURE_URL_ROOT}{season}-UTC.csv"
				logger.debug(f"Downloading {league} fixture CSV file for season {season}")

				data = pd.read_csv(GMT_URL)
				logger.info(f'Attempted to download GMT {league} fixture CSV file for season {season}: {GMT_URL}')

				if data.empty:
					data = pd.read_csv(UTC_URL)
					logger.info(f'Attempted to download UTC {league} fixture CSV file for season {season}: {UTC_URL}')
				
				file_name = f"{league}_{season}-{str(int(season) + 1)[-2:]}.csv"
				save_path = os.path.join(SCHEDULE_SAVE_PATH_ROOT, file_name)
				data.to_csv(save_path)
				logger.info(f'Fixture CSV file for season {season} downloaded and saved to {save_path}')

			except Exception as e:
				logger.error(f'An error occurred while downloading {league} fixtures for season {season}: {str(e)}')
				continue

def add_elo_to_df(base_df: pd.DataFrame, df: pd.DataFrame, team_name: str) -> pd.DataFrame:
	try:
		home_team_df = df[df['home_team'] == team_name]
		away_team_df = df[df['away_team'] == team_name]

		home_team_df["date_no_time"] = pd.to_datetime(home_team_df["date"]).dt.strftime("%Y-%m-%d")
		away_team_df["date_no_time"] = pd.to_datetime(away_team_df["date"]).dt.strftime("%Y-%m-%d")

		elos = get_team_elo_rating(team_name)[["Date", "Club", "Elo", "From", "To"]]

		if not elos.empty:
			print(f"All home game dates in elos for {team_name}: " + str(all(home_team_df["date_no_time"].isin(elos["Date"].unique()).values)))
			print(f"All away game dates in elos for {team_name}: " + str(all(away_team_df["date_no_time"].isin(elos["Date"].unique()).values)))

			home_team_df_index = home_team_df.index
			home_team_df = home_team_df.merge(elos[["Date", "Club", "Elo"]], left_on=['date_no_time', 'home_team'], right_on=['Date', 'Club'], how='left', validate="1:1", suffixes=(None, '_elos_home'))
			home_team_df = home_team_df.rename(columns={"Elo": "home_elo"})
			home_team_df["away_elo"] = np.nan
			home_team_df = home_team_df.set_index(home_team_df_index, drop=True)

			away_team_df_index = away_team_df.index
			away_team_df = away_team_df.merge(elos[["Date", "Club", "Elo"]], left_on=['date_no_time', 'away_team'], right_on=['Date', 'Club'], how='left', validate="1:1", suffixes=(None, '_elos_away'))
			away_team_df = away_team_df.rename(columns={"Elo": "away_elo"})
			away_team_df["home_elo"] = np.nan
			away_team_df = away_team_df.set_index(away_team_df_index, drop=True)

			team_df = pd.concat([home_team_df[base_df.columns], away_team_df[base_df.columns]]).sort_values(by=["date"])
			pd.set_option('display.max_columns', None)

			print(team_df.head())

			# team_df["home_elo"] = team_df["home_elo"].fillna(team_df["home_elo"].rolling(window=3, min_periods=1).mean())
			# team_df["away_elo"] = team_df["away_elo"].fillna(team_df["away_elo"].rolling(window=3, min_periods=1).mean())
			
			print(f"Team df for {team_name}:")

			base_df.update(team_df[base_df.columns])
			logger.info(f"Inserted ELO ratings for {team_name}.")
		return base_df
	except Exception as e:
		logger.error(f"Error adding ELOs to df for {team_name} at line {e.__traceback__.tb_lineno}: {e}")
		print(f"Error adding ELOs to df for {team_name} at line {e.__traceback__.tb_lineno}: {e}")
		raise Exception(f"Error adding ELOs to df for {team_name} at line {e.__traceback__.tb_lineno}: {e}")


def clean_schedule_data(db_connection: SQLConnection, df: pd.DataFrame) -> pd.DataFrame:
	# Rename columns to lowercase with underscores
	try:
		df.columns = df.columns.str.lower().str.replace(" ", "_")

		# Rename team names in 'home_team' and 'away_team' columns
		unique_teams = pd.Series(pd.concat([df["home_team"], df["away_team"]]).unique())
		
		team_replacements = unique_teams.apply(lambda team: get_name_from_database(db_connection, team, "team"))
		team_replacement_dict = dict(zip(unique_teams, team_replacements))
		df["home_team"] = df["home_team"].replace(team_replacement_dict)
		df["away_team"] = df["away_team"].replace(team_replacement_dict)

		# Update unique_teams after renaming
		unique_teams = pd.Series(pd.concat([df["home_team"], df["away_team"]]).unique())

		# Convert 'date' column to datetime format
		df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y %H:%M").dt.strftime("%Y/%m/%d %H:%M")

		# Add season column based on date
		df["season"] = pd.to_datetime(df["date"]).apply(lambda x: f"{x.year}-{x.year+1}" if x.month >= 8 else f"{x.year-1}-{x.year}")

		updated_df = df.copy()
		updated_df["home_elo"] = np.nan
		updated_df["away_elo"] = np.nan

		for team_name in unique_teams:
			try:
				updated_df = add_elo_to_df(updated_df, df, team_name)
			except Exception as e:
				logger.error(f"Error inserting ELOs for {team_name} at line {e.__traceback__.tb_lineno}: {e}")
				print(f"Error inserting ELOs for {team_name} at line {e.__traceback__.tb_lineno}: {e}")
				continue
		
		df = updated_df.copy()

		# Retrieve team IDs from the database
		df["home_team"] = df["home_team"].apply(lambda team: get_id_from_name(db_connection, team, "team"))
		df["away_team"] = df["away_team"].apply(lambda team: get_id_from_name(db_connection, team, "team"))

		# Replace null values in 'result' column with "-"
		df["result"] = df["result"].fillna("-")

		# Drop unnecessary columns
		df = df.drop(columns=["location", "match_number"])

		# Rename columns and add competition_id
		df = df.rename(columns={"home_team": "home_team_id", "away_team": "away_team_id"})
		df["competition_id"] = df["league"].apply(lambda x: competition_name_conversion[x])
		df = df.drop(columns=["league"])
		for comp in df["competition_id"].unique():
			df.loc[df["competition_id"] == comp, "competition_id"] = get_id_from_name(db_connection, comp, "competition")

		deduplicated_df = remove_duplicate_rows(db_connection, df, ["round_number", "date", "home_team_id", "away_team_id"], "schedule")
		return deduplicated_df
	except Exception as e:
		raise Exception(e)


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
			df.to_sql("schedule", conn, if_exists="append", index=False)
	except Exception as e:
		raise Exception(e)

def schedule_main(db_connection) -> None:
	"""
	Main function for processing and ingesting season schedule data.

	Args:
		db_connection: The database connection object.

	Returns:
		None
	"""
	season_schedule_folder_path = "./data/schedule_data"
	try:
		all_data = pd.DataFrame()
		for season_schedule_file in os.scandir(season_schedule_folder_path):
			if season_schedule_file.is_file() and season_schedule_file.name.endswith(".csv"):
				file_path = os.path.join(season_schedule_folder_path, season_schedule_file.name)
				df = pd.read_csv(file_path)
				league = season_schedule_file.name.split("_")[0]
				df["league"] = league
				all_data = df if all_data.empty else pd.concat([all_data, df]).reset_index(drop=True)
		df = clean_schedule_data(db_connection, all_data)

		df = df [[
			"competition_id",
			"round_number",
			"date",
			"home_team_id",
			"away_team_id",
			"result",
			"home_elo",
			"away_elo",
			"season"
		]]
		
		if not df.empty:
			df = df.sort_values(by=["date"]).reset_index(drop=True)
			save_to_database(db_connection, df)
			logger.info(f"Inserted into schedule table")
	except Exception as e:
		logger.error(f"Error: {e}")

# TODO - Add logging for more visibility of data_intake process