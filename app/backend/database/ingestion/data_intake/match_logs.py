import pandas as pd
import os
from app_logger import FluentLogger
from db_connection import SQLConnection
from data_intake.utilities.unique_id import get_id_from_name


def match_logs_main(connector: SQLConnection) -> None:

	data = pd.read_csv("data/fbref_data/enhanced_player_match_logs.csv")

	player_id_data = connector.get_df("SELECT id, first_name || ' ' || last_name AS name FROM player")
	data["player_name"] = data["player_name"].apply(lambda x: get_id_from_name(x, player_id_data["name"].tolist()))
	data["player_id"] = data["player_name"].apply(lambda x: player_id_data[player_id_data["name"] == x]["id"].values[0])

	team_id_data = connector.get_df("SELECT id, name FROM team")
	data = data.rename(columns={"team": "home_team_id", "opponent": "away_team_id"})
	data["home_team_id"] = data["home_team_id"].apply(lambda x: get_id_from_name(x, team_id_data["name"].tolist()))
	data["home_team_id"] = data["home_team_id"].apply(lambda x: team_id_data[team_id_data["name"] == x]["id"].values[0])
	data["away_team_id"] = data["away_team_id"].apply(lambda x: get_id_from_name(x, team_id_data["name"].tolist()))
	data["away_team_id"] = data["away_team_id"].apply(lambda x: team_id_data[team_id_data["name"] == x]["id"].values[0])

	competition_id_data = connector.get_df("SELECT id, name FROM competition")
	data["competition"] = data["competition"].apply(lambda x: get_id_from_name(x, competition_id_data["name"].tolist()))
	data["competition_id"] = data["competition"].apply(lambda x: competition_id_data[competition_id_data["name"] == x]["id"].values[0])

	match_id_data = connector.get_df("SELECT id, competition_id, season, home_team_id, away_team_id FROM match")
	data["match_id"] = data.apply(lambda x: match_id_data[
		(match_id_data["season"] == x["season"])
		& (match_id_data["home_team_id"] == x["home_team_id"])
		& (match_id_data["away_team_id"] == x["away_team_id"])
		& (match_id_data["competition_id"] == x["competition_id"])
	]["id"].values[0], axis=1)

	data = data[[
		"player_id","fbref_id","competition_id","match_id","season","date","location",
		"home_team_id","away_team_id","result","position","started","minutes","goals","assists",
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

	data.to_sql("match_logs", connector.engine, if_exists="append", index=False)