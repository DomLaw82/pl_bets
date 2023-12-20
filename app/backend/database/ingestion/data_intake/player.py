from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.utilities.unique_id import get_team_id, get_player_id
from data_intake.utilities.string_manipulation import escape_single_quote

def not_blank_entry(player: list) -> bool:
	player = [player[0].strip("\r\n-").strip(), player[1].strip("\r\n-").strip(), player[2].strip("\r\n-").strip()]
	return all(player)

def format_player_entries(player: list[str]) -> list[str]:
	# Original format: [first_name, last_name, position, dob]

	player = [player[0].strip("\r\n-").strip(), player[1].strip("\r\n-").strip(), player[2].strip("\r\n-").strip(), player[3].strip("\r\n-").strip()]
	
	formatted_name = player[0].split(maxsplit=1)
	formatted_name = formatted_name + [""] if len(formatted_name) < 2 else formatted_name
	formatted_name = [name.strip("\r\n").strip() for name in formatted_name]
	
		
	split_dob = [portion.strip("\r\n").strip() for portion in player[2].split("-")]
	formatted_dob_year = "19" + str(split_dob[-1]) if int(str(datetime.now().year)[-2:]) < int(split_dob[-1]) else "20" + str(split_dob[-1]) 
	new_dob = [f"{formatted_dob_year}-{split_dob[1]}-{split_dob[0]}"]

	return formatted_name + [player[1]] + new_dob + [player[3]]

def get_page_soup(html_text):
	return BeautifulSoup(html_text, "html.parser")

def get_all_teams_for_season(soup) -> list:
	h5_elements = soup.find_all("h5")
	team_names = [ele.text for ele in h5_elements]
	a_elements = [ele.a for ele in h5_elements]
	hrefs = [ele.get("href") for ele in a_elements]
	return list(zip(team_names, hrefs))

def get_team_squad(html_content):
	soup = get_page_soup(html_content)
	rows = soup.find_all("tr")[1:]
	
	all_columns = soup.find_all("tr")[0]
	all_column_names = all_columns.find_all("td")
	all_column_names = [elem.text.strip("\n") for elem in all_column_names]

	for idx, row in enumerate(rows):
		if "Players no longer at this club" in str(row):
			rows = rows[:idx] + rows[idx+2:-1]
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

def player_df_to_db(df:pd.DataFrame, db_connection):
	df = df[["first_name", "last_name", "birth_date", "position"]]
	df.loc[:, "first_name"] = df.apply(lambda row: escape_single_quote(row.first_name), axis=1)
	df.loc[:, "last_name"] = df.apply(lambda row: escape_single_quote(row.last_name), axis=1)
	rows_not_in_db_df = remove_duplicate_rows(db_connection, df, ["first_name", "last_name", "birth_date", "position"], "player")
	if rows_not_in_db_df.empty:
		return
	ordered_player_df = rows_not_in_db_df[["first_name", "last_name", "birth_date", "position"]]
	ordered_player_df.to_sql("player", db_connection.conn, if_exists="append", index=False)

# TODO - Fix error "index out of range" concerning below function
def player_team_df_to_db(df: pd.DataFrame, season: str, db_connection):
	df.loc[:, "player_id"] = df.apply(lambda row: get_player_id(db_connection, row), axis=1)
	df.loc[:, "team_id"] = df.apply(lambda row: get_team_id(db_connection, row.team_id), axis=1)
	df["season"] = season
	player_team_df = df[["player_id", "team_id", "season"]]
	player_team_df = remove_duplicate_rows(db_connection, player_team_df, ["player_id", "team_id", "season"], "player_team")
	player_team_df.to_sql("player_team", db_connection.conn, if_exists="append", index=False)

def player_main(db_connection):

	data_folder_path = "./data/squad_data"

	seasons = sorted(os.listdir(data_folder_path))

	for season in seasons:

		season_folder = data_folder_path + "/" + season 

		teams = sorted(os.listdir(season_folder))
		
		for team in teams:
			html_content = ""
			with open(f"{season_folder+'/'+team}", "r") as file:
				html_content = file.read()
			
			squad = get_team_squad(html_content)
			
			squad_no_blanks = [player for player in squad if not_blank_entry(player)]
			squad_with_team = [player + [team] for player in squad_no_blanks]
			complete_squad = [format_player_entries(player) for player in squad_with_team]

			player_df = pd.DataFrame(data=complete_squad, columns=["first_name", "last_name", "position", "birth_date", "team_id"])
			player_df.loc[:, "birth_date"] = player_df.apply(lambda row: datetime.date(datetime.strptime(row.birth_date, "%Y-%m-%d")), axis=1)
			
			player_team_df = player_df.copy(deep=True)

			player_df = player_df[["first_name", "last_name", "birth_date", "position"]]
			player_df.loc[:, "first_name"] = player_df.apply(lambda row: escape_single_quote(row.first_name), axis=1)
			player_df.loc[:, "last_name"] = player_df.apply(lambda row: escape_single_quote(row.last_name), axis=1)
			rows_not_in_db_df = remove_duplicate_rows(db_connection, player_df, ["first_name", "last_name", "birth_date"], "player")
			if rows_not_in_db_df.empty:
				continue
			save_to_database(db_connection, rows_not_in_db_df, "player")

			player_team_df['team_id'] = player_team_df['team_id'].apply(lambda x: x.replace('.html', ''))
			player_team_df.loc[:, "player_id"] = player_team_df.apply(lambda row: get_player_id(db_connection, row), axis=1)
			player_team_df.loc[:, "team_id"] = player_team_df.apply(lambda row: get_team_id(db_connection, row.team_id), axis=1)

			player_team_df["season"] = season
			

			player_team_df = player_team_df[["player_id", "team_id", "season"]]
			player_team_df = remove_duplicate_rows(db_connection, player_team_df, ["player_id", "team_id", "season"], "player_team")
			save_to_database(db_connection, player_team_df, "player_team")
		
def save_to_database(db_connection, df: pd.DataFrame, table_name: str) -> None:
	df.to_sql(table_name, db_connection.conn, if_exists="append", index=False)
