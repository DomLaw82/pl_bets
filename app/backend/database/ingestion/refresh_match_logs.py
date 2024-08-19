import requests
import bs4
import datetime, time
import pandas as pd

PLAYER_DATA_URL = f'https://fbref.com/en/comps/9/XXXX-XXXX/stats/XXXX-XXXX-Premier-League-Stats'

def get_fbref_data(url: str, season: str) -> list|None:

		response = requests.get(url)
		results = []
		
		# Check if the request was successful
		if response.status_code == 200:
			# Parse the HTML content
			soup = bs4.BeautifulSoup(response.text, 'html.parser')
			table_data = None
			comments = soup.find_all(string=lambda text: isinstance(text, bs4.Comment))

			# Look for the specific div in the comments
			for comment in comments:
				comment_soup = bs4.BeautifulSoup(comment, 'html.parser')
				div_standard_stats = comment_soup.find('div', id='div_stats_standard')
				if div_standard_stats:
					table_data = div_standard_stats.find('table')
			
			# Find the div with the class 'all-stats-standard'
			div = table_data
			
			# Find the table within the div
			if div:
				# Find the rows in the table
				name_col = div.find_all('td', {'data-stat': 'player'})
				match_logs_col = div.find_all('td', {'data-stat': 'matches'})
				position_col = div.find_all('td', {'data-stat': 'position'})

				player_name = ""
				player_href = ""
				id = ""
				match_logs_href = ""

				if len(name_col) < 1:
					print(f'Failed to find the player column for season {season}.')
					return None

				for idx in range(len(name_col)):
					player_name = name_col[idx].find('a').get_text()
					id = name_col[idx].get('data-append-csv')
					position = position_col[idx].get_text()
					match_logs_href = match_logs_col[idx].find('a')['href']

					print({
						'season': season,
						'player_name': player_name,
						'position': position,
						'match_logs_href': "https://fbref.com" + match_logs_href,
						'fbref_id': id
					})
					results.append({
						'season': season,
						'player_name': player_name,
						'position': position,
						'match_logs_href': "https://fbref.com" + match_logs_href,
						'fbref_id': id
					})
				
				print(f'SUCCESS')
				print(f'Number of players found: {len(name_col)}')
				print("----------------------------------------")
				print("\n")
				return results
			else:
				print(f'Failed to find the div for season {season}.')
				return None

		else:
			print(response.status_code)
			print(response.text)
			print(f'Failed to retrieve the HTML content for season {season}.')
			return None
		
