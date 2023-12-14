import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pandas import DataFrame
from database.utilities.remove_duplicates import remove_duplicate_rows
from database.utilities.unique_id import create_id, convert_team_name_to_team_id, get_player_id
from database.utilities.string_manipulation import escape_single_quote

PLAYERS_WEBSITE_ROOT = "https://www.footballsquads.co.uk/eng/"
SEASONS_ARRAY = [f"{str(year-1)}-{str(year)}/" for year in range(2017, 2025, 1)]
LEAGUE_NAMES = ["faprem.htm", "engprem.htm"]

def not_blank_entry(player: list) -> bool:
	player = [player[0].strip("\r\n-").strip(), player[1].strip("\r\n-").strip(), player[2].strip("\r\n-").strip()]
	return all(player)

def format_player_entries(player: list[str]) -> list[str]:
	# Original format: [first_name last_name, position, dob]

	player = [player[0].strip("\r\n-").strip(), player[1].strip("\r\n-").strip(), player[2].strip("\r\n-").strip(), player[3].strip("\r\n-").strip()]
	
	formatted_name = player[0].split(maxsplit=1)
	formatted_name = formatted_name + [""] if len(formatted_name) < 2 else formatted_name
	formatted_name = [name.strip("\r\n").strip() for name in formatted_name]
	
		
	split_dob = [portion.strip("\r\n").strip() for portion in player[2].split("-")]
	formatted_dob_year = "19" + str(split_dob[-1]) if int(str(datetime.now().year)[-2:]) < int(split_dob[-1]) else "20" + str(split_dob[-1]) 
	new_dob = [f"{formatted_dob_year}-{split_dob[1]}-{split_dob[0]}"]

	return formatted_name + [player[1]] + new_dob + [player[3]]

def player_df_to_db(df:DataFrame, db_connection):
	df = df[["first_name", "last_name", "birth_date", "position"]]
	df.loc[:, "first_name"] = df.apply(lambda row: escape_single_quote(row.first_name), axis=1)
	df.loc[:, "last_name"] = df.apply(lambda row: escape_single_quote(row.last_name), axis=1)
	rows_not_in_db_df = remove_duplicate_rows(db_connection, df, ["first_name", "last_name", "birth_date", "position"], "player")
	if rows_not_in_db_df.empty:
		return
	rows_not_in_db_df.loc[:, "id"] = rows_not_in_db_df.apply(lambda row: create_id("player", db_connection, row.name), axis=1)
	ordered_player_df = rows_not_in_db_df[["id", "first_name", "last_name", "birth_date", "position"]]
	ordered_player_df.to_sql("player", db_connection.conn, if_exists="append", index=False)

# TODO - Fix error "index out of range" concerning below function
def player_team_df_to_db(df: DataFrame, season: str, db_connection):
	df.loc[:, "player_id"] = df.apply(lambda row: get_player_id(db_connection, row), axis=1)
	df.loc[:, "team_id"] = df.apply(lambda row: convert_team_name_to_team_id(db_connection, row.team_id), axis=1)
	df["season"] = season
	player_team_df = df[["player_id", "team_id", "season"]]
	player_team_df = remove_duplicate_rows(db_connection, player_team_df, ["player_id", "team_id", "season"], "player_team")
	player_team_df.to_sql("player_team", db_connection.conn, if_exists="append", index=False)

def main(db_connector):
	for SEASON in SEASONS_ARRAY:
		faprem_url = PLAYERS_WEBSITE_ROOT+SEASON+LEAGUE_NAMES[0]
		engprem_url = PLAYERS_WEBSITE_ROOT+SEASON+LEAGUE_NAMES[1]

		try:
			response = requests.get(faprem_url)
			if response.status_code != 200:
				response = requests.get(engprem_url)
				if response.status_code != 200:
					raise Exception
			html_content = response.text
			soup = BeautifulSoup(html_content, "html.parser")
			teams_links = get_all_teams_for_season(soup)

			player_team_season = f"{SEASON[2:4]}/{SEASON[-3:-1]}"
			season_squads = {}

			for team_link in teams_links:
				team = team_link[0]
				link = team_link[1]
				
				squad = get_team_squad(link, SEASON, PLAYERS_WEBSITE_ROOT)
				squad_no_blanks = [player for player in squad if not_blank_entry(player)]
				squad_with_team = [player + [team] for player in squad_no_blanks]
				complete_squad = [format_player_entries(player) for player in squad_with_team]

				squad_df = DataFrame(data=complete_squad, columns=["first_name", "last_name", "position", "birth_date", "team_id"])
				squad_df.loc[:, "birth_date"] = squad_df.apply(lambda row: datetime.date(datetime.strptime(row.birth_date, "%Y-%m-%d")), axis=1)
				
				player_df_to_db(squad_df, db_connector)
				player_team_df_to_db(squad_df, player_team_season, db_connector)

		except Exception as e:
			print(f"ERROR: {team} - {SEASON}\n")
			print(e)