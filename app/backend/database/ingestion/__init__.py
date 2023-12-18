from db_connector import local_pl_stats_connector
from data_intake.format_season_schedule import schedule_main
from data_intake.team_match_data import rename_team_name, rename_table_columns, create_teams_table, create_referee_table, select_match_columns
from data_intake.squad_data import get_team_squad, format_player_entries, not_blank_entry
from utilities.unique_id import get_team_id, get_player_id
from utilities.remove_duplicates import remove_duplicate_rows
from utilities.string_manipulation import escape_single_quote
import os, re
from datetime import datetime
import pandas as pd

# Ingest locally stored data into the database

# format season schedule [schedule]
schedule_main(local_pl_stats_connector, "./app/data_intake/schedule_data")
    
# format game data [team, match, referee]
SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2017, 2025, 1)]
TABLE_SEASONS = [f"{str(year-1)}-{str(year)[-2:]}" for year in range(2017, 2025, 1)]

data_folder_path = "./app/data_intake/game_data"

data = sorted(os.listdir(data_folder_path))

for year in data:
	season = re.findall("\d{4}", year)[0]
	season = season[:2]+"-"+season[-2:]
	full_season = TABLE_SEASONS[data.index(year)]
      
	path = data_folder_path+"/"+year
	
	df = pd.read_csv(path)

	year_df = rename_table_columns(df, full_season, '001')
	year_df.loc[:, "referee_id"] = year_df.apply(lambda row: escape_single_quote(row.referee_id), axis=1)
	year_df.loc[:, "home_team_id"] = year_df.apply(lambda row: rename_team_name(row.home_team_id), axis=1)
	year_df.loc[:, "away_team_id"] = year_df.apply(lambda row: rename_team_name(row.away_team_id), axis=1)
	
	team_df = create_teams_table(year_df, local_pl_stats_connector)
	referee_df = create_referee_table(year_df, local_pl_stats_connector)
	match_df = select_match_columns(year_df, local_pl_stats_connector)
	
	team_df.to_sql("team", local_pl_stats_connector.conn, if_exists="append", index=False) if not team_df.empty else None
	referee_df.to_sql("referee", local_pl_stats_connector.conn, if_exists="append", index=False) if not referee_df.empty else None
	match_df.to_sql("match", local_pl_stats_connector.conn, if_exists="append", index=False)

# format squad data [player, player_team]
data_folder_path = "./app/data_intake/squad_data"

seasons = sorted(os.listdir(data_folder_path))

for season in seasons:

	season_folder = data_folder_path + "/" + season 

	teams = sorted(os.listdir(season_folder))
	
	for team in teams:
		html_content = ""
		with open(f"{season_folder+'/'+team}", "r") as file:
			html_content = file.read()
		# 
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

		rows_not_in_db_df = remove_duplicate_rows(local_pl_stats_connector, player_df, ["first_name", "last_name", "birth_date", "position"], "player")
		if rows_not_in_db_df.empty:
			continue
		rows_not_in_db_df.to_sql("player", local_pl_stats_connector.conn, if_exists="append", index=False)

		player_team_df.loc[:, "player_id"] = df.apply(lambda row: get_player_id(local_pl_stats_connector, row), axis=1)
		player_team_df.loc[:, "team_id"] = df.apply(lambda row: get_team_id(local_pl_stats_connector, row.team_id), axis=1)

		df["season"] = season

		player_team_df = player_team_df[["player_id", "team_id", "season"]]
		player_team_df = remove_duplicate_rows(local_pl_stats_connector, player_team_df, ["player_id", "team_id", "season"], "player_team")
		player_team_df.to_sql("player_team", local_pl_stats_connector.conn, if_exists="append", index=False)

	
# TODO - country, competition, historic_player_per_ninety

	

	