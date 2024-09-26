import bs4
import time
import requests
from datetime import datetime
import pandas as pd
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.utilities.unique_id import get_id_from_name
from data_intake.utilities.save_to_database import save_to_database
from app_logger import FluentLogger
from db_connection import SQLConnection

PLAYER_DATA_SAVE_PATH = "./data/player_data/player_data.csv"
CURRENT_SEASON_END_YEAR = datetime.now().year + 2 if datetime.now().month > 8 else datetime.now().year + 1
PLAYER_DATA_DOWNLOAD_SEASONS = list(range(2017, CURRENT_SEASON_END_YEAR))

LEAGUES = ["Premier-League", "Championship"]

log_class = FluentLogger("intake-player")
logger = log_class.get_logger()

def get_player_fbref_data(url: str, season: str, league: str) -> list|None:
	"""Get player data from FBRef for a specific season"""

	response = requests.get(url)
	log_class.log_http_request(url, response)
	results = []

	# Check if the request was successful
	if response.status_code == 200:
		# Parse the HTML content
		soup = bs4.BeautifulSoup(response.text, 'html.parser')
		table_data = None
		comments = soup.find_all(string=lambda text: isinstance(text, bs4.Comment))
		logger.debug(f'Found {len(comments)} comments in the HTML content.')

		# Look for the specific div in the comments
		for comment in comments:
			comment_soup = bs4.BeautifulSoup(comment, 'html.parser')
			div_standard_stats = comment_soup.find('div', id='div_stats_standard')
			if not div_standard_stats:
				continue
			table_data = div_standard_stats.find('table')
			logger.debug('Found the div with the class "all-stats-standard".')
			break
		
		# Find the div with the class 'all-stats-standard'
		div = table_data
		
		# Find the table within the div
		if div:
			# Find the rows in the table
			name_col = div.find_all('td', {'data-stat': 'player'})
			match_logs_col = div.find_all('td', {'data-stat': 'matches'})
			position_col = div.find_all('td', {'data-stat': 'position'})
			birth_year_col = div.find_all('td', {'data-stat': 'birth_year'})
			nationality_col = div.find_all('td', {'data-stat': 'nationality'})
			team_col = div.find_all('td', {'data-stat': 'team'})

			player_name = ""
			player_href = ""
			id = ""
			match_logs_href = ""

			if len(name_col) < 1:
				logger.error(f'Failed to find the player column in {league} for season {season}.')
				return None
			logger.debug(f'Found {len(name_col)} players in {league} for season {season}.')

			for idx in range(len(name_col)):
				try:
					try:
						player_name = name_col[idx].find('a').get_text()
					except Exception:
						player_name = ""

					try:
						id = name_col[idx].get('data-append-csv')
					except Exception:
						id = ""

					try:
						position = position_col[idx].get_text()
					except Exception:
						position = ""

					try:
						match_logs_href = match_logs_col[idx].find('a')['href']
					except Exception:
						match_logs_href = ""

					try:
						year_of_birth = birth_year_col[idx].get_text()
					except Exception:
						year_of_birth = ""

					try:
						nationality = nationality_col[idx].find('a').find('span').get_text()
					except Exception:
						nationality = ""

					try:
						team = team_col[idx].find('a')["href"].split("/")[-1]
						team = team.removesuffix("-Stats").replace("-", " ")
					except Exception:
						team = ""
				except Exception as e:
					logger.error(f"Failed to extract player data in {league} for season {season} - player {name_col[idx].find('a').get_text()}")
					continue

				# print({
				# 	'season': season,
				# 	'player_name': player_name,
				# 	'position': position,
				# 	'team': team,
				# 	"nationality": nationality,
				# 	'birth_year': year_of_birth,
				# 	'fbref_match_logs_href': "https://fbref.com" + match_logs_href,
				# 	'fbref_id': id
				# })
				results.append({
					'season': season,
					'player_name': player_name,
					'position': position,
					'team': team,
					"nationality": nationality,
					'birth_year': year_of_birth,
					'fbref_match_logs_href': "https://fbref.com" + match_logs_href,
					'fbref_id': id
				})

			return results
		else:
			logger.error(f'Failed to find the div in {league} for season {season}.')
			return None
	else:
		logger.error(f'Failed to retrieve the HTML content in {league} for season {season}.')
		return None
	
