import pandas as pd
import numpy as np
import os
from data_intake.utilities.unique_id import get_team_id
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.team_ref_match import rename_team_name
from app_logger import FluentLogger
import requests
from io import StringIO

logger = FluentLogger("intake-season_schedule").get_logger()

elo_name_conversion = {
	"Manchester City": "ManCity",
	"Arsenal": "Arsenal",
	"Liverpool": "Liverpool",
	"Chelsea": "Chelsea",
	"Newcastle United": "Newcastle",
	"Tottenham Hotspur": "Tottenham",
	"Manchester United": "ManUnited",
	"Aston Villa": "AstonVilla",
	"Crystal Palace": "CrystalPalace",
	"West Ham United": "WestHam",
	"Fulham": "Fulham",
	"Brighton & Hove Albion": "Brighton",
	"Brentford": "Brentford",
	"Everton": "Everton",
	"Bournemouth": "Bournemouth",
	"Wolverhampton Wanderers": "Wolves",
	"Nottingham Forest": "Forest",
	"Leicester City": "Leicester",
	"Southampton": "Southampton",
	"Ipswich Town": "Ipswich",
	"Burnley": "Burnley",
	"Leeds United": "Leeds",
	"Luton Town": "Luton",
	"Middlesbrough": "Middlesbrough",
	"West Bromwich Albion": "WestBrom",
	"Sheffield United": "SheffieldUnited",
	"Norwich City": "Norwich",
	"Hull City": "Hull",
	"Coventry City": "Coventry",
	"Watford": "Watford",
	"Bristol City": "Bristol City",
	"Swansea City": "Swansea",
	"Stoke City": "Stoke",
	"Sheffield Wednesday": "SheffieldWeds",
	"Blackburn Rovers": "Blackburn",
	"Millwall": "Millwall",
	"Sunderland": "Sunderland",
	"Queens Park Rangers": "QPR",
	"Preston North End": "Preston",
	"Plymouth Argyle": "Plymouth",
	"Oxford United": "Oxford",
	"Cardiff City": "Cardiff",
	"Portsmouth": "Portsmouth",
	"Derby County": "Derby",
}

def get_team_elo_rating(team_name: str) -> pd.DataFrame:
	"""
	Get the ELO rating of a team on a specific date.

	Args:
		team_name (str): The name of the team.

	Returns:
		pd.DataFrame: The ELO rating DataFrame of the team on the given date.
	"""
	try:
		elo_team_name = elo_name_conversion.get(team_name, team_name)
		url = f"http://api.clubelo.com/{elo_team_name}"
		logger.info(f"Getting ELO rating for {elo_team_name}: {url}.")
		response = requests.get(url)

		if response.status_code == 200:
			csv_data = StringIO(response.text)
			df = pd.read_csv(csv_data)
			df["Club"] = team_name
			return df
		else:
			logger.error(f"Error finding ELO for {elo_team_name}: {response.status_code}")
			return pd.DataFrame()
	except Exception as e:
		logger.error(f"Error finding ELO for {elo_team_name}: {e}")
		return pd.DataFrame()

