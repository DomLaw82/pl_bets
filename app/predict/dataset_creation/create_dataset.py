import pandas as pd
from dataset_creation.db_connection import local_pl_stats_connector

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
player_stats_columns = [
	"player_id", "minutes_played","ninetys","goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]
pure_stats_columns = [
	"minutes_played","goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]
pure_stats_columns_no_minutes = [
	"goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]
team_stats_columns = [
	"team_id", "goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed"
]

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

def get_match_column_values(all_matches: pd.DataFrame) -> list:
	"""
	Extracts specific columns from a DataFrame of matches and returns a list of their values.

	Parameters:
		all_matches (pd.DataFrame): A DataFrame containing match data.

	Returns:
		list: A list of lists, where each inner list contains the values of the specified columns for each match.
	"""
	columns_to_extract = ["home_team_id", "away_team_id", "season", "id"]
	values_list = []

	for index, row in all_matches.iterrows():
		row_values = [row[column] for column in columns_to_extract]
		values_list.append(row_values)

	return values_list

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

def group_stats_by_player_for_home_and_away_teams(df: pd.DataFrame, home_team_id: str, away_team_id:str) -> pd.DataFrame:
	"""
	Groups the statistics of players by their player_id for the specified home and away teams.

	Args:
		df (pd.DataFrame): The input DataFrame containing player statistics.
		home_team_id (str): The ID of the home team.
		away_team_id (str): The ID of the away team.

	Returns:
		pd.DataFrame: The DataFrame with player statistics grouped by player_id.
	"""
	specified_team_ids = [home_team_id, away_team_id]
	unique_player_ids = df['player_id'].unique().tolist()

	for player_id in unique_player_ids:
		teams_played_for = df[df["player_id"] == player_id]["team_id"].unique().tolist()
		if specified_team_ids[0] in teams_played_for:
			df.loc[df["player_id"] == player_id, "team_id"] = specified_team_ids[0]
		if specified_team_ids[1] in teams_played_for:
			df.loc[df["player_id"] == player_id, "team_id"] = specified_team_ids[1]
			
	# Apply the custom aggregation function to "team_id" while grouping by "player_id"
	df[player_stats_columns] = (
		df[player_stats_columns]
		.groupby("player_id")
		.sum()
		.div(df.groupby("player_id")["season"].nunique(), axis=0)
		.reset_index()
	)

	df = df[df.index < df["player_id"].nunique()]

	return df

def create_per_90_stats(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Create per 90 minutes statistics for the given DataFrame.

	Args:
		df (pd.DataFrame): The DataFrame containing the statistics.

	Returns:
		pd.DataFrame: The DataFrame with per 90 minutes statistics.

	"""
	ninety_mins_per_season = 38

	df.loc[:, pure_stats_columns] = df[pure_stats_columns].apply(lambda x: x / ninety_mins_per_season)
	return df

def create_contribution_per_90_stats(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Creates contribution per 90 minutes statistics for the given DataFrame.

	Args:
		df (pd.DataFrame): The input DataFrame containing the statistics.

	Returns:
		pd.DataFrame: The modified DataFrame with contribution per 90 minutes statistics.

	"""
	minutes_per_game = 90

	df[pure_stats_columns] = df[pure_stats_columns].apply(lambda x: x * (df["minutes_played"] / minutes_per_game))
	df = df.drop(columns=["minutes_played"])
	pure_stats_columns.remove("minutes_played")
	return df

def group_stats_by_team(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Groups the statistics in the DataFrame by team and returns a new DataFrame.

	Parameters:
		df (pd.DataFrame): The input DataFrame containing player statistics.

	Returns:
		pd.DataFrame: The new DataFrame with team statistics.

	"""
	df = df.drop(columns=["player_id"])
	df[team_stats_columns] = df[team_stats_columns].groupby("team_id").sum().reset_index()
	return df[df.index < df["team_id"].nunique()]

def convert_team_rows_to_single_row(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Converts team rows in a DataFrame to a single row.

	Args:
		df (pd.DataFrame): The DataFrame containing team rows.

	Returns:
		pd.DataFrame: The DataFrame with a single row representing the teams.
	"""
	home = df["home_team_id"].unique().tolist()[0]
	away = df["away_team_id"].unique().tolist()[0]

	columns = df.columns.to_list()
	final_df = {}

	for column in columns:
		if column in pure_stats_columns:
			value = df[column][df["team_id"] == home].iloc[0] - df[column][df["team_id"] == away].iloc[0] 
			final_df[column] = value
		else:
			final_df[column] = df[column][df["team_id"] == home].iloc[0]

	return pd.DataFrame(final_df, index=[0])

def create_dataset() -> pd.DataFrame:
	"""
	Create a dataset for match predictions.

	Returns:
		pd.DataFrame: The combined dataset containing player stats and match facts.
	"""
	all_matches = db.get_df("SELECT * FROM match")
	match_values = get_match_column_values(all_matches)

	complete_player_career_stats_for_match_df = pd.DataFrame()
	complete_player_form_stats_for_match_df = pd.DataFrame()

	columns_to_remove = ["_plus_", "_minus", "_divided_by_",]

	for match in match_values:

		season = match[2]
		home_team_id = match[0]
		away_team_id = match[1]

		career_df = create_player_stats_for_match(season, home_team_id, away_team_id, "<")
		form_df = create_player_stats_for_match(season, home_team_id, away_team_id, "=")

		if career_df.empty or form_df.empty:
			continue
		
		for key, df in {"career": career_df, "form": form_df}.items():
			columns = [col for col in df.columns if any(word in col for word in columns_to_remove)]
			df = df.drop(columns=columns)

			df = group_stats_by_player_for_home_and_away_teams(df)

			if df["team_id"].nunique() < 2:
				continue

			df = create_per_90_stats(df)
			df = create_contribution_per_90_stats(df)
			df = group_stats_by_team(df)
			df = convert_team_rows_to_single_row(df)

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

		career_stats_ratio = 0.6
		form_stats_ratio = 0.4

		career_stats[pure_stats_columns_no_minutes] = career_stats[pure_stats_columns_no_minutes] * career_stats_ratio
		form_stats[pure_stats_columns_no_minutes] = form_stats[pure_stats_columns_no_minutes] * form_stats_ratio

		all_stats = pd.concat([career_stats, form_stats])
		# Combined stats for all the players on both teams
		all_match_stats = all_stats[pure_stats_columns_no_minutes + ["match_id"]]
		#Match facts for all games
		all_match_facts = all_stats[match_columns].drop_duplicates(subset='match_id')

		combined = all_match_stats.groupby("match_id").sum().reset_index()
		combined = combined.merge(all_match_facts, how="inner", on=["match_id"])

		return combined

	