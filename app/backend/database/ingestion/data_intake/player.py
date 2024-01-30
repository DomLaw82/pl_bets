from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.utilities.unique_id import get_team_id, get_player_id
from data_intake.utilities.string_manipulation import escape_single_quote

def not_blank_entry(player: list) -> bool:
	"""
	Checks if all elements in the player list are not blank.

	Args:
		player (list): A list containing player information.

	Returns:
		bool: True if all elements in the player list are not blank, False otherwise.
	"""
	return all(element.strip("\r\n-").strip() for element in player)

def format_player_entries(player: list[str]) -> list[str]:
	"""
	Formats the player entries by removing leading and trailing whitespaces and hyphens,
	splitting the first name and last name if necessary, and reformatting the date of birth.

	Args:
		player (list[str]): The player information in the format [first_name, last_name, position, dob].

	Returns:
		list[str]: The formatted player information in the format [first_name, last_name, position, dob].
	"""
	formatted_name = [name.strip("\r\n-").strip() for name in player[0].split(maxsplit=1)]
	formatted_name += [""] * (2 - len(formatted_name))
	
	split_dob = [portion.strip("\r\n").strip() for portion in player[2].split("-")]
	formatted_dob_year = "19" + split_dob[-1] if int(str(datetime.now().year)[-2:]) < int(split_dob[-1]) else "20" + split_dob[-1]
	new_dob = [f"{formatted_dob_year}-{split_dob[1]}-{split_dob[0]}"]

	return formatted_name + [player[1].strip("\r\n-").strip()] + new_dob + [player[3].strip("\r\n-").strip()]

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
	Retrieves all the teams for a given season from the provided BeautifulSoup object.

	Parameters:
	soup (BeautifulSoup): The BeautifulSoup object containing the HTML data.

	Returns:
	list: A list of tuples, where each tuple contains the team name and its corresponding href.
	"""
	team_elements = soup.find_all("h5")
	teams = [(ele.text, ele.a.get("href")) for ele in team_elements]
	return teams

def get_team_squad(html_content):
	"""
	Extracts the squad information from the HTML content.

	Args:
		html_content (str): The HTML content of the page.

	Returns:
		list: A list of lists containing the player's name, position, and date of birth.
	"""
	soup = get_page_soup(html_content)
	rows = soup.find_all("tr")[1:]
	
	all_columns = soup.find_all("tr")[0]
	all_column_names = [elem.text.strip("\n") for elem in all_columns.find_all("td")]

	required_cols = [all_column_names.index("Name"), all_column_names.index("Pos"), all_column_names.index("Date of Birth")]

	squad = []
	for idx, row in enumerate(rows):
		if "Players no longer at this club" in row.text:
			rows = rows[:idx] + rows[idx+2:-1]
			break

		row_data = [row_data.text for row_data in row.find_all("td")]
		if all(col_index < len(row_data) for col_index in required_cols):
			squad.append([row_data[col_index] for col_index in required_cols])

	return squad

def player_df_to_db(df: pd.DataFrame, db_connection):
	"""
	Inserts player data from a DataFrame into the database.

	Args:
		df (pd.DataFrame): The DataFrame containing player data.
		db_connection: The connection to the database.

	Returns:
		None
	"""
	df = df[["first_name", "last_name", "birth_date", "position"]]
	df["first_name"] = df["first_name"].apply(escape_single_quote)
	df["last_name"] = df["last_name"].apply(escape_single_quote)
	player_rows_not_in_db_df = remove_duplicate_rows(db_connection, df, ["first_name", "last_name", "birth_date", "position"], "player")
	if player_rows_not_in_db_df.empty:
		return
	ordered_player_df = player_rows_not_in_db_df[["first_name", "last_name", "birth_date", "position"]]
	ordered_player_df.to_sql("player", db_connection.conn, if_exists="append", index=False)

def player_team_df_to_db(df: pd.DataFrame, season: str, db_connection):
	"""
	Inserts player-team data from a DataFrame into the database.

	Args:
		df (pd.DataFrame): The DataFrame containing the player-team data.
		season (str): The season for which the data is being inserted.
		db_connection: The database connection object.

	Returns:
		None
	"""
	df["player_id"] = df.apply(lambda row: get_player_id(db_connection, row), axis=1)
	df["team_id"] = df["team_id"].apply(lambda team_id: get_team_id(db_connection, team_id))
	df["season"] = season
	player_team_df = df[["player_id", "team_id", "season"]]
	player_team_df = remove_duplicate_rows(db_connection, player_team_df, ["player_id", "team_id", "season"], "player_team")
	player_team_df.to_sql("player_team", db_connection.conn, if_exists="append", index=False)

def player_main(db_connection):
	data_folder_path = "./data/squad_data"
	seasons = sorted(os.listdir(data_folder_path))

	for season in seasons:
		season_folder = os.path.join(data_folder_path, season)
		teams = sorted(os.listdir(season_folder))

		for team in teams:
			with open(os.path.join(season_folder, team), "r") as file:
				html_content = file.read()

			squad = get_team_squad(html_content)
			squad_no_blanks = [player for player in squad if not_blank_entry(player)]
			squad_with_team = [player + [team] for player in squad_no_blanks]
			complete_squad = [format_player_entries(player) for player in squad_with_team]

			player_df = pd.DataFrame(data=complete_squad, columns=["first_name", "last_name", "position", "birth_date", "team_id"])
			player_df["birth_date"] = pd.to_datetime(player_df["birth_date"], format="%Y-%m-%d").dt.strftime("%Y-%m-%d")

			player_team_df = player_df.copy()
			player_team_df['team_id'] = player_team_df['team_id'].apply(lambda x: x.replace('.html', ''))

			player_df[["first_name", "last_name"]] = player_df[["first_name", "last_name"]].map(escape_single_quote)
			player_rows_not_in_db_df = remove_duplicate_rows(db_connection, player_df, ["first_name", "last_name", "birth_date"], "player")
			
			if not player_rows_not_in_db_df.empty:
				player_rows_not_in_db_df = player_rows_not_in_db_df[["first_name", "last_name", "birth_date", "position"]]
				save_to_database(db_connection, player_rows_not_in_db_df, "player")

			player_team_df["player_id"] = player_team_df.apply(lambda row: get_player_id(db_connection, row), axis=1)
			player_team_df["team_id"] = player_team_df["team_id"].apply(lambda x: get_team_id(db_connection, x))
			player_team_df["season"] = season

			player_team_df = player_team_df[["player_id", "team_id", "season"]]
			player_team_df = remove_duplicate_rows(db_connection, player_team_df, ["player_id", "team_id", "season"], "player_team")
			save_to_database(db_connection, player_team_df, "player_team")
		
def save_to_database(db_connection, df: pd.DataFrame, table_name: str) -> None:
	"""
	Saves a DataFrame to a database table.

	Args:
		db_connection: The database connection object.
		df: The DataFrame to be saved.
		table_name: The name of the table to save the DataFrame to.

	Returns:
		None
	"""
	df.to_sql(table_name, db_connection.conn, if_exists="append", index=False)
