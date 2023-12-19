import requests, os, time
from bs4 import BeautifulSoup

# DOWNLOADING GAMES DATA FOR EVERY SEASON
# TODO - add url and word_to_replace as an argument to the download_csv_for_all_games_in_a_season function, have a word set in the url to replace with the season

PLAYERS_WEBSITE_ROOT = "https://www.footballsquads.co.uk/eng/"
SEASONS_ARRAY = [f"{str(year-1)}-{str(year)}/" for year in range(2017, 2025, 1)]
MATCH_SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2017, 2025, 1)]

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
	return BeautifulSoup(html_text, "html.parser")

def get_all_teams_for_season(soup) -> list:
	h5_elements = soup.find_all("h5")
	team_names = [ele.text for ele in h5_elements]
	a_elements = [ele.a for ele in h5_elements]
	hrefs = [ele.get("href") for ele in a_elements]
	return list(zip(team_names, hrefs))

def get_team_squad(endpoint: str, SEASON: str, site_root: str):
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