def get_match_log_data(name: str, fbref_id: str, url: str, season: str, **kwargs) -> dict:
	""""""
	retries = kwargs.get('retries', 3)
	stat_type = kwargs.get('stat_type', 'summary')
	is_goalkeeper = kwargs.get('goalkeeper', False)

	columns = {
		"summary": ['minutes', 'goals', 'assists', 'pens_made', 'pens_att', 'shots', 'shots_on_target', 'cards_yellow', 'cards_red', 'blocks', 'xg', 'npxg'],
		"passing": ["passes_total_distance", "passes_progressive_distance", "passes_completed_short", "passes_short", "passes_completed_medium", "passes_medium", "passes_completed_long", "passes_long", "xg_assist", "pass_xa", "assisted_shots", "passes_into_final_third", "passes_into_penalty_area", "crosses_into_penalty_area", "progressive_passes"],
		"gca": ["sca", "sca_passes_live", "sca_passes_dead", "sca_take_ons", "sca_shots", "sca_fouled", "sca_defense", "gca", "gca_passes_live", "gca_passes_dead", "gca_take_ons", "gca_shots", "gca_fouled", "gca_defense"],
		"defense": ["tackles", "tackles_won", "tackles_def_3rd", "tackles_mid_3rd", "tackles_att_3rd", "challenge_tackles", "challenges", "blocked_shots", "blocked_passes", "interceptions", "clearances", "errors"],
		"possession": ["touches", "touches_def_pen_area", "touches_def_3rd", "touches_mid_3rd", "touches_att_3rd", "touches_att_pen_area", "touches_live_ball", "take_ons", "take_ons_won", "take_ons_tackled", "carries", "carries_distance", "carries_progressive_distance", "progressive_carries", "carries_into_final_third", "carries_into_penalty_area", "miscontrols", "dispossessed", "passes_received", "progressive_passes_received" ],
		"keeper": ["gk_shots_on_target_against", "gk_goals_against", "gk_saves", "gk_clean_sheets", "gk_psxg", "gk_pens_att", "gk_pens_allowed", "gk_pens_saved", "gk_pens_missed", "gk_passed_completed_launched", "gk_passes_launched", "gk_passes", "gk_passes_throws", "gk_passes_length_avg", "gk_goal_kicks", "gk_goal_kicks_length_avg"],
	}

	results = []

	match_logs_table_id = "matchlogs_all"

	if not is_goalkeeper and stat_type == "keeper":
		# Find out the number of rows required for this player
		url = url.replace("keeper", "summary")

	response = requests.get(url)
	
	if response.status_code == 200:
		soup = bs4.BeautifulSoup(response.text, 'html.parser')

		# Attempt to find the table directly or within comments
		table_data = soup.find('table', id=match_logs_table_id)
		if table_data is None:
			comments = soup.find_all(string=lambda text: isinstance(text, bs4.Comment))
			table_data = next(
				(bs4.BeautifulSoup(comment, 'html.parser').find('table', id=match_logs_table_id) 
					for comment in comments), None
			)

		if table_data:
			rows = table_data.find_all('tr', class_=lambda x: x is None or 'unused_sub' not in x.split())

			for row in rows[2:-1]:
				if not row.find('th', {'data-stat': 'date'}).get_text(strip=True):
					continue

				match_data = {
					'fbref_id': fbref_id,
					'player_name': name,
					'season': season,
					'date': row.find('th', {'data-stat': 'date'}).get_text(strip=True) if row.find('th', {'data-stat': 'date'}) else None,
					'competition': row.find('td', {'data-stat': 'comp'}).get_text(strip=True) if row.find('td', {'data-stat': 'comp'}) else None,
					'gameweek': row.find('td', {'data-stat': 'round'}).get_text(strip=True) if row.find('td', {'data-stat': 'round'}) else None,
					'location': row.find('td', {'data-stat': 'venue'}).get_text(strip=True) if row.find('td', {'data-stat': 'venue'}) else None,
					'result': row.find('td', {'data-stat': 'result'}).get_text(strip=True) if row.find('td', {'data-stat': 'result'}) else None,
					'team': row.find('td', {'data-stat': 'team'}).get_text(strip=True) if row.find('td', {'data-stat': 'team'}) else None,
					'opponent': row.find('td', {'data-stat': 'opponent'}).get_text(strip=True) if row.find('td', {'data-stat': 'opponent'}) else None,
					'position': row.find('td', {'data-stat': 'position'}).get_text(strip=True) if row.find('td', {'data-stat': 'position'}) else None,
					'started': row.find('td', {'data-stat': 'game_started'}).get_text(strip=True) if row.find('td', {'data-stat': 'game_started'}) else None,
				}

				if not is_goalkeeper and stat_type == "keeper":
					# Set all the goalkeeper stats to 0 for non-goalkeepers
					for column in columns[stat_type]:
						match_data[column] = 0

				else:
					for column in columns[stat_type]:
						match_data[column] = row.find('td', {'data-stat': column}).get_text(strip=True) if row.find('td', {'data-stat': column}) else None
						match_data[column] = float(match_data[column]) if match_data[column] else 0
			
				results.append(match_data)

	else:
		print(f'F', end=" ")
		time.sleep(10)
		retries -= 1
		if retries > 0:
			retry_result = get_match_log_data(name, fbref_id, url, season, retries=retries)
			if "missing_data" in retry_result:
				print(f'')
				return retry_result
			if "data" in retry_result:
				return retry_result
			return {"data": retry_result}
		else:
			return {
				"missing_data" : {
				'fbref_id': fbref_id,
				'player_name': name,
				'season': season,
				'url': url,
				'error': f'Failed to retrieve the HTML content. Error code {response.status_code}'
				}
			}
	print('SUCCESS')
	return {"data": results}
		