def download_player_data() -> None:
	"""Download player data from FBRef and save it to a CSV file"""
	all_results = []

	# Iterate through the seasons from 2000-2001 to 2024-2025
	url_number = {
		"Premier-League": "9",
		"Championship": "10"
	}
	for year in PLAYER_DATA_DOWNLOAD_SEASONS:
		time.sleep(5)
		for league in LEAGUES:
			time.sleep(5)
			try:
				season = f"{year}-{str(year + 1)}"
				url = f'https://fbref.com/en/comps/{url_number[league]}/{season}/stats/{season}-{league}-Stats'
				logger.debug(f'Processing player data in {league} for season {season} at URL: {url}')
				
				season_results = get_player_fbref_data(url, season, league)
				# Check if the request was successful
				if season_results is None:
					continue
				all_results.extend(season_results)

			except Exception as e:
				logger.error(f'An error occurred while processing {league} for season {season}: line {e.__traceback__.tb_lineno} : {e}')

	# Convert the results to a DataFrame
	df = pd.DataFrame(all_results)
	df = df.drop_duplicates(subset=['fbref_id', 'season'], keep='first')
	df = df[['fbref_id', 'player_name', 'team', 'position', 'birth_year', 'nationality', 'fbref_match_logs_href', 'season']]

	# Save the results to a CSV file
	df.to_csv(PLAYER_DATA_SAVE_PATH, index=False)
	logger.debug(F'Player data saved to CSV file at {PLAYER_DATA_SAVE_PATH}')

def player_to_db_main(db_connection: SQLConnection):
	"""Ingest local player data and save player data to database

	Args:
		db_connection (SQLConnection): Postgres database connection object

	Raises:
		e: Exception
	"""
	try:
		data = pd.read_csv(PLAYER_DATA_SAVE_PATH)
		data = data.sort_values(by=["season"], ascending=True)

		# Player Table
		player_df = data[["fbref_id", "player_name", "birth_year", "position", "nationality", "fbref_match_logs_href"]]
		player_df[['first_name', 'last_name']] = player_df['player_name'].str.split(' ', n=1, expand=True)
		player_df['last_name'] = player_df['last_name'].fillna('')
		player_df[["first_name", "last_name"]] = player_df[["first_name", "last_name"]].replace("'", "`")
		player_df = player_df.drop_duplicates(subset=["fbref_id"], keep="last")
		player_df = player_df.drop("player_name", axis=1)
		logger.debug(f"Players with nulls: {player_df[player_df.isnull().any(axis=1)]}")
		player_df = player_df.fillna("")
		logger.debug(f"Player data shape: {player_df.shape}")
		save_to_database(db_connection, player_df, "player")

		# Player Team Table
		player_team_df = data[["player_name", "team", "season"]]
		player_team_df.rename(columns={"team": "team_id"}, inplace=True)
		# Get the team id from the team name
		for team in player_team_df["team_id"].unique():
			team_id = get_id_from_name(db_connection, team, "team")
			player_team_df.loc[player_team_df["team_id"] == team, "team_id"] = team_id
		# Get the player id from the player name
		player_team_df.rename(columns={"player_name": "player_id"}, inplace=True)
		for name in player_team_df["player_id"].unique():
			player_id = get_id_from_name(db_connection, name, "player")
			player_team_df.loc[player_team_df["player_id"] == name, "player_id"] = player_id
		print(player_team_df[(player_team_df["team_id"].isnull())|(player_team_df["player_id"].isnull())])
		player_team_df.dropna(inplace=True)
		save_to_database(db_connection, player_team_df, "player_team")

	except Exception as e:
		log_class.log_error(e)
		raise e
