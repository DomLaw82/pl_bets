import os, re
import pandas as pd, numpy as np
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.utilities.unique_id import get_id_from_name, get_name_from_database
from data_intake.utilities.string_manipulation import escape_single_quote
from app_logger import FluentLogger
import time
from io import StringIO

logger = FluentLogger("intake-team_ref_match").get_logger()

SEASON_END_YEAR = 2026
SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2018, SEASON_END_YEAR, 1)]
TABLE_SEASONS = [f"{str(year-1)}-{str(year)}" for year in range(2018, SEASON_END_YEAR, 1)]

MATCH_SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2018, SEASON_END_YEAR)]
MATCH_LEAGUES = ["E0"] # Add leagues as needed
GAME_DATA_DOWNLOAD_ROOT = "https://www.football-data.co.uk/mmz4281/"
GAME_SAVE_PATH_ROOT = "data/game_data/"

competition_name_conversion = {
    "E0": "English Premier League",
    "E1" : "EFL Championship"
}

def download_all_game_data():
    """
    Downloads match facts for every game for the specified season data as a single csv

    Arguments:
        season (str): last 2 digits of each year the season encompasses, e.g. "16/17"
    """
    for season in MATCH_SITE_SEASONS:
        time.sleep(0.2)
        for league in MATCH_LEAGUES:
            try:
                # MATCH_SITE_SEASONS
                save_path = os.path.join(GAME_SAVE_PATH_ROOT, f"{league} - {season}.csv")
                url = os.path.join(GAME_DATA_DOWNLOAD_ROOT, season, f'{league}.csv')
                match_data = pd.read_csv(url)
                match_data.to_csv(save_path)
                logger.info(f'Game csv file for league {league} in {season} downloaded and saved to {save_path}')
                return True
            except Exception as e:
                logger.error(f'An error occurred while downloading games for league {league} in {season}:', str(e))
                return False

def rename_table_columns(df: pd.DataFrame, season: str) -> pd.DataFrame:
    """
    Renames the columns of a DataFrame according to a predefined mapping and adds season and competition_id columns.

    Args:
        df (pd.DataFrame): The DataFrame to be modified.
        season (str): The season value to be added to the DataFrame.
        competition_id (str): The competition ID value to be added to the DataFrame.

    Returns:
        pd.DataFrame: The modified DataFrame with renamed columns and added season and competition_id columns.
    """
    try:
        column_mapping = {
            "Div": "competition_id",
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
            "Referee": "referee_id",
            "Date": "date",
            "PSH": "home_odds",
            "PSD": "draw_odds",
            "PSA": "away_odds",
            "PSCH": "closing_home_odds",
            "PSCD": "closing_draw_odds",
            "PSCA": "closing_away_odds",
        }

        df = df.rename(columns=column_mapping)
        return df
    except Exception as e:
        logger.error(f"Error: {e}")
        return df

def select_match_columns(df: pd.DataFrame, db_connection) -> pd.DataFrame:
    """
    Selects specific columns from the input DataFrame and performs data transformations.

    Args:
        df (pd.DataFrame): The input DataFrame containing match data.
        db_connection: The database connection object.

    Returns:
        pd.DataFrame: The transformed DataFrame with selected columns.
    """
    try:
        new_df = df[[
            "season",
            "date",
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
            "home_odds",
            "draw_odds",
            "away_odds",
            "closing_home_odds",
            "closing_draw_odds",
            "closing_away_odds",
        ]].copy()
        
        # Convert team names to IDs
        print(new_df["home_team_id"].unique())
        print(new_df["away_team_id"].unique())
        new_df["home_team_id"] = new_df["home_team_id"].apply(lambda x: get_id_from_name(db_connection, x, "team"))
        new_df["away_team_id"] = new_df["away_team_id"].apply(lambda x: get_id_from_name(db_connection, x, "team"))

        # Convert referee names to IDs
        new_df["referee_id"] = new_df["referee_id"].apply(lambda x: get_id_from_name(db_connection, x, "referee"))

        # Remove duplicate rows based on specific columns
        columns_to_compare = ["season", "competition_id", "home_team_id", "away_team_id"]
        final_df = remove_duplicate_rows(db_connection, new_df, columns_to_compare, "match")

        return final_df
    except Exception as e:
        logger.error(f"Error selecting match columns at line {e.__traceback__.tb_lineno}: {e}")
        return df

