import os, re
import pandas as pd
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.utilities.unique_id import *
from data_intake.utilities.string_manipulation import escape_single_quote

SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2017, 2025, 1)]
TABLE_SEASONS = [f"{str(year-1)}-{str(year)[-2:]}" for year in range(2017, 2025, 1)]

def rename_team_name(team_name:str) -> str:
    rename_teams = {
        "Leeds": "Leeds United",
        "Newcastle": "Newcastle United",
        "Tottenham": "Tottenham Hotspur",
        "Leicester": "Leicester City",
        "Man United": "Manchester United",
        "Brighton": "Brighton & Hove Albion",
        "Man City": "Manchester City",
        "Nott'm Forest": "Nottingham Forest",
        "Luton": "Luton Town",
        "Derby": "Derby County",
        "Birmingham": "Birmingham City",
        "Blackburn": "Blackburn Rovers",
        "Bolton": "Bolton Wanderers",
        "Hull": "Hull City",
        "Stoke": "Stoke City",
        "Wigan": "Wigan Athletic",
        "West Brom": "West Bromwich Albion",
        "Swansea": "Swansea City",
        "QPR": "Queens Park Rangers",
        "Wolves": "Wolverhampton Wanderers",
        "West Ham": "West Ham United",
        "Charlton": "Charlton Athletic",
        "Cardiff": "Cardiff City",
        "Huddersfield": "Huddersfield Town"
    }
    new_name = rename_teams.get(team_name) or team_name
    return new_name

def rename_table_columns(df: pd.DataFrame, season: str, competition_id: str) -> pd.DataFrame:
    df = df.rename(
        {
            "HomeTeam": "home_team_id", 
            "FTHG": "home_goals",
            "HS": "home_shots",
            "HST": "home_shots_on_target",
            "HY": "home_yellow_cards",
            "HR": "home_red_cards",
            "HC": "home_corners",
            "HF": "home_fouls",
            "AwayTeam": "away_team_id",
            "FTAG": "away_goals",
            "AS": "away_shots",
            "AST": "away_shots_on_target",
            "AC": "away_corners",
            "AF": "away_fouls",
            "AY": "away_yellow_cards",
            "AR": "away_red_cards",
            "Referee": "referee_id"
        }, 
        axis=1
    )
    df.loc[:, "season"] = season
    df.loc[:, "competition_id"] = competition_id

    return df

def select_match_columns(df: pd.DataFrame, db_connection) -> pd.DataFrame:
    new_df = df[
		[
			"season",
			"competition_id",
			"home_team_id",
			"away_team_id",
			"referee_id",
			"home_goals",
			"away_goals",
			"home_shots",
			"home_shots_on_target",
			"away_shots",
			"away_shots_on_target",
			"home_fouls",
			"home_yellow_cards",
			"home_red_cards",
			"away_fouls",
			"away_yellow_cards",
			"away_red_cards",
			"home_corners",
			"away_corners",
		]
	]

    new_df.loc[:, "home_team_id"] = new_df.apply(lambda row: get_team_id(db_connection, row.home_team_id), axis=1)
    new_df.loc[:, "away_team_id"] = new_df.apply(lambda row: get_team_id(db_connection, row.away_team_id), axis=1)
    
    new_df.loc[:, "referee_id"] = new_df.apply(lambda row: get_referee_id(db_connection, row.referee_id), axis=1)
    
    columns_to_compare = ["season", "competition_id", "home_team_id", "away_team_id"]
    final_df = remove_duplicate_rows(db_connection, new_df, columns_to_compare, "match")
    return final_df

def create_teams_table(df: pd.DataFrame, db_connection) -> pd.DataFrame:
    df = df.rename(columns={"home_team_id": "name"})
    only_new_teams_df = df.drop_duplicates(subset="name", keep="first")
    only_new_teams_df = remove_duplicate_rows(db_connection, only_new_teams_df, ["name"], "team").reset_index()
    return only_new_teams_df

def create_referee_table(df: pd.DataFrame, db_connection) -> pd.DataFrame:
    df = df.rename(columns={"referee_id": "name"})
    df = remove_duplicate_rows(db_connection, df, ["name"], "referee")
    referee_df = df[["name"]]
    return referee_df

def clean_match_data(db_connection) -> list:

    data_folder_path = "./data/game_data"

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
        
        team_df = create_teams_table(year_df, db_connection)
        referee_df = create_referee_table(year_df, db_connection)
        match_df = select_match_columns(year_df, db_connection)
        
        return [team_df, referee_df, match_df]

def save_to_database(db_connection, df: pd.DataFrame) -> None:
	df.to_sql("schedule", db_connection.conn, if_exists="append", index=False) if not df.empty else None


def team_ref_match_main(db_connection):

    team_ref_match_df = clean_match_data()

    for df in team_ref_match_df:
        save_to_database(db_connection, df)
