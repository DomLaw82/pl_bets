import pandas as pd, numpy as np
import os
from app_logger import FluentLogger
from db_connection import SQLConnection
from data_intake.utilities.unique_id import get_id_from_name, get_name_from_database
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("intake-match_logs").get_logger()

def match_logs_main(connector: SQLConnection) -> None:
	try:
		logger.info("Ingesting match logs data")
		
		data = pd.read_csv("data/fbref_data/enhanced_player_match_logs.csv")
		logger.info("Data loaded successfully")

		##### --------------------------------------------------------------------------------------------#####
		##### Only EPL data is being used as of now, other matches not captured in match table            #####
		##### This is a temporary solution, need to update the match table to include all matches         #####
		##### i.e. matches from other leagues/competitions                                                #####
		##### Currently all teams stored in the database are from the English Premier League              #####
		data = data[data["competition"] == "Premier League"]
		data["team"] = data["team"].apply(lambda x: get_name_from_database(connector, x, "team"))
		data["opponent"] = data["opponent"].apply(lambda x: get_name_from_database(connector, x, "team"))
		data = data[(data["team"].notnull()) & (data["opponent"].notnull())]
		logger.info("Data filtered for Premier League matches")
		##### --------------------------------------------------------------------------------------------#####

		for player in data["player_name"].unique():
			logger.info(f"Fetching player ID for {player}")
			player_id = get_id_from_name(connector, player, "player")
			if not player_id:
				logger.info(f"Player ID not found for {player}")
				continue
			data.loc[data["player_name"] == player, "player_id"] = player_id
			fbref_id = data[data["player_name"] == player]["fbref_id"].values[0]
			connector.execute(f"UPDATE player SET fbref_id = '{fbref_id}' WHERE id = '{player_id}'")
		logger.info("Player IDs fetched successfully")

		unique_teams = pd.concat([data["team"], data["opponent"]]).unique()
		for team in unique_teams:
			logger.info(f"Fetching team ID for {team}")
			team_id = get_id_from_name(connector, team, "team")
			if not team_id:
				logger.info(f"Team ID not found for {team}")
				continue
			data.loc[data["team"] == team, "team_id"] = team_id
			data.loc[data["opponent"] == team, "opponent_id"] = team_id
		logger.info("Team IDs fetched successfully")
		

		data["home_team_id"] = np.where(data["location"] == "Home", data["team_id"], data["opponent_id"])
		data["away_team_id"] = np.where(data["location"] == "Away", data["team_id"], data["opponent_id"])

		data["home_team_id"] = np.where(
			(
				(data["location"] == "Home")
				| ((data["location"] == "Neutral") & (data["result"].str[0] == "W") & (data["result"].str[2].astype(int) > data["result"].str[4].astype(int)))
				| ((data["location"] == "Neutral") & (data["result"].str[0] == "L") & (data["result"].str[4].astype(int) > data["result"].str[2].astype(int)))
				| ((data["location"] == "Neutral") & (data["result"].str[0] == "D"))
			),
			data["team_id"],
			data["opponent_id"]
		)
		data["away_team_id"] = np.where(
			(
				(data["location"] == "Away")
				| ((data["location"] == "Neutral") & (data["result"].str[0] == "W") & (data["result"].str[2].astype(int) < data["result"].str[4].astype(int)))
				| ((data["location"] == "Neutral") & (data["result"].str[0] == "L") & (data["result"].str[4].astype(int) < data["result"].str[2].astype(int)))
			),
			data["team_id"],
			data["opponent_id"]
		)
		logger.info("Team IDs fetched successfully")

		for competition in data["competition"].unique():
			logger.info(f"Fetching competition ID for {competition}")
			competition_id = get_id_from_name(connector, competition, "competition")
			if not competition_id:
				logger.info(f"Competition ID not found for {competition}")
				continue
			data.loc[data["competition"] == competition, "competition_id"] = competition_id
		logger.info("Competition IDs fetched successfully")

		match_id_data = connector.get_df("SELECT id AS match_id, competition_id, season, home_team_id, away_team_id FROM match")

		# Merge the match_id_data with the data DataFrame to get the match IDs
		data = data.merge(
			match_id_data,
			how='left',  # Use left join to keep all rows from data and only matching rows from match_id_data
			on=['season', 'home_team_id', 'away_team_id', 'competition_id']
		)

		# Log missing match IDs
		missing_matches = data[data['match_id'].isnull()]

		if not missing_matches.empty:
			# Get unique values of missing matches
			unique_missing_matches = missing_matches[['season', 'home_team_id', 'away_team_id', 'competition_id']].drop_duplicates()

			# Log the unique missing match details
			logger.warning(f"Missing {len(unique_missing_matches)} unique match IDs for entries: {unique_missing_matches.values}")

		logger.info("Match IDs fetched successfully")

		data[["minutes","goals","assists",
			"pens_made","pens_att","shots","shots_on_target","cards_yellow","cards_red","blocks","xg",
			"npxg","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short",
			"passes_completed_medium","passes_medium","passes_completed_long","passes_long","xg_assist","pass_xa",
			"assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area",
			"progressive_passes","tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd",
			"challenge_tackles","challenges","blocked_shots","blocked_passes","interceptions","clearances",
			"errors","touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd",
			"touches_att_pen_area","touches_live_ball","take_ons","take_ons_won","take_ons_tackled","carries",
			"carries_distance","carries_progressive_distance","progressive_carries","carries_into_final_third",
			"carries_into_penalty_area","miscontrols","dispossessed","passes_received","progressive_passes_received",
			"sca","sca_passes_live","sca_passes_dead","sca_take_ons","sca_shots","sca_fouled","sca_defense","gca",
			"gca_passes_live","gca_passes_dead","gca_take_ons","gca_shots","gca_fouled","gca_defense",
			"gk_shots_on_target_against","gk_goals_against","gk_saves","gk_clean_sheets","gk_psxg","gk_pens_att",
			"gk_pens_allowed","gk_pens_saved","gk_pens_missed","gk_passed_completed_launched","gk_passes_launched",
			"gk_passes","gk_passes_throws","gk_passes_length_avg","gk_goal_kicks","gk_goal_kicks_length_avg"]] = data[["minutes","goals","assists",
			"pens_made","pens_att","shots","shots_on_target","cards_yellow","cards_red","blocks","xg",
			"npxg","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short",
			"passes_completed_medium","passes_medium","passes_completed_long","passes_long","xg_assist","pass_xa",
			"assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area",
			"progressive_passes","tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd",
			"challenge_tackles","challenges","blocked_shots","blocked_passes","interceptions","clearances",
			"errors","touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd",
			"touches_att_pen_area","touches_live_ball","take_ons","take_ons_won","take_ons_tackled","carries",
			"carries_distance","carries_progressive_distance","progressive_carries","carries_into_final_third",
			"carries_into_penalty_area","miscontrols","dispossessed","passes_received","progressive_passes_received",
			"sca","sca_passes_live","sca_passes_dead","sca_take_ons","sca_shots","sca_fouled","sca_defense","gca",
			"gca_passes_live","gca_passes_dead","gca_take_ons","gca_shots","gca_fouled","gca_defense",
			"gk_shots_on_target_against","gk_goals_against","gk_saves","gk_clean_sheets","gk_psxg","gk_pens_att",
			"gk_pens_allowed","gk_pens_saved","gk_pens_missed","gk_passed_completed_launched","gk_passes_launched",
			"gk_passes","gk_passes_throws","gk_passes_length_avg","gk_goal_kicks","gk_goal_kicks_length_avg"]].fillna(0)

		data = data[[
			"player_id","fbref_id","competition_id","match_id","season","date","location",
			"team_id","opponent_id","position","started","minutes","goals","assists",
			"pens_made","pens_att","shots","shots_on_target","cards_yellow","cards_red","blocks","xg",
			"npxg","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short",
			"passes_completed_medium","passes_medium","passes_completed_long","passes_long","xg_assist","pass_xa",
			"assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area",
			"progressive_passes","tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd",
			"challenge_tackles","challenges","blocked_shots","blocked_passes","interceptions","clearances",
			"errors","touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd",
			"touches_att_pen_area","touches_live_ball","take_ons","take_ons_won","take_ons_tackled","carries",
			"carries_distance","carries_progressive_distance","progressive_carries","carries_into_final_third",
			"carries_into_penalty_area","miscontrols","dispossessed","passes_received","progressive_passes_received",
			"sca","sca_passes_live","sca_passes_dead","sca_take_ons","sca_shots","sca_fouled","sca_defense","gca",
			"gca_passes_live","gca_passes_dead","gca_take_ons","gca_shots","gca_fouled","gca_defense",
			"gk_shots_on_target_against","gk_goals_against","gk_saves","gk_clean_sheets","gk_psxg","gk_pens_att",
			"gk_pens_allowed","gk_pens_saved","gk_pens_missed","gk_passed_completed_launched","gk_passes_launched",
			"gk_passes","gk_passes_throws","gk_passes_length_avg","gk_goal_kicks","gk_goal_kicks_length_avg",
		]]
		data_duplicates = data[data.duplicated(subset=["player_id", "match_id"], keep=False)]
		logger.info(f"{data_duplicates.groupby(['player_id', 'match_id'])} duplicate records found:\n{data_duplicates}")
		print(data_duplicates)
		data = data.drop_duplicates(subset=["player_id","match_id"], keep="last")

		data.to_sql("match_logs", connector.engine, if_exists="append", index=False)
		logger.info("Match logs data ingested successfully")
	except Exception as e:
		logger.error(f"Error ingesting match logs data: line {e.__traceback__.tb_lineno} : {str(e)}")
		raise Exception(e)