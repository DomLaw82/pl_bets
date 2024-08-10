import pandas as pd
import numpy as np
from db_connection import SQLConnection
import datetime, sys, os
from dotenv import load_dotenv
from app_logger import FluentLogger

load_dotenv()
logger = FluentLogger("predict-dataset_creation").get_logger()

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
    "goals","assists","penalties_scored","penalties_attempted","yellow_cards","red_cards","expected_goals",
    "non_penalty_expected_goals","expected_assisted_goals","progressive_carries","progressive_passes","total_passing_distance",
    "total_progressive_passing_distance","short_passes_completed","short_passes_attempted","medium_passes_completed",
    "medium_passes_attempted","long_passes_completed","long_passes_attempted","expected_assists","key_passes",
    "passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","shots","shots_on_target",
    "average_shot_distance","shots_from_free_kicks","touches_in_defensive_penalty_area","touches_in_defensive_third",
    "touches_in_middle_third","touches_in_attacking_third","touches_in_attacking_penalty_area","live_ball_touches",
    "take_ons_attempted","take_ons_succeeded","carries","total_carrying_distance","progressive_carrying_distance",
    "carries_into_final_third","carries_into_penalty_area","miscontrols","dispossessed","passes_received",
    "progressive_passes_received","tackles_won","defensive_third_tackles","middle_third_tackles","attacking_third_tackles",
    "dribblers_tackled","dribbler_tackles_attempted","shots_blocked","passes_blocked","interceptions","clearances",
    "errors_leading_to_shot","goals_against","shots_on_target_against","saves","clean_sheets","penalties_faced",
    "penalties_allowed","penalties_saved","penalties_missed"
]
player_stats_columns = ["player_id", "minutes_played","ninetys"] + stats_columns
pure_stats_columns = ["minutes_played"] + stats_columns
team_stats_columns = ["team_id"] + stats_columns

def get_all_match_data(sql_connection) -> pd.DataFrame:
    """
    Retrieves all the matches from the database.

    Returns:
        pd.DataFrame: The DataFrame containing all the matches.
    """
    try:
        return sql_connection.get_df("""
            SELECT
                m.id AS match_id,
                m.season,
                m.competition_id,
                m.referee_id, 
                m.home_team_id, m.away_team_id,
                m.home_goals, m.away_goals,
                m.home_shots, m.away_shots,
                m.home_shots_on_target, m.away_shots_on_target,
                m.home_corners, m.away_corners,
                m.home_fouls, m.away_fouls, 
                m.home_yellow_cards, m.away_yellow_cards,
                m.home_red_cards, m.away_red_cards
            FROM
                match m
        """)
    except Exception as e:
        raise e

def get_player_stats(sql_connection, game_season: str, home_team_id: str, away_team_id: str, less_than_or_equal_to:str) -> pd.DataFrame:
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
    try:
        df = sql_connection.get_df(f"""
            WITH player_team_filtered AS (
                SELECT
                    player_id,
                    team_id
                FROM
                    player_team
                WHERE
                    season = '{game_season}'
                    AND team_id IN ('{home_team_id}', '{away_team_id}')
            )

            SELECT 
                hpn.*,
                ptf.team_id AS current_team_id
            FROM 
                historic_player_per_ninety hpn
            JOIN
                player_team_filtered ptf
            ON
                hpn.player_id = ptf.player_id
            WHERE 
                hpn.season {less_than_or_equal_to} '{game_season}';
        """)
        df["team_id"] = df["current_team_id"]
        df = df.drop(columns=["current_team_id"])
        return df
    except Exception as e:
        raise e

def group_stats_by_player(df: pd.DataFrame) -> pd.DataFrame:
    """
    Groups the statistics of players by their player_id for the specified home and away teams.

    Args:
        df (pd.DataFrame): The input DataFrame containing player statistics.

    Returns:
        pd.DataFrame: The DataFrame with player statistics grouped by player_id.
    """
    try:
        # EDGE CASE: A player has played for both the teams playing against each other in the same season, this player's stats
        #               will be used for both teams, when we only want them considered for the final team
        # TODO: Get current team squad and compare the players in the squad with the players in the player stats DataFrame

        df = (
            df[player_stats_columns+["season", "team_id"]]
            .groupby(["player_id", "season", "team_id"])
            .sum()
            .reset_index()
            [player_stats_columns + ["team_id"]]
            .groupby(["player_id", "team_id"]) # Team id should be the same for all entries for each player, so grouping by team_id should return a single row for each player
            .mean()
            .reset_index()
        )
        # This returns the per-season output for each player, which is then averaged across all seasons
        # Team context is not currently considered
        # TODO: Consider teams performance/play-style with features to improve prediction accuracy
        # e.g. team possession, territory, shots on target, goals scored, etc.

        return df
    except Exception as e:
        raise e

def create_per_90_stats(df: pd.DataFrame, columns_to_evaluate: list = None) -> pd.DataFrame:
    """
    Create per 90 minutes statistics for the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the statistics.
        columns_to_evaluate (list, optional): The list of columns to evaluate. Defaults to None.

    Returns:
        pd.DataFrame: The DataFrame with per 90 minutes statistics.
    """
    try:
        ninety_mins_per_season = 38

        # Use vectorized operations to update pure_stats_columns
        df[columns_to_evaluate] /= ninety_mins_per_season

        return df
    except Exception as e:
        raise e

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
    try:
        minutes_per_game = 90
        
        # Use vectorized operations to update pure_stats_columns
        df[columns_to_evaluate] = df[columns_to_evaluate].multiply(df["minutes_played"] / minutes_per_game, axis=0)

        # Drop the "minutes_played" column
        df = df.drop(columns=["minutes_played"])

        return df
    except Exception as e:
        raise e

