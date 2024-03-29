import requests, os, time
from bs4 import BeautifulSoup
import datetime

# DOWNLOADING GAMES DATA FOR EVERY SEASON
SEE_FIXTURES = "https://fixturedownload.com/download/csv/epl-" # + year the season starts in, i.e. 2024

GAME_DATA_DOWNLOAD_ROOT = "https://www.football-data.co.uk/mmz4281/"
DOWNLOAD_FIXTURE_URL_ROOT = "https://fixturedownload.com/download/epl-" # add on the year the season starts in, i.e. 2024
PLAYER_DOWNLOAD_ROOT = "https://www.footballsquads.co.uk/eng/"


current_year = datetime.datetime.now().year

FIXTURE_SEASON_ARRAY = [str(year) for year in range(2017, current_year, 1)]
SEASONS_ARRAY = [f"{str(year-1)}-{str(year)}/" for year in range(2017, current_year+1)]
MATCH_SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2018, current_year+1)]

def download_csv_for_all_games_in_a_season(season: str, url: str, save_path_root: str):
	"""
	Downloads match facts for every game for the specified season data as a single csv

	Arguments:
		season (str): last 2 digits of each year the season encompasses, e.g. "16/17"
	"""
	  
	try:
		# MATCH_SITE_SEASONS
		save_path = os.path.join(save_path_root, f"E0 - {season}.csv")
		url = url+season+'/E0.csv'
		response = requests.get(url)
		if response.status_code == 200:
			csv_data = response.text
			with open(save_path, 'w') as file:
				file.write(csv_data)
			print(f'Game csv file for season {season} downloaded and saved to {save_path}')
			return True
		else:
			print(f'Failed to download the CSV file for season {season}. Status code:', response.status_code)
			return False
	except Exception as e:
		print(f'An error occurred while downloading games for season {season}:', str(e))
		return False
	
def get_page_soup(html_text):
	"""
	Parses the given HTML text and returns a BeautifulSoup object.

	Parameters:
	html_text (str): The HTML text to be parsed.

	Returns:
	BeautifulSoup: A BeautifulSoup object representing the parsed HTML.
	"""
	return BeautifulSoup(html_text, "html.parser")

def get_all_teams_for_season(soup) -> list:
	"""
	Extracts the names and hrefs of all teams for a given season from the provided soup object.

	Parameters:
	soup (BeautifulSoup): The BeautifulSoup object containing the HTML data.

	Returns:
	list: A list of tuples, where each tuple contains the team name and its corresponding href.
	"""
	h5_elements = soup.find_all("h5")
	team_names = [ele.text for ele in h5_elements]
	a_elements = [ele.a for ele in h5_elements]
	hrefs = [ele.get("href") for ele in a_elements]
	return list(zip(team_names, hrefs))

def get_team_squad(endpoint: str, SEASON: str, site_root: str):
	"""
	Retrieves the squad information for a given team and season.

	Args:
		endpoint (str): The endpoint for the squad data.
		SEASON (str): The season for which the squad data is requested.
		site_root (str): The root URL of the website.

	Returns:
		list: A list of lists containing the squad information. Each inner list contains the name, position, and date of birth of a player.
	"""
	squad_url = site_root+SEASON+endpoint
	page_content = requests.get(squad_url).text
	soup = get_page_soup(page_content)
	rows = soup.find_all("tr")[1:]
	
	all_columns = soup.find_all("tr")[0]
	all_column_names = all_columns.find_all("td")
	all_column_names = [elem.text.strip("\n") for elem in all_column_names]

	for idx, row in enumerate(rows):
		if "Players no longer at this club" in str(row):
			rows = rows[:idx]
			break
	
	squad = []
	for row in rows:
		row = row.find_all("td")
		required_cols = [all_column_names.index("Name"), all_column_names.index("Pos"),all_column_names.index("Date of Birth")]
		try:
			squad.append([row[i].text for i in required_cols])
		except:
			continue
	return squad

