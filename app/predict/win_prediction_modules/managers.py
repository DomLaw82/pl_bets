import pandas as pd
import numpy as np
import datetime
from app_logger import FluentLogger
from date_functions import get_current_date, get_current_season
from define_environment import load_correct_environment_variables
from db_connection import SQLConnection
import os

load_correct_environment_variables()

logger = FluentLogger("managers").get_logger()
db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))

def get_team_current_manager_id(db: SQLConnection, team_id: str, fixture_date: str) -> str:
	"""
	Get the current manager ID of the given team.

	Args:
		db (SQLConnection): SQLConnection object
		team_id (str): The ID of the team

	Returns:
		str : The ID of the current manager of the team
	"""
	try:
		# Get the current manager of the team
		manager_id = db.get_list(f"""
			SELECT 
				manager.id,
				manager.first_name,
				manager.last_name
			FROM manager
			JOIN team_manager
			ON manager.id = team_manager.manager_id
			WHERE team_manager.team_id = '{team_id}'
				AND (team_manager.start_date <= '{fixture_date}')
				AND (team_manager.end_date = 'current' OR team_manager.end_date >= '{fixture_date}')
		""")[0]
		return manager_id
	except Exception as e:
		logger.error(f"An error occurred while getting the current manager ID of the team: {str(e)}")
		raise e
	
def get_all_teams_managed(db: SQLConnection, manager_id: str, fixture_date: str) -> list[str]:
	"""
	Get all the teams managed by the given manager.

	Args:
		db (SQLConnection): SQLConnection object
		manager_id (str): The ID of the manager
		fixture_date (str): The date of the fixture

	Returns:
		list[str] : [team_id, start_date, end_date]
	"""
	try:
		# Get all the teams managed by the manager
		teams_managed = db.get_list(f"""
			SELECT 
				team_id,
				start_date,
				end_date
			FROM team_manager
			WHERE manager_id = '{manager_id}'
			AND start_date <= '{fixture_date}'
		""")
		return teams_managed
	
	except Exception as e:
		logger.error(f"An error occurred while getting all the teams managed by the manager: {str(e)}")
		raise e
	
def get_manager_games_managed(db: SQLConnection, data: list, fixture_date: str) -> pd.DataFrame:
	"""
	Get the number of games managed by the given manager for the given team between the given dates.

	Args:
		db (SQLConnection): SQLConnection object
		manager_id (str): The ID of the manager
		team_id (str): The ID of the team
		start_date (str): The start date
		end_date (str): The end date

	Returns:
		int : The number of games managed by the manager
	"""
	try:
		games = []
		for team_id, start_date, end_date in data:
			# Get the number of games managed by the manager
			games_managed = db.get_dict(f"""
				SELECT 
					id, date, home_team_id, 
					away_team_id, home_goals, 
					away_goals, home_shots, 
					away_shots, home_shots_on_target, 
					away_shots_on_target, home_corners, 
					away_corners, home_fouls, 
					away_fouls, home_yellow_cards, 
					away_yellow_cards, home_red_cards, 
					away_red_cards,
					CASE
						WHEN home_team_id = '{team_id}' THEN 'home'
						WHEN away_team_id = '{team_id}' THEN 'away'
					END AS team_managed
				FROM match
				WHERE (
					home_team_id = '{team_id}'
					OR away_team_id = '{team_id}'
				)
				AND date >= '{start_date}'
				AND date <= '{end_date}'
				AND date < '{fixture_date}'
			""")
			games.extend(games_managed)
		games_df = pd.DataFrame(games)
		return games_df
	except Exception as e:
		logger.error(f"An error occurred while getting the number of games managed by the manager: {str(e)}")
		raise e

def create_manager_average_stats(data: pd.DataFrame, columns: list, location: str) -> pd.DataFrame:
	"""
	Create the average stats of the given columns for the given data.

	location must be either "home" or "away".
	"""

	manager_stats = pd.DataFrame(index=data.index, columns=columns)

	not_location = "home" if location == "away" else "away"

	for stat in columns:
		manager_stats[f"{stat}"] = np.where(data[f"team_managed_{location}_manager"] == f"{location}", 
											data[f"{location}_{stat}"],
											data[f"{not_location}_{stat}"])
	
	manager_stats = manager_stats.mean().to_frame().T
	
	manager_stats = manager_stats.add_prefix(f"{location}_manager_h2h_avg_")

	return manager_stats

