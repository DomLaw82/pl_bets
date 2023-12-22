import pandas as pd
import numpy as np
from db_connection import local_pl_stats_connector
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import plotly.express as px

db = local_pl_stats_connector

def create_player_stats_for_match(game_season: str, home_team_id: str, away_team_id: str) -> pd.DataFrame:
	"""
		Generate a dataframe containing all the career stats of the players (up to and including season of the game in question) 
		playing in a specific match
	"""
	return db.get_df(f"""
		SELECT hpn.*, pt.team_id FROM historic_player_per_ninety hpn
		JOIN player_team pt ON pt.player_id = hpn.player_id
		WHERE hpn.season <= '{game_season}'
		AND pt.player_id IN (
			SELECT player_id FROM player_team 
			WHERE team_id IN ('{home_team_id}', '{away_team_id}')
			AND season = '{game_season}'
		)
	""")


def create_match_facts_for_match(game_season: str, home_team_id: str, away_team_id: str) -> pd.DataFrame:
	"""
		Generate a dataframe containing all the match facts based on the season and teams
	"""
	return db.get_df(f"""
		SELECT * FROM match 
		WHERE season = '{game_season}' and home_team_id = '{home_team_id}' and away_team_id = '{away_team_id}'
	""")

def get_match_column_values(all_matches: pd.DataFrame) -> list:
	columns_to_extract = ["home_team_id", "away_team_id", "season"]
	values_list = []

	for index, row in all_matches.iterrows():
		row_values = [row[column] for column in columns_to_extract]
		values_list.append(row_values)

	return values_list

if __name__ == "__main__":

# Query to the database is written based on:
	# The teams playing (home, away)
	# Season the match is taking place in

	all_matches = db.get_df("SELECT * FROM match")
	match_values = get_match_column_values(all_matches)

	complete_dataset = pd.DataFrame()

	for match in match_values:

		season = match[2]
		home_team_id = match[0]
		away_team_id = match[1]

		players_in_match = create_player_stats_for_match(season, home_team_id, away_team_id)
		# combine all rows for all the players into one row row the match
		print(players_in_match)
		break
		# join the match facts for the game to the player dataframe row
		# append to complete match dataframe

	# all_player_historic_stats = db.get_df("SELECT * FROM historic_player_per_ninety")


	# output_columns = [
	# 	"home_goals", "away_goals", "home_shots", "away_shots", "home_shots_on_target", "away_shots_on_target",
	# 	"home_corners", "away_corners", "home_fouls", "away_fouls", "home_yellow_cards", "away_yellow_cards",
	# 	"home_red_cards", "away_red_cards"
	# ]

	# columns_to_remove = ["_plus_", "_minus", "_divided_by_",]
	
	# player_stats_columns = [
	# 	"player_id", "minutes_played","ninetys","goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	# 	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	# 	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	# 	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	# 	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	# 	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed","season"
	# ]

	# player_all_stats = all_player_historic_stats[player_stats_columns].groupby("player_id").sum() / all_player_historic_stats.groupby("player_id")["season"].nunique()
	# player_current_season_stats = max_season = all_player_historic_stats[player_stats_columns][all_player_historic_stats["season"] == all_player_historic_stats["season"].max()]

	# columns_to_divide = [
	# 	"minutes_played","ninetys","goals","assists","non_penalty_goals","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
	# 	"non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","progressive_passes_received","total_passing_distance","total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed","medium_passes_attempted",
	# 	"long_passes_completed","long_passes_attempted","expected_assists","key_passes","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target","average_shot_distance","shots_from_free_kicks",
	# 	"shots_from_penalties","touches","touches_in_defensive_penalty_area","touches_in_defensive_third","touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches","take_ons_attempted","take_ons_succeeded","times_tackled_during_take_on",
	# 	"carries","total_carrying_distance","progressive_carrying_distance","carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received","tackles","tackles_won","defensive_third_tackles",
	# 	"middle_third_tackles","attacking_third_tackles","dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances","errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced","penalties_allowed","penalties_saved","penalties_missed","season"
	# ]

	# for col in columns_to_divide:
	# 	player_all_stats[col] = np.where(player_all_stats['ninetys'] == 0, 0, player_all_stats[col] / player_all_stats['ninetys'])
	# 	player_current_season_stats[col] = np.where(player_current_season_stats['ninetys'] == 0, 0, player_current_season_stats[col] / player_current_season_stats['ninetys'])

	# career_stats = player_all_stats.drop(columns=["player_id", "ninetys", "minutes_played", "penalties_allowed", "penalties_saved", "penalties_missed"])
	# season_stats = player_current_season_stats.drop(columns=["player_id", "ninetys", "minutes_played", "penalties_allowed", "penalties_saved", "penalties_missed"])
	
	# scaler = StandardScaler(copy=True)

	# career_stats_standardized = scaler.fit_transform(career_stats)	
	# season_stats_standardized = scaler.fit_transform(season_stats)

	# n=13

	# pca = PCA(n_components = n, random_state=938)

	# pca.fit(career_stats_standardized)
	# feature_to_pc_map_career = pd.DataFrame(pca.components_, columns=career_stats_standardized.columns)
	# components_career = pca.transform(career_stats_standardized)
	# components_career_df = pd.DataFrame(data=components_career[:, [p for p in range(n)]], columns=pca.get_feature_names_out(), )

	# pca.fit(season_stats_standardized)
	# feature_to_pc_map_season = pd.DataFrame(pca.components_, columns=season_stats_standardized.columns)
	# components_season = pca.transform(season_stats_standardized)
	# components_season_df = pd.DataFrame(data=components_season[:, [p for p in range(n)]], columns=pca.get_feature_names_out(), )

	# Output Layer Activator - ReLU

	