def match_logs_main(current_season: str) -> pd.DataFrame:
	url = PLAYER_DATA_URL.replace('XXXX-XXXX', current_season)
	season_players = get_fbref_data(url, current_season)

	all_season_players = pd.DataFrame()
	if season_players:
		season_players_df = pd.DataFrame(season_players)
		all_season_players = pd.read_csv('./data/fbref_data/player_data.csv')

		all_season_players = pd.concat([all_season_players, season_players_df], ignore_index=True)
		all_season_players.drop_duplicates(subset=['fbref_id', 'season'], keep='first', inplace=True)
		all_season_players = all_season_players[['fbref_id', 'player_name', 'position', 'match_logs_href', 'season']]
		all_season_players.to_csv('./data/fbref_data/player_data.csv', index=False)

		print(f"Successfully saved the player data for season {current_season}.")

	# Get the match logs for each player
	enhanced_match_logs_results = []
	missing_enhanced_data = []

	current_season_players = all_season_players[all_season_players['season'] == current_season]
	for idx, row in current_season_players.iterrows():

		fbref_id = row["fbref_id"]
		name = row["player_name"]
		position = row["position"]
		url = row["match_logs_href"]
		season = row["season"]
		retries = 3

		urls = []
		summary_url = url
		urls.append(summary_url)
		passing_url = url.replace("summary", "passing")
		urls.append(passing_url)
		defensive_actions_url = url.replace("summary", "defense")
		urls.append(defensive_actions_url)
		possession_url = url.replace("summary", "possession")
		urls.append(possession_url)
		gca_url = url.replace("summary", "gca")
		urls.append(gca_url)
		goalkeeping_url = url.replace("summary", "keeper")
		urls.append(goalkeeping_url)

		enhanced_stats = []
		for url in urls:
			print(f'({idx}) Processing player {name} logs for season {season} at URL: {url}', end=' ... ')
			try:
				result = get_match_log_data(name, fbref_id, url, season, retries=retries, stat_type=url.split("/")[-2], goalkeeper=position == "GK")
				if "data" in result:
					if len(enhanced_stats) == 0:
						enhanced_stats = result["data"]
					else:
						for i, match in enumerate(result["data"]):
							enhanced_stats[i].update(match)
				elif "missing_data" in result:
					missing_enhanced_data.extend(result["missing_data"])
			except Exception as e:
				print(f'FAILED - {e.__cause__}: {str(e)}')
				missing_enhanced_data.append({
					'fbref_id': fbref_id,
					'player_name': name,
					'position': position,
					'season': season,
					'url': url,
					'error': str(e)
				})
			time.sleep(4)
		enhanced_match_logs_results.extend(enhanced_stats)

	res = pd.DataFrame(enhanced_match_logs_results)
	res["result"] = res["result"].str.replace("–", "-") # remove ambiguous hyphen character
	add_to_db_df = res.copy()

	all_matches = pd.read_csv('./data/fbref_data/enhanced_player_match_logs.csv')
	combined = pd.concat([all_matches, res], ignore_index=True)
	combined.drop_duplicates(subset=['fbref_id', 'season', 'date'], keep='first', inplace=True)
	
	combined.to_csv("./data/fbref_data/enhanced_player_match_logs.csv", index=False)
	print(f"Successfully saved the enhanced player match logs for season {current_season}.")

	# Filter duplicates based on what's in the database
	add_to_db_df = add_to_db_df[~add_to_db_df[['fbref_id', 'season', 'date']].isin(all_matches[['fbref_id', 'season', 'date']])]
	return add_to_db_df