def create_referee_table(df: pd.DataFrame, db_connection) -> pd.DataFrame:
    """
    Creates a referee table from the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the referee data.
        db_connection: The database connection object.

    Returns:
        pd.DataFrame: The DataFrame containing the referee names.
    """
    try:
        referee_df = df.drop_duplicates(subset="referee_id")[["referee_id"]]
        referee_df = referee_df.rename(columns={"referee_id": "name"})
        return referee_df
    except Exception as e:
        logger.error(f"Error: {e}")
        return df

def clean_ref_match_data(db_connection, table_name:str, season:str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the match data by renaming table columns, dropping unnecessary columns, 
    renaming team names, and escaping single quotes in the referee_id column.
    
    Parameters:
        db_connection (connection): The database connection object.
        table_name (str): The name of the table to be created.
        season (str): The season of the match data.
        df (pd.DataFrame): The input DataFrame containing the match data.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    try:
        df = rename_table_columns(df, season)

        df["season"] = season
        df["competition_id"] = get_id_from_name(db_connection, competition_name_conversion[df["competition_id"]], "competition")

        df = df.drop(columns=["B365H","B365D","B365A","BWH","BWD","BWA","IWH","IWD","IWA","PSH","PSD","PSA","WHH","WHD","WHA","VCH","VCD","VCA","Bb1X2","BbMxH","BbAvH","BbMxD","BbAvD","BbMxA","BbAvA","BbOU","BbMx>2.5","BbAv>2.5","BbMx<2.5","BbAv<2.5","BbAH","BbAHh","BbMxAHH","BbAvAHH","BbMxAHA","BbAvAHA","PSCH","PSCD","PSCA"], errors="ignore")

        # unique_teams = pd.Series(pd.concat([df["home_team_id"], df["away_team_id"]]).unique())
        # team_replacements = unique_teams.apply(lambda team: get_name_from_database(db_connection, team, "team"))
        # team_replacement_dict = dict(zip(unique_teams, team_replacements))
        # df[["home_team_id", "away_team_id"]] = df[["home_team_id", "away_team_id"]].replace(team_replacement_dict)

        df["referee_id"] = df["referee_id"].apply(escape_single_quote)

        if table_name == "referee":
            df = create_referee_table(df, db_connection)
        if table_name == "match":
            df = select_match_columns(df, db_connection)
            
        return df
    except Exception as e:
        logger.error(f"Error: {e}")
        return df

def save_to_database(db_connection, table_name, df: pd.DataFrame) -> None:
    """
    Save a DataFrame to a database table.

    Args:
        db_connection: The database connection object.
        table_name: The name of the table to save the DataFrame to.
        df: The DataFrame to be saved.

    Returns:
        None
    """
    try:
        if table_name == "match":
            df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
            df = df.sort_values(by=["date"]).reset_index(drop=True)
        with db_connection.connect() as conn:
            df.to_sql(table_name, conn, if_exists="append", index=False) if not df.empty else None
    except Exception as e:
        raise Exception(e)


def ref_match_main(db_connection):
    """
    Main function for processing team, referee, and match data intake.

    Args:
        db_connection (object): Database connection object.

    Returns:
        None
    """
    data_folder_path = "./data/game_data"

    data = sorted(os.listdir(data_folder_path))
    try:
        for year in data:
            season = re.findall("\d{4}", year)[0]
            season = season[:2]+"-"+season[-2:]
            full_season = TABLE_SEASONS[data.index(year)]
            
            path = data_folder_path+"/"+year
            order = ["referee", "match"]
            comparison_columns = [["name"], ["season","home_team_id","away_team_id"]]

            for idx, table in enumerate(order):
                df = pd.read_csv(path)
                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
                df = clean_ref_match_data(db_connection, table, full_season, df)
                deduplicated_df = remove_duplicate_rows(db_connection, df, comparison_columns[idx], table)
                
                if not deduplicated_df.empty:
                    save_to_database(db_connection, table, deduplicated_df)
                    logger.info(f"Inserted into {table} table for {season}.")
    except Exception as e:
        logger.error(f"Error in ref_match_main in {e.__context__} on line {str(e.__traceback__.tb_lineno)}: {e.__cause__} - {e}")
        return f"Error in ref_match_main in {e.__context__} on line {str(e.__traceback__.tb_lineno)}: {e.__cause__} - {e}"

# TODO - Add logging for more visibility of data_intake process