def download_html_for_squad_player_data(season: str, url_root: str, save_path_root: str):
	"""
	Downloads player data for each season and team.

	This function iterates over each season in the SEASONS_ARRAY and downloads player data for each team in that season.
	It first retrieves the HTML content of the players' website for the given season and league. If the response status
	code is not 200, it tries with the other league. If both requests fail, an exception is raised.

	For each team in the season, it retrieves the squad data by visiting the team's URL. The squad data is then saved
	in a file in the format "./data/squad_data/{SEASON}{team}.html".

	If the directory for the squad data of the current season does not exist, it creates the directory before saving
	the file.

	If any error occurs during the process, the error message along with the season is printed.

	Note: This function requires the SEASONS_ARRAY, url_root, LEAGUE_NAMES, get_all_teams_for_season,
	requests, time, os, and BeautifulSoup to be imported.

	Returns:
		None
	"""
	# Function code here

	LEAGUE_NAMES = ["faprem.htm", "engprem.htm"]

	faprem_url = url_root+season+LEAGUE_NAMES[0]
	engprem_url = url_root+season+LEAGUE_NAMES[1]
	time.sleep(2)

	try:
		response = requests.get(faprem_url)
		if response.status_code != 200:
			response = requests.get(engprem_url)
			if response.status_code != 200:
				raise Exception
		html_content = response.text 
		soup = get_page_soup(html_content)


		teams_links = get_all_teams_for_season(soup)

		for team_link in teams_links:
			team = team_link[0]
			link = team_link[1]

			file_save_path = os.path.join(save_path_root, f"{season}{team}.html")
			year_dir_path = os.path.join(save_path_root, f"{season.replace('/', '')}")

			squad_url = url_root+season+link
			page_content = requests.get(squad_url).text
			if (not os.path.exists(year_dir_path)):
				os.mkdir(year_dir_path) 
			with open(file_save_path, 'w') as file:
				file.write(page_content)
			print(f'Squad csv file for season {season} downloaded and saved to {file_save_path}')
	except Exception as e:
		print(f'An error occurred while downloading squad for season {season}:', str(e))
		print(e)

def download_csv_for_all_fixtures_in_a_season(season: str, url: str, save_path_root: str):
	"""
	Downloads match facts for every game for the specified season data as a single csv

	Arguments:
		season (str): last 2 digits of each year the season encompasses, e.g. "16/17"
	"""
	  
	try:
		response = requests.get(f"{url}{season}-UTC.csv")
		save_path = os.path.join(save_path_root, f"epl_{season}-{str(int(season) + 1)[-2:]}.csv") if response.status_code == 200 else None

		if not save_path:
			response = requests.get(f"{url}{season}-GMTStandardTime.csv")
			save_path = os.path.join(save_path_root, f"epl_{season}-{str(int(season) + 1)[-2:]}.csv") if response.status_code == 200 else None

		if not save_path:
			print(f'Failed to download the fixture CSV file for season {season}. Message:', response.text)
			return False

		with open(save_path, 'w') as file:
			file.write(response.text)

		print(f'Fixture CSV file for season {season} downloaded and saved to {save_path}')
		return True

	except Exception as e:
		print(f'An error occurred while downloading fixtures for season {season}:', str(e))
		return False

def download_latest_data():
	print("\n")
	print("--- --- --- --- --- --- --- ---")
	print("---Fetching latest data---")
	print("--- --- --- --- --- --- --- ---")
	print("\n")
	
	# This code is used to initially download the data from the web, but also to update the data on the fly from the frontend
	GAME_SAVE_PATH_ROOT = "data/game_data/"
	SCHEDULE_SAVE_PATH_ROOT = "data/schedule_data/"
	PLAYER_SAVE_PATH_ROOT = "data/squad_data/"
	
	# Create directories if they don't exist
	for path_root in [GAME_SAVE_PATH_ROOT, SCHEDULE_SAVE_PATH_ROOT, PLAYER_SAVE_PATH_ROOT]:
		if not os.path.exists(path_root):
			os.makedirs(path_root)
	
	# game data download
	print("Downloading game data...")
	for season in MATCH_SITE_SEASONS:
		time.sleep(0.2)
		download_csv_for_all_games_in_a_season(season, GAME_DATA_DOWNLOAD_ROOT, GAME_SAVE_PATH_ROOT)
	print("--- --- --- --- --- --- --- ---\n")
	
	# fixture data download
	print("Downloading fixture data...")
	for season in FIXTURE_SEASON_ARRAY:
		time.sleep(0.2)
		download_csv_for_all_fixtures_in_a_season(season, DOWNLOAD_FIXTURE_URL_ROOT, SCHEDULE_SAVE_PATH_ROOT)
	print("--- --- --- --- --- --- --- ---\n")
	
	# player data download
	print("Downloading player data...")
	for season in SEASONS_ARRAY:
		time.sleep(0.2)
		download_html_for_squad_player_data(season, PLAYER_DOWNLOAD_ROOT, PLAYER_SAVE_PATH_ROOT)
	print("--- --- --- --- --- --- --- ---")
	print("--- --- --- --- --- --- --- ---\n")

		

	