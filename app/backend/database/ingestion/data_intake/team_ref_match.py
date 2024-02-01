import os, re
import pandas as pd
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
from data_intake.utilities.unique_id import *
from data_intake.utilities.string_manipulation import escape_single_quote

SITE_SEASONS = [f"{str(year-1)[-2:]}{str(year)[-2:]}" for year in range(2018, 2025, 1)]
TABLE_SEASONS = [f"{str(year-1)}-{str(year)}" for year in range(2018, 2025, 1)]

def rename_team_name(team_name: str) -> str:
    """
    Renames a team name based on a predefined mapping.

    Args:
        team_name (str): The name of the team to be renamed.

    Returns:
        str: The renamed team name, if it exists in the mapping. Otherwise, returns the original team name.
    """
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
        "Huddersfield": "Huddersfield Town",
        "Norwich": "Norwich City",
    }
    return rename_teams.get(team_name, team_name)

def rename_table_columns(df: pd.DataFrame, season: str, competition_id: str) -> pd.DataFrame:
    """
    Renames the columns of a DataFrame according to a predefined mapping and adds season and competition_id columns.

    Args:
        df (pd.DataFrame): The DataFrame to be modified.
        season (str): The season value to be added to the DataFrame.
        competition_id (str): The competition ID value to be added to the DataFrame.

    Returns:
        pd.DataFrame: The modified DataFrame with renamed columns and added season and competition_id columns.
    """
    column_mapping = {
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
    }

    df = df.rename(columns=column_mapping)
    df["season"] = season
    df["competition_id"] = competition_id

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
    # Select specific columns
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
    ].copy()

    # Get team IDs using vectorized operations
    new_df["home_team_id"] = new_df["home_team_id"].apply(lambda x: get_team_id(db_connection, x))
    new_df["away_team_id"] = new_df["away_team_id"].apply(lambda x: get_team_id(db_connection, x))

    # Get referee IDs using vectorized operations
    new_df["referee_id"] = new_df["referee_id"].apply(lambda x: get_referee_id(db_connection, x))

    # Remove duplicate rows based on specific columns
    columns_to_compare = ["season", "competition_id", "home_team_id", "away_team_id"]
    final_df = remove_duplicate_rows(db_connection, new_df, columns_to_compare, "match")
    return final_df

def create_teams_table(df: pd.DataFrame, db_connection) -> pd.DataFrame:
    """
    Creates a teams table in the database based on the provided DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the team data.
        db_connection: The connection to the database.

    Returns:
        pd.DataFrame: The DataFrame containing only the names of the newly created teams.
    """
    df = df.rename(columns={"home_team_id": "name"})
    only_new_teams_df = df.drop_duplicates(subset="name", keep="first")
    only_new_teams_df = remove_duplicate_rows(db_connection, only_new_teams_df, ["name"], "team").reset_index()
    return only_new_teams_df[["name"]]

def create_referee_table(df: pd.DataFrame, db_connection) -> pd.DataFrame:
    """
    Creates a referee table from the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the referee data.
        db_connection: The database connection object.

    Returns:
        pd.DataFrame: The DataFrame containing the referee names.
    """
    referee_df = df.drop_duplicates(subset="referee_id")[["referee_id"]]
    referee_df = referee_df.rename(columns={"referee_id": "name"})
    return referee_df

def clean_match_data(db_connection, table_name:str, season:str, df: pd.DataFrame) -> pd.DataFrame:
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
    df = rename_table_columns(df, season, '001')

    df = df.drop(columns=["B365H","B365D","B365A","BWH","BWD","BWA","IWH","IWD","IWA","PSH","PSD","PSA","WHH","WHD","WHA","VCH","VCD","VCA","Bb1X2","BbMxH","BbAvH","BbMxD","BbAvD","BbMxA","BbAvA","BbOU","BbMx>2.5","BbAv>2.5","BbMx<2.5","BbAv<2.5","BbAH","BbAHh","BbMxAHH","BbAvAHH","BbMxAHA","BbAvAHA","PSCH","PSCD","PSCA"], errors="ignore")

    df["home_team_id"] = df["home_team_id"].apply(rename_team_name)
    df["away_team_id"] = df["away_team_id"].apply(rename_team_name)
    df["referee_id"] = df["referee_id"].apply(escape_single_quote)

    if table_name == "team":
        df = create_teams_table(df, db_connection)
    if table_name == "referee":
        df = create_referee_table(df, db_connection)
    if table_name == "match":
        df = select_match_columns(df, db_connection)
        
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
    df.to_sql(table_name, db_connection.conn, if_exists="append", index=False) if not df.empty else None


def team_ref_match_main(db_connection):
    """
    Main function for processing team, referee, and match data intake.

    Args:
        db_connection (object): Database connection object.

    Returns:
        None
    """
    data_folder_path = "./data/game_data"

    data = sorted(os.listdir(data_folder_path))

    for year in data:
        season = re.findall("\d{4}", year)[0]
        season = season[:2]+"-"+season[-2:]
        full_season = TABLE_SEASONS[data.index(year)]
        
        path = data_folder_path+"/"+year
        order = ["team", "referee", "match"]
        comparison_columns = [["name"], ["name"], ["season","home_team_id","away_team_id"]]

        for idx, table in enumerate(order):
            df = pd.read_csv(path)
            df = clean_match_data(db_connection, table, full_season, df)
            deduplicated_df = remove_duplicate_rows(db_connection, df, comparison_columns[idx], table)
            
            if not deduplicated_df.empty:
                save_to_database(db_connection, table, deduplicated_df)
                print(f"Inserted into {table} table for {season}.")
        print("\n")
    print("\n")

# TODO - Add logging for more visibility of data_intake process