from db_connector import local_pl_stats_connector
from data_intake.team_match_data import rename_team_name, rename_table_columns, create_teams_table, create_referee_table, select_match_columns
from data_intake.squad_data import main
from data_intake.team_match_data import main
from utilities.unique_id import get_team_id
from utilities.string_manipulation import escape_single_quote
import os, re, time
import pandas as pd

# Ingest locally stored data into the database

# format season schedule
season_schedule_folder_path = "./app/data_intake/schedule_data"

season_schedules = sorted(os.listdir(season_schedule_folder_path))

for season in season_schedules:
    path = season_schedule_folder_path + "/" + season
    df = pd.read_csv(path)
    df.columns = ["_".join(col.lower().split(" ") )for col in df.columns.to_list()]

    df.loc[:, "home_team"] = df.apply(lambda row: rename_team_name(row.home_team.title()), axis=1)
    df.loc[:, "away_team"] = df.apply(lambda row: rename_team_name(row.away_team.title()), axis=1)
    
    df.loc[:, "home_team"] = df.apply(lambda row: get_team_id(local_pl_stats_connector, row.home_team), axis=1)
    df.loc[:, "away_team"] = df.apply(lambda row: get_team_id(local_pl_stats_connector, row.away_team), axis=1)
    
    df.to_sql("schedule", local_pl_stats_connector.conn, if_exists="append", index=False)
    
# format game data
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

# format squad data
teams_links = get_all_teams_for_season(soup)

player_team_season = f"{SEASON[2:4]}/{SEASON[-3:-1]}"
season_squads = {}

for team_link in teams_links:
	time.sleep(1)
	team = team_link[0]
	link = team_link[1]
	
	squad = get_team_squad(link, SEASON, PLAYERS_WEBSITE_ROOT)
	squad_no_blanks = [player for player in squad if not_blank_entry(player)]
	squad_with_team = [player + [team] for player in squad_no_blanks]
	complete_squad = [format_player_entries(player) for player in squad_with_team]

	squad_df = DataFrame(data=complete_squad, columns=["first_name", "last_name", "position", "birth_date", "team_id"])
	squad_df.loc[:, "birth_date"] = squad_df.apply(lambda row: datetime.date(datetime.strptime(row.birth_date, "%Y-%m-%d")), axis=1)

	df = df[["first_name", "last_name", "birth_date", "position"]]
	df.loc[:, "first_name"] = df.apply(lambda row: escape_single_quote(row.first_name), axis=1)
	df.loc[:, "last_name"] = df.apply(lambda row: escape_single_quote(row.last_name), axis=1)
	rows_not_in_db_df = remove_duplicate_rows(local_pl_stats_connector, df, ["first_name", "last_name", "birth_date", "position"], "player")
	if rows_not_in_db_df.empty:
		return
	rows_not_in_db_df.to_sql("player", local_pl_stats_connector.conn, if_exists="append", index=False)