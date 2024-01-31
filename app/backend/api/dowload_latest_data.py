import requests, os, time
from bs4 import BeautifulSoup

# DOWNLOADING GAMES DATA FOR EVERY SEASON
# TODO - add url and word_to_replace as an argument to the download_csv_for_all_games_in_a_season function, have a word set in the url to replace with the season
SEE_FIXTURES = "https://fixturedownload.com/results/epl-2022"
DOWNLOAD_FIXTURE_URL = "https://fixturedownload.com/download/csv/epl-" # add on the year the season starts in, i.e. 2024
PLAYERS_WEBSITE_ROOT = "https://www.footballsquads.co.uk/eng/"

FIXTURE_SEASON_ARRAY = [str(year) for year in range(2017, 2024, 1)]
SEASONS_ARRAY = [f"{str(year-1)}-{str(year)}/" for year in range(2018, 2025, 1)]
MATCH_SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2018, 2025, 1)]

LEAGUE_NAMES = ["faprem.htm", "engprem.htm"]

def download_csv_for_all_games_in_a_season(season: str):
	"""
	Downloads match facts for every game for the specified season data as a single csv

	Arguments:
		season (str): last 2 digits of each year the season encompasses, e.g. "16/17"
	"""
      
	try:
			# MATCH_SITE_SEASONS
		save_path = f"game_data/E0 - {season}.csv"
		url = f'https://www.football-data.co.uk/mmz4281/{season}/E0.csv'
		response = requests.get(url)
		if response.status_code == 200:
			csv_data = response.text
			with open(save_path, 'w') as file:
				file.write(csv_data)
			print(f'CSV file for season {season} downloaded and saved to {save_path}')
			return True
		else:
			print(f'Failed to download the CSV file for season {season}. Status code:', response.status_code)
			return False
	except Exception as e:
		print(f'An error occurred while downloading season {season}:', str(e))
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

def player_data():
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

	Note: This function requires the SEASONS_ARRAY, PLAYERS_WEBSITE_ROOT, LEAGUE_NAMES, get_all_teams_for_season,
	requests, time, os, and BeautifulSoup to be imported.

	Returns:
		None
	"""
	# Function code here
	for SEASON in SEASONS_ARRAY:
		try:
			squad_url = PLAYERS_WEBSITE_ROOT+SEASON+LEAGUE_NAMES[0]
			page_content = requests.get(squad_url).text
		except Exception as e:
			try:
				squad_url = PLAYERS_WEBSITE_ROOT+SEASON+LEAGUE_NAMES[1]
				page_content = requests.get(squad_url).text
			except Exception as e:
				print(f"ERROR: {SEASON}\n")
				print(e)
		finally:
			soup = get_page_soup(page_content)
			teams_links = get_all_teams_for_season(soup)

			for team_link in teams_links:
				team = team_link[0]
				link = team_link[1]

				squad_url = PLAYERS_WEBSITE_ROOT+SEASON+link
				page_content = requests.get(squad_url).text
				if (not os.path.exists(f"./data/squad_data/{SEASON.replace('/', '')}")):
					os.mkdir(f"./data/squad_data/{SEASON.replace('/', '')}") 
				with open(f"./data/squad_data/{SEASON}/{team}.html", 'w') as file:
					file.write(page_content)


def player_data():
	
	for SEASON in SEASONS_ARRAY:
		faprem_url = PLAYERS_WEBSITE_ROOT+SEASON+LEAGUE_NAMES[0]
		engprem_url = PLAYERS_WEBSITE_ROOT+SEASON+LEAGUE_NAMES[1]
		time.sleep(2)
		try:
			response = requests.get(faprem_url)
			if response.status_code != 200:
				response = requests.get(engprem_url)
				if response.status_code != 200:
					raise Exception
			html_content = response.text 
			soup = BeautifulSoup(html_content, "html.parser")


			teams_links = get_all_teams_for_season(soup)

			for team_link in teams_links:
				team = team_link[0]
				link = team_link[1]

				squad_url = PLAYERS_WEBSITE_ROOT+SEASON+link
				page_content = requests.get(squad_url).text
				if (not os.path.exists(f"./data/squad_data/{SEASON.replace('/', '')}")):
					os.mkdir(f"./data/squad_data/{SEASON.replace('/', '')}") 
				with open(f"./data/squad_data/{SEASON}{team}.html", 'w') as file:
					file.write(page_content)
		except Exception as e:
			print(f"ERROR: {SEASON}\n")
			print(e)

def download_latest_data():
	
	# game data
	for season in MATCH_SITE_SEASONS:
		download_csv_for_all_games_in_a_season(season)

	