def group_stats_by_team(df: pd.DataFrame, columns_to_evaluate: list = None) -> pd.DataFrame:
    """
    Groups the player statistics in the DataFrame by team and returns a new DataFrame with team statistics.

    Args:
        df (pd.DataFrame): The input DataFrame containing player statistics.
        columns_to_evaluate (list, optional): The list of columns to evaluate. Defaults to None.

    Returns:
        pd.DataFrame: The new DataFrame with team statistics.

    """
    try:
        df = df.drop(columns=["player_id"])
        df[columns_to_evaluate] = df[columns_to_evaluate].groupby("team_id").sum().reset_index()
        return df[df.index < df["team_id"].nunique()]
    except Exception as e:
        raise e

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
    try:
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
    except Exception as e:
        raise e

def combine_form_and_career_stats(dfs: tuple, columns_to_evaluate: list = None) -> pd.DataFrame:
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
    try:
        career_df = dfs[0]
        form_df = dfs[1]

        career_stats_ratio = float(os.environ.get("CAREER_STATS_RATIO"))
        form_stats_ratio = 1 - career_stats_ratio

        career_df[columns_to_evaluate] = career_df[columns_to_evaluate] * career_stats_ratio
        form_df[columns_to_evaluate] = form_df[columns_to_evaluate] * form_stats_ratio

        all_stats = pd.concat([career_df, form_df])

        # Combined stats for all the players on both teams
        all_stats = all_stats[["match_id"] + columns_to_evaluate]
        all_stats = all_stats.groupby("match_id").sum().reset_index()

        if "team_id" in all_stats.columns and "ninetys" in all_stats.columns:
            all_stats.drop(columns=["ninetys", "team_id"], inplace=True)
        
        return all_stats

    except Exception as e:
        raise e


def get_current_season() -> str:
    """
    Get the current season based on the current date.

    Returns:
        str: The current season.
    """
    try:
        current_date = datetime.datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        if current_month < 8:
            current_year -= 1

        return f"{current_year}-{current_year + 1}"
    except Exception as e:
        raise e

def grouping_prediction_dataframe_rows(df: pd.DataFrame, home_team_id: str, away_team_id:str) -> pd.DataFrame:

    try:
        columns_to_remove = ["_plus_", "_minus", "_divided_by_", "_per_"]
        columns = [col for col in df.columns if any(word in col for word in columns_to_remove)]
        df = df.drop(columns=columns)

        df = group_stats_by_player(df)

        if df["team_id"].nunique() < 2:
            print("Not enough players in each team available for prediction")
            return pd.DataFrame()

        df = create_per_90_stats(df, pure_stats_columns)
        df = create_contribution_per_90_stats(df, pure_stats_columns)
        df = group_stats_by_team(df, team_stats_columns)
        df = convert_team_rows_to_single_row(df, home_team_id, away_team_id, pure_stats_columns)

        return df
    except Exception as e:
        raise e

def create_training_dataset(sql_connection) -> pd.DataFrame:
    """
    Create a dataset for match predictions.

    Returns:
        pd.DataFrame: The combined dataset containing player stats and match facts.
    """
    try:
        all_matches = get_all_match_data(sql_connection)
        complete_player_career_stats_for_match_df = pd.DataFrame()
        complete_player_form_stats_for_match_df = pd.DataFrame()

        all_seasons = all_matches["season"].unique()
        all_seasons.sort()

        for match in all_matches.values:
            home_team_id = match[4]
            away_team_id = match[5]
            season = match[1]
            match_id = match[0]
            
            if season == all_seasons[0]:
                continue

            career = get_player_stats(sql_connection, season, home_team_id, away_team_id, "<")
            form = get_player_stats(sql_connection, season, home_team_id, away_team_id, "=")

            career = grouping_prediction_dataframe_rows(career, home_team_id, away_team_id)
            form = grouping_prediction_dataframe_rows(form, home_team_id, away_team_id)

            career["match_id"] = match_id
            form["match_id"] = match_id

            complete_player_career_stats_for_match_df = pd.concat([complete_player_career_stats_for_match_df, career])
            complete_player_form_stats_for_match_df = pd.concat([complete_player_form_stats_for_match_df, form])

        df = combine_form_and_career_stats((complete_player_career_stats_for_match_df, complete_player_form_stats_for_match_df), columns_to_evaluate=stats_columns)
        df = pd.merge(df, all_matches, on="match_id")

        logger.info(f"Dataset created successfully - {df.shape[0]} rows and {df.shape[1]} columns.")
        print(f"Dataset created successfully - {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except Exception as e:
        raise e
    
def create_prediction_dataset(sql_connection, home_team_id: str, away_team_id: str) -> pd.DataFrame:
    try:

        season = get_current_season()

        career = get_player_stats(sql_connection, season, home_team_id, away_team_id, "<")
        form = get_player_stats(sql_connection, season, home_team_id, away_team_id, "=")
        career = grouping_prediction_dataframe_rows(career, home_team_id, away_team_id)
        form = grouping_prediction_dataframe_rows(form, home_team_id, away_team_id)
        
        if career.empty or form.empty:
            raise ValueError(f"Not enough players in each team for season {season} available for prediction; Career dataframe players: {career.shape[0]}, Form dataframe players: {form.shape[0]}")

        career["match_id"] = "match_id"
        form["match_id"] = "match_id"

        df = combine_form_and_career_stats((career, form), columns_to_evaluate=stats_columns)

        logger.info(f"Career player stats combined successfully for prediction: \n{career}.")
        logger.info(f"Form player stats combined successfully for prediction: \n{form}.")

        df = df.drop(columns=["match_id"])
        logger.info(f"Prediction dataset created successfully - {df.shape[0]} rows and {df.shape[1]} columns.")

        return df
    except Exception as e:
        raise e