def clean_schedule_data(db_connection, df: pd.DataFrame) -> pd.DataFrame:
	# Rename columns to lowercase with underscores
	try:
		df.columns = df.columns.str.lower().str.replace(" ", "_")

		# Rename team names in 'home_team' and 'away_team' columns
		df["home_team"] = df["home_team"].str.title().apply(rename_team_name)
		df["away_team"] = df["away_team"].str.title().apply(rename_team_name)

		# Convert 'date' column to datetime format
		df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y %H:%M").dt.strftime("%Y/%m/%d %H:%M")

		# Add season column based on date
		df["season"] = pd.to_datetime(df["date"]).apply(lambda x: f"{x.year}-{x.year+1}" if x.month >= 8 else f"{x.year-1}-{x.year}")

		updated_df = df.copy()
		updated_df["home_elo"] = 0
		updated_df["away_elo"] = 0

		unique_team_names = df['home_team'].unique().tolist()

		elo_dict = {}

		for team_name in unique_team_names:
			try:
				team_df = df[(df['home_team'] == team_name) | (df['away_team'] == team_name)]
				team_df["date_no_time"] = pd.to_datetime(team_df["date"]).dt.strftime("%Y-%m-%d")
				index = team_df.index
				elos = pd.DataFrame()
				if team_name not in elo_dict:
					elos = get_team_elo_rating(team_name)[["Club", "Elo", "From", "To"]]
					elo_dict[team_name] = elos
				else:
					elos = elo_dict[team_name]

				if not elos.empty:
					elos['From'] = pd.to_datetime(elos['From'])
					elos['To'] = pd.to_datetime(elos['To'])

					elos_expanded = pd.DataFrame({
						'Date': pd.date_range(start=elos['From'].min(), end=elos['To'].max(), freq='D')
					})
					elos_expanded = elos_expanded.merge(elos, left_on='Date', right_on='From', how='left').ffill()
					elos_expanded["Date"] = pd.to_datetime(elos_expanded["Date"]).dt.strftime("%Y-%m-%d")

					team_df = team_df.merge(elos_expanded[["Date", "Club", "Elo"]], left_on=['date_no_time', 'home_team'], right_on=['Date', 'Club'], how='left')
					team_df.rename(columns={"Elo": "home_elo"}, inplace=True)

					team_df = team_df.merge(elos_expanded[["Date", "Club", "Elo"]], left_on=['date_no_time', 'away_team'], right_on=['Date', 'Club'], how='left')
					team_df.rename(columns={"Elo": "away_elo"}, inplace=True)

					if 'Date' in team_df.columns:
						team_df.drop(columns=['Date'], inplace=True)
					if 'Club_x' in team_df.columns:
						team_df.drop(columns=['Club_x', 'Club_y'], inplace=True)
					team_df.index = index

					updated_df.update(team_df)
					logger.info(f"Inserted ELO ratings for {team_name}.")
			except Exception as e:
				logger.error(f"Error inserting ELOs for {team_name} at line {e.__traceback__.tb_lineno}: {e}")
				continue
		
		df = updated_df.copy()

		# Retrieve team IDs from the database
		df["home_team"] = df["home_team"].apply(lambda team: get_team_id(db_connection, team))
		df["away_team"] = df["away_team"].apply(lambda team: get_team_id(db_connection, team))

		# Replace null values in 'result' column with "-"
		df["result"] = df["result"].fillna("-")

		# Drop unnecessary columns
		df = df.drop(columns=["location", "match_number"])

		# Rename columns and add competition_id
		df = df.rename(columns={"home_team": "home_team_id", "away_team": "away_team_id"})
		df["competition_id"] = "x-00001"

		deduplicated_df = remove_duplicate_rows(db_connection, df, ["round_number", "date", "home_team_id", "away_team_id"], "schedule")
		return deduplicated_df
	except Exception as e:
		raise e


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
		df = df.sort_values(by=["date"]).reset_index(drop=True)
		with db_connection.connect() as conn:
			df.to_sql("schedule", conn, if_exists="append", index=False)
	except Exception as e:
		raise e

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
		for season_schedule_file in os.scandir(season_schedule_folder_path):
			if season_schedule_file.is_file() and season_schedule_file.name.endswith(".csv"):
				file_path = os.path.join(season_schedule_folder_path, season_schedule_file.name)
				df = pd.read_csv(file_path)
				df = clean_schedule_data(db_connection, df)
				
				if not df.empty:
					save_to_database(db_connection, df)
					logger.info(f"Inserted into schedule table for {season_schedule_file.name}")
	except Exception as e:
		logger.error(f"Error: {e}")

# TODO - Add logging for more visibility of data_intake process