def get_manager_head_to_head(sql_connection: SQLConnection, data: pd.DataFrame) -> pd.DataFrame:
	"""
	Get the head-to-head record between the two managers of the given fixtures.

	Args:
		data (pd.DataFrame): DataFrame containing the fixture data

	Returns:
		pd.DataFrame : DataFrame containing the head-to-head record between the two managers
	"""

	stats_list = ["goals", "shots", "shots_on_target", "corners", "fouls", "yellow_cards", "red_cards"]
	output_columns = ["home_manager_h2h_avg_goals","home_manager_h2h_avg_shots","home_manager_h2h_avg_shots_on_target","home_manager_h2h_avg_corners","home_manager_h2h_avg_fouls","home_manager_h2h_avg_yellow_cards","home_manager_h2h_avg_red_cards","away_manager_h2h_avg_goals","away_manager_h2h_avg_shots","away_manager_h2h_avg_shots_on_target","away_manager_h2h_avg_corners","away_manager_h2h_avg_fouls","away_manager_h2h_avg_yellow_cards","away_manager_h2h_avg_red_cards"]

	try:
		# Get the head-to-head record between the two managers
		for idx, row in data.copy().iterrows():
			home_team_id = row["home_team_id"]
			away_team_id = row["away_team_id"]
			date = row["date"]
			print(f"\n--------\n\n{home_team_id} v {away_team_id} @ {date}\n\n")

			home_manager_id, home_manager_first_name, home_manager_last_name = get_team_current_manager_id(sql_connection, home_team_id, date)
			away_manager_id, away_manager_first_name, away_manager_last_name = get_team_current_manager_id(sql_connection, away_team_id, date)

			home_management_periods = get_all_teams_managed(sql_connection, home_manager_id, date)
			away_management_periods = get_all_teams_managed(sql_connection, away_manager_id, date)

			home_games_managed = get_manager_games_managed(sql_connection, home_management_periods, date)
			away_games_managed = get_manager_games_managed(sql_connection, away_management_periods, date)

			if home_games_managed.empty or away_games_managed.empty:
				# If empty, there are no games managed by one or both of the managers
				data.loc[idx, output_columns] = 0
				continue

			head_to_heads = home_games_managed.merge(away_games_managed[['id', 'team_managed']], on="id", how="inner", suffixes=('_home_manager', '_away_manager'))
			home_manager_stats = pd.DataFrame()
			away_manager_stats = pd.DataFrame()

			if head_to_heads.empty:
				# If empty, there are no head-to-head games between the two managers
				# Use the manager's average stats from all games managed up to the fixture date
				print(f"No head-to-head games between {home_manager_first_name} {home_manager_last_name} ({home_manager_id}) ({len(home_games_managed)} matches) and {away_manager_first_name} {away_manager_last_name} ({away_manager_id}) ({len(away_games_managed)} matches) - using average stats from all games managed up to the fixture date")
				home_games_managed = home_games_managed.rename(columns={"team_managed": "team_managed_home_manager"})
				away_games_managed = away_games_managed.rename(columns={"team_managed": "team_managed_away_manager"})
				home_manager_stats = create_manager_average_stats(home_games_managed, stats_list, "home")
				away_manager_stats = create_manager_average_stats(away_games_managed, stats_list, "away")
			else:
				print(f"{home_manager_first_name} {home_manager_last_name} ({home_manager_id}) and {away_manager_first_name} {away_manager_last_name} ({away_manager_id}) have managed {len(head_to_heads)} games against one another:\n\n{head_to_heads}")
				home_manager_stats = create_manager_average_stats(head_to_heads, stats_list, "home")
				away_manager_stats = create_manager_average_stats(head_to_heads, stats_list, "away")

			print(f"{home_manager_first_name} {home_manager_last_name} ({home_manager_id}) has an average of:\n{home_manager_stats.T}\n\nagainst {away_manager_first_name} {away_manager_last_name} ({away_manager_id}) who has an average of:\n{away_manager_stats.T}")

			average_stats = pd.concat([home_manager_stats, away_manager_stats], axis=1)
			data.loc[idx, average_stats.columns] = average_stats.values

		return data

	except Exception as e:
		# logger.error(f"An error occurred while getting the head-to-head record between the two managers: {str(e)}")
		raise e
	
if __name__ == "__main__":
	data = pd.read_csv('../files/match_and_form_data.csv')
	data = get_manager_head_to_head(db, data)
	data.to_csv('../files/match_and_form_data_with_manager_h2h.csv', index=False)