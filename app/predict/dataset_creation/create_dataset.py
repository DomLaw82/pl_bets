import pandas as pd
import numpy as np
from dataset_creation.db_connection import local_pl_stats_connector
import datetime, sys

db = local_pl_stats_connector

output_columns = [
	"home_goals", "away_goals", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
	"home_corners", "away_corners", "home_fouls", "away_fouls", "home_yellow_cards", "away_yellow_cards",
	"home_red_cards", "away_red_cards"
]
match_columns = [
	"match_id", "competition_id", "home_team_id", "away_team_id", "referee_id",
	"home_goals", "away_goals", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
	"home_corners", "away_corners", "home_fouls", "away_fouls", "home_yellow_cards", "away_yellow_cards",
	"home_red_cards", "away_red_cards"
]
stats_columns = [
	"goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]
player_stats_columns = ["player_id", "minutes_played","ninetys"] + stats_columns
pure_stats_columns = ["minutes_played"] + stats_columns
team_stats_columns = ["team_id"] + stats_columns

def create_player_stats_for_match(game_season: str, home_team_id: str, away_team_id: str, less_than_or_equal_to:str) -> pd.DataFrame:
	"""
	Create player statistics for a match.

	Args:
		game_season (str): The season of the match.
		home_team_id (str): The ID of the home team.
		away_team_id (str): The ID of the away team.
		less_than_or_equal_to (str): The condition for filtering the player statistics.

	Returns:
		pd.DataFrame: The DataFrame containing the player statistics for the match.
	"""
	return db.get_df(f"""
		SELECT 
			hpn.*, m.id AS match_id, m.competition_id, m.home_team_id, m.away_team_id, m.referee_id, 
			m.home_goals, m.away_goals, m.home_shots, m.away_shots, m.home_shots_on_target, 
			m.away_shots_on_target, m.home_corners, m.away_corners, m.home_fouls, m.away_fouls, 
			m.home_yellow_cards, m.away_yellow_cards, m.home_red_cards, m.away_red_cards
		FROM historic_player_per_ninety hpn
		JOIN match m
			ON m.season = '{game_season}'
			AND m.home_team_id = '{home_team_id}'
			AND m.away_team_id = '{away_team_id}'
		WHERE player_id IN ( 
			SELECT player_id FROM historic_player_per_ninety hpn
			JOIN match m
				ON m.season = '{game_season}'
				AND m.home_team_id = '{home_team_id}'
				AND m.away_team_id = '{away_team_id}'
				AND hpn.team_id IN (m.home_team_id, m.away_team_id)
			WHERE hpn.season {less_than_or_equal_to} '{game_season}'
		)
			AND hpn.season {less_than_or_equal_to} '{game_season}'
	""")

def create_prediction_player_stats_for_match(game_season: str, home_team_id: str, away_team_id: str, less_than_or_equal_to:str) -> pd.DataFrame:
	"""
	Create player statistics for a match.

	Args:
		game_season (str): The season of the match.
		home_team_id (str): The ID of the home team.
		away_team_id (str): The ID of the away team.
		less_than_or_equal_to (str): The condition for filtering the player statistics.

	Returns:
		pd.DataFrame: The DataFrame containing the player statistics for the match.
	"""
	return db.get_df(f"""
		SELECT 
			hpn.*
		FROM 
			historic_player_per_ninety hpn
		WHERE 
			hpn.season {less_than_or_equal_to} '{game_season}'
			AND hpn.player_id IN (
				SELECT 
					player_id
				FROM
					player_team pt
				WHERE 
					season = '{game_season}'
					AND team_id IN ('{home_team_id}', '{away_team_id}')
			)
	""")



def get_all_players_in_match(season: str, home_team_id: str, away_team_id: str, match_id: str) -> pd.DataFrame:
	"""
	Retrieves the player statistics for a given match.

	Args:
		season (str): The season of the match.
		home_team_id (str): The ID of the home team.
		away_team_id (str): The ID of the away team.
		match_id (str): The ID of the match.

	Returns:
		pd.DataFrame: The DataFrame containing the player statistics for the match.
	"""
	columns_to_remove = ["_plus_", "_minus", "_divided_by_",]

	df = create_player_stats_for_match(season, home_team_id, away_team_id)

	columns = [col for col in df.columns if any(word in col for word in columns_to_remove)]
	df = df.drop(columns=columns)

	return df

def group_stats_by_player_for_home_and_away_teams(df: pd.DataFrame, home_team_id: str, away_team_id:str, home_team_squad_ids:list = None, pred: bool = False) -> pd.DataFrame:
	"""
	Groups the statistics of players by their player_id for the specified home and away teams.

	Args:
		df (pd.DataFrame): The input DataFrame containing player statistics.
		home_team_id (str): The ID of the home team.
		away_team_id (str): The ID of the away team.
		home_team_squad_ids (list): The list of player IDs in the home team's squad.
		pred (bool, optional): Indicates whether the function is used for prediction. Defaults to False.

	Returns:
		pd.DataFrame: The DataFrame with player statistics grouped by player_id.
	"""
	unique_player_ids = df['player_id'].unique().tolist()
	
	# TODO: Look at this again
	# EDGE CASE: A player has played for both the teams playing against each other in the same season
	home_team_mask = df["player_id"].isin(home_team_squad_ids)

	if home_team_squad_ids:
		df["team_id"] = np.where(df["player_id"].isin(unique_player_ids), np.where(home_team_mask, home_team_id, away_team_id), df["team_id"])
	else:
		df['team_id'] = df.groupby('player_id')['team_id'].transform(lambda x: x.loc[x['season'].idxmax()])

	if pred:

		df = (
			df
			.groupby(["player_id", "season", "team_id"]) # team_id included in the group by as it is not a numerical column that can be summed, but the values for each player id should be consistent, as this is changed above
			.sum()
			.reset_index()
		)
		df = df.drop(columns=["season"])

		df = (
			df
			.groupby(["player_id", "team_id"]) # team_id included in the group by as it is not a numerical column that can be averaged, but each player should only have one distinct team_id, either the home or away team
			.mean()
			.reset_index()
		)

		print(df)

	else:
		df[player_stats_columns] = (
			df[player_stats_columns+["season"]]
			.groupby(["player_id", "season"])
			.sum()
			.reset_index()
			[player_stats_columns]
			.groupby("player_id")
			.mean()
			.reset_index()
		)

	df = df[df.index < df["player_id"].nunique()]

	return df

def create_per_90_stats(df: pd.DataFrame, columns_to_evaluate: list = None) -> pd.DataFrame:
	"""
	Create per 90 minutes statistics for the given DataFrame.

	Args:
		df (pd.DataFrame): The DataFrame containing the statistics.
		columns_to_evaluate (list, optional): The list of columns to evaluate. Defaults to None.

	Returns:
		pd.DataFrame: The DataFrame with per 90 minutes statistics.
	"""
	ninety_mins_per_season = 38

	# Use vectorized operations to update pure_stats_columns
	df[columns_to_evaluate] /= ninety_mins_per_season

	return df

def create_contribution_per_90_stats(df: pd.DataFrame, columns_to_evaluate: list = None) -> pd.DataFrame:
	"""
	Creates contribution per 90 minutes statistics for the given DataFrame.

	Args:
		df (pd.DataFrame): The input DataFrame containing the statistics.
		pred (bool): Whether the function is used during prediction (default is False).
		columns_to_evaluate (list): List of columns to evaluate for contribution per 90 minutes statistics.

	Returns:
		pd.DataFrame: The modified DataFrame with contribution per 90 minutes statistics.
	"""
	minutes_per_game = 90
	
	# Use vectorized operations to update pure_stats_columns
	df[columns_to_evaluate] = df[columns_to_evaluate].multiply(df["minutes_played"] / minutes_per_game, axis=0)

	# Drop the "minutes_played" column
	df = df.drop(columns=["minutes_played"])

	return df

def group_stats_by_team(df: pd.DataFrame, columns_to_evaluate: list = None) -> pd.DataFrame:
	"""
	Groups the player statistics in the DataFrame by team and returns a new DataFrame with team statistics.

	Args:
		df (pd.DataFrame): The input DataFrame containing player statistics.
		columns_to_evaluate (list, optional): The list of columns to evaluate. Defaults to None.

	Returns:
		pd.DataFrame: The new DataFrame with team statistics.

	"""
	df = df.drop(columns=["player_id"])
	df[columns_to_evaluate] = df[columns_to_evaluate].groupby("team_id").sum().reset_index()
	return df[df.index < df["team_id"].nunique()]

def convert_team_rows_to_single_row(df: pd.DataFrame, home_team_id: str = None, away_team_id: str = None, columns_to_evaluate: list = None) -> pd.DataFrame:
    """
    Converts team rows in a DataFrame to a single row.

    Args:
        df (pd.DataFrame): The DataFrame containing team rows.
        home_team_id (str, optional): The ID of the home team. If not provided, it will be inferred from the 'home_team_id' column.
        away_team_id (str, optional): The ID of the away team. If not provided, it will be inferred from the 'away_team_id' column.
        columns_to_evaluate (list, optional): A list of column names to evaluate and compute the difference between home and away teams. If not provided, all columns will be included.

    Returns:
        pd.DataFrame: A DataFrame with a single row representing the teams, including the specified columns with differences calculated between home and away teams.
    """
    home = home_team_id or df["home_team_id"].unique().tolist()[0]
    away = away_team_id or df["away_team_id"].unique().tolist()[0]

    # Create a mask for home and away teams
    home_mask = df["team_id"] == home
    away_mask = df["team_id"] == away

    # Create a mask for the columns to evaluate
    columns_mask = df.columns.isin(columns_to_evaluate) if columns_to_evaluate else slice(None)

    # Initialize the final_df with the home team's values
    final_df = df.loc[home_mask, :].copy()

    # Calculate the difference for columns to evaluate
    final_df.loc[:, columns_mask] = df.loc[home_mask, columns_mask].values - df.loc[away_mask, columns_mask].values

    # Reset the index to a single row
    final_df.reset_index(drop=True, inplace=True)

    return final_df



def create_career_and_form_dataframes_for_database(match_values: list) -> dict:
	"""
	Create career and form dataframes for a given match.

	Args:
		match_values (list): A list containing the home team ID, away team ID, and season.

	Returns:
		dict: A dictionary containing the career and form dataframes.

	"""
	home_team_id = match_values[0]
	away_team_id = match_values[1]
	season = match_values[2]

	columns_to_remove = ["_plus_", "_minus", "_divided_by_",]

	career_df = create_player_stats_for_match(season, home_team_id, away_team_id, "<")
	form_df = create_player_stats_for_match(season, home_team_id, away_team_id, "=")

	dfs = {}

	for key, df in {"career": career_df, "form": form_df}.items():
		columns = [col for col in df.columns if any(word in col for word in columns_to_remove)]
		df = df.drop(columns=columns)

		df = group_stats_by_player_for_home_and_away_teams(df)


		if df["team_id"].nunique() < 2:
			continue

		df = create_per_90_stats(df, pure_stats_columns)
		df = create_contribution_per_90_stats(df, pure_stats_columns)
		df = group_stats_by_team(df, team_stats_columns)
		df = convert_team_rows_to_single_row(df, pure_stats_columns)

		dfs[key] = df

	return dfs

def combine_form_and_career_stats(dfs: tuple, pred: bool = False, columns_to_evaluate: list = None, match_columns: list = match_columns) -> pd.DataFrame:
	"""
	Combines the career and form statistics for a player.

	Args:
		dfs (tuple): A tuple containing the career and form DataFrames.
		pred (bool): Flag indicating if the function is used for prediction.
		columns_to_evaluate (list): List of columns to evaluate and combine.
		match_columns (list): List of columns related to match information.

	Returns:
		pd.DataFrame: The combined DataFrame.
	"""
	career_df = dfs[0]
	form_df = dfs[1]

	career_stats_ratio = 0.6
	form_stats_ratio = 0.4

	career_df[columns_to_evaluate] = career_df[columns_to_evaluate] * career_stats_ratio
	form_df[columns_to_evaluate] = form_df[columns_to_evaluate] * form_stats_ratio

	all_stats = pd.concat([career_df, form_df])

	# Combined stats for all the players on both teams
	if pred:
		all_stats = all_stats[columns_to_evaluate]
		all_stats.loc[:, "match"] = "m"
		all_stats = all_stats.groupby("match").sum().reset_index(drop=True)
		return all_stats

	all_match_stats = all_stats[columns_to_evaluate + ["match_id"]]
	# Match facts for all games
	all_match_facts = all_stats[match_columns].drop_duplicates(subset='match_id')

	combined = all_match_stats.groupby("match_id").sum().reset_index()
	combined = combined.merge(all_match_facts, how="inner", on=["match_id"])

	combined.drop(columns=["ninetys", "team_id"], inplace=True)

	return combined



def get_current_season() -> str:
	"""
	Get the current season based on the current date.

	Returns:
		str: The current season.
	"""
	current_date = datetime.datetime.now()
	current_year = current_date.year
	current_month = current_date.month

	if current_month < 8:
		current_year -= 1

	return f"{current_year}-{current_year + 1}"

def remove_unavailable_players_from_df(df: pd.DataFrame, squad_list: list) -> pd.DataFrame:
	"""
	Removes players not in the squad list from the DataFrame.

	Args:
		df (pd.DataFrame): The DataFrame containing the player statistics.
		squad_list (list): The list of player IDs.

	Returns:
		pd.DataFrame: The modified DataFrame.
	"""
	df = df[df["player_id"].isin(squad_list)]

	return df

def grouping_prediction_dataframe_rows(df: pd.DataFrame, home_team_id: str, home_team_squad_ids: list, away_team_id:str, pred: bool = False) -> pd.DataFrame:

	columns_to_remove = ["_plus_", "_minus", "_divided_by_",]
	columns = [col for col in df.columns if any(word in col for word in columns_to_remove)]
	df = df.drop(columns=columns)

	df = group_stats_by_player_for_home_and_away_teams(df, home_team_id, away_team_id, home_team_squad_ids, pred)

	if df["team_id"].nunique() < 2:
		sys.exit("Not enough players in each team available for prediction")

	df = create_per_90_stats(df, pure_stats_columns)
	print("\n\nper 90 stats\n",df)
	df = create_contribution_per_90_stats(df, pure_stats_columns)
	print("\n\ncontributions per 90\n",df)
	df = group_stats_by_team(df, team_stats_columns)
	print("\n\ngroup stats by team\n",df)
	df = convert_team_rows_to_single_row(df, home_team_id, away_team_id, pure_stats_columns)
	print("\n\nsingle row\n",df)

	return df



def create_dataset() -> pd.DataFrame:
	"""
	Create a dataset for match predictions.

	Returns:
		pd.DataFrame: The combined dataset containing player stats and match facts.
	"""
	all_matches = db.get_list("SELECT home_team_id, away_team_id, season, id FROM match")

	complete_player_career_stats_for_match_df = pd.DataFrame()
	complete_player_form_stats_for_match_df = pd.DataFrame()

	
	for match in all_matches:
		dfs = create_career_and_form_dataframes_for_database(match)

		for key, df in dfs.items():
			if key == "career" and complete_player_career_stats_for_match_df.empty:
				complete_player_career_stats_for_match_df = df.copy(deep=True)
			elif key == "form" and complete_player_form_stats_for_match_df.empty:
				complete_player_form_stats_for_match_df = df.copy(deep=True)
			elif key == "career":
				complete_player_career_stats_for_match_df = pd.concat([complete_player_career_stats_for_match_df, df])
			else:
				complete_player_form_stats_for_match_df = pd.concat([complete_player_form_stats_for_match_df, df])

		career_stats = complete_player_career_stats_for_match_df.copy(deep=True)
		form_stats = complete_player_form_stats_for_match_df.copy(deep=True)

		return combine_form_and_career_stats((career_stats, form_stats), columns_to_evaluate=stats_columns)
	
def create_prediction_dataset(home_team_id: str, home_team_squad: list, away_team_id: str, away_team_squad: list) -> pd.DataFrame:
		
	home_team_squad_ids = db.get_list(f"""
		SELECT player_id FROM player_team
		JOIN player ON player.id = player_team.player_id
		WHERE
			player_team.team_id = '{home_team_id}'
			AND CONCAT(player.first_name, ' ', player.last_name) IN ('{"','".join(home_team_squad)}')
	""")
	away_team_squad_ids = db.get_list(f"""
		SELECT player_id FROM player_team
		JOIN player ON player.id = player_team.player_id
		WHERE
			player_team.team_id = '{away_team_id}'
			AND CONCAT(player.first_name, ' ', player.last_name) IN ('{"','".join(away_team_squad)}')
	""")
	home_team_squad_ids = list(set([player_id[0] for player_id in home_team_squad_ids]))
	away_team_squad_ids = list(set([player_id[0] for player_id in away_team_squad_ids]))
	

	season = get_current_season()

	career = create_prediction_player_stats_for_match(season, home_team_id, away_team_id, "<")
	form = create_prediction_player_stats_for_match(season, home_team_id, away_team_id, "=")

	career = remove_unavailable_players_from_df(career, home_team_squad_ids+away_team_squad_ids)
	form = remove_unavailable_players_from_df(form, home_team_squad_ids+away_team_squad_ids)
	
	career = grouping_prediction_dataframe_rows(career, home_team_id, home_team_squad_ids, away_team_id, True)
	form = grouping_prediction_dataframe_rows(form, home_team_id, home_team_squad_ids, away_team_id, True)

	if career.empty or form.empty:
		return None

	return combine_form_and_career_stats((career, form), pred=True, columns_to_evaluate=stats_columns)

	
