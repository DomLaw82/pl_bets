import pandas as pd
import numpy as np
from db_connection import SQLConnection
from app_logger import FluentLogger
from date_functions import get_current_season, get_current_date
from elo_ratings import get_team_elo_rating
from define_environment import load_correct_environment_variables

load_correct_environment_variables()
logger = FluentLogger("predict-dataset_creation").get_logger()

stats_columns = [
    "goals",
    "assists",
    "pens_made",
    "pens_att",
    "shots",
    "shots_on_target",
    "cards_yellow",
    "cards_red",
    "blocks",
    "xg",
    "npxg",
    "passes_total_distance",
    "passes_progressive_distance",
    "passes_completed_short",
    "passes_short",
    "passes_completed_medium",
    "passes_medium",
    "passes_completed_long",
    "passes_long",
    "xg_assist",
    "pass_xa",
    "assisted_shots",
    "passes_into_final_third",
    "passes_into_penalty_area",
    "crosses_into_penalty_area",
    "progressive_passes",
    "tackles",
    "tackles_won",
    "tackles_def_3rd",
    "tackles_mid_3rd",
    "tackles_att_3rd",
    "challenge_tackles",
    "challenges",
    "blocked_shots",
    "blocked_passes",
    "interceptions",
    "clearances",
    "errors",
    "touches",
    "touches_def_pen_area",
    "touches_def_3rd",
    "touches_mid_3rd",
    "touches_att_3rd",
    "touches_att_pen_area",
    "touches_live_ball",
    "take_ons",
    "take_ons_won",
    "take_ons_tackled",
    "carries",
    "carries_distance",
    "carries_progressive_distance",
    "progressive_carries",
    "carries_into_final_third",
    "carries_into_penalty_area",
    "miscontrols",
    "dispossessed",
    "passes_received",
    "progressive_passes_received",
    "sca",
    "sca_passes_live",
    "sca_passes_dead",
    "sca_take_ons",
    "sca_shots",
    "sca_fouled",
    "sca_defense",
    "gca",
    "gca_passes_live",
    "gca_passes_dead",
    "gca_take_ons",
    "gca_shots",
    "gca_fouled",
    "gca_defense",
    "gk_shots_on_target_against",
    "gk_goals_against",
    "gk_saves",
    "gk_clean_sheets",
    "gk_psxg",
    "gk_pens_att",
    "gk_pens_allowed",
    "gk_pens_saved",
    "gk_pens_missed",
    "gk_passed_completed_launched",
    "gk_passes_launched",
    "gk_passes",
    "gk_passes_throws",
    "gk_passes_length_avg",
    "gk_goal_kicks",
    "gk_goal_kicks_length_avg",
]
player_stats_columns = ["player_id", "minutes"] + stats_columns
pure_stats_columns = ["minutes"] + stats_columns
team_stats_columns = ["team_id"] + stats_columns

def get_all_match_data(sql_connection: SQLConnection, **kwargs) -> pd.DataFrame:
    """
    Retrieves all the matches from the database.
    """
    start_date = str(kwargs.get("start_date", None))
    query = f"""
        SELECT
            m.id AS match_id,
            m.date,
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
        {"WHERE m.date >= '" + start_date + "'" if start_date != 'None'  else ''}
    """
    return sql_connection.get_df(query)

def get_player_stats_for_game(sql_connection: SQLConnection, game_season: str, date: str, home_team_id: str, away_team_id: str, head_to_head: bool = False) -> pd.DataFrame:
    """
    Retrieves player statistics up to a certain date for specified teams.
    """
    head_to_head_condition = f""" AND ml.team_id IN ('{home_team_id}', '{away_team_id}')
        AND ml.opponent_id IN ('{home_team_id}', '{away_team_id}')""" if head_to_head else ""
    query = f"""
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
            ml.*,
            ptf.team_id AS current_team_id
        FROM 
            match_logs ml
        JOIN
            player_team_filtered ptf
        ON
            ml.player_id = ptf.player_id
        WHERE 
            ml.date < '{date}'{head_to_head_condition};
    """
    df = sql_connection.get_df(query)
    df["team_id"] = df["current_team_id"]
    df = df.drop(columns=["current_team_id"])
    return df

def group_stats_by_player(df: pd.DataFrame, player_id: str, is_home:bool) -> pd.DataFrame:
    """
    Groups the statistics of players by their player_id.


    Args:
        df (pd.DataFrame): The input DataFrame containing player statistics.

    Returns:
        pd.DataFrame: The DataFrame with player statistics grouped by player_id.
    """
    try:
        to_remove = [
            "fbref_id",
            "competition_id",
            "match_id",
            "season",
            "date",
            "opponent_id",
            "position",
            "started",
        ]
        df = df.drop(columns=to_remove)
        player_df = df[df["player_id"] == player_id]
        player_at_loc_df = player_df[player_df["location"].str.lower() == "home"] if is_home else player_df[player_df["location"].str.lower() == "away"]
        player_form_df = player_df.tail(5)
        player_form_at_loc_df = player_at_loc_df.tail(5)

        dataframes = [player_df, player_at_loc_df, player_form_df, player_form_at_loc_df]
        transformed_dataframes = []

        team_id = player_df["team_id"].unique()[0]
        for dataframe in dataframes:
            dataframe = dataframe.drop(columns=["location", "player_id", "team_id"])
            total_games = dataframe.shape[0]
            total_minutes = dataframe["minutes"].sum()
            minutes_per_game = total_minutes / total_games if total_games > 0 and total_minutes > 0 else 0
            summed_df = dataframe.sum()
            dataframe = create_player_stat_per_minute(summed_df, stats_columns)
            dataframe = dataframe.to_frame().T
            dataframe["minutes_per_game"] = minutes_per_game
            dataframe = dataframe.drop(columns=["minutes"])
            transformed_dataframes.append(dataframe)

        # Declare a ratio for the combination of the 4 dataframes
        ratios = [0.15, 0.15, 0.35, 0.35]
        df = pd.concat([df * ratio for df, ratio in zip(transformed_dataframes, ratios)], axis=0).sum(axis=0).to_frame().T
        # Add player_id and team_id back to the dataframe
        df["player_id"] = player_id
        df["team_id"] = team_id
        # TODO: Consider teams performance/play-style with features to improve prediction accuracy
        # e.g. team possession, territory, shots on target, goals scored, etc.

        return df
    except Exception as e:
        raise Exception(e)

def create_player_stat_per_minute(df: pd.DataFrame, columns_to_evaluate: list = None) -> pd.Series:
    try:
        # Avoid division by zero
        if df["minutes"] == 0:
            df[columns_to_evaluate] = 0
        else:
            df[columns_to_evaluate] /= df["minutes"]
        return df
    except Exception as e:
        raise Exception(e)
    
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
        # Use vectorized operations to update pure_stats_columns
        df[columns_to_evaluate] = df[columns_to_evaluate].multiply(df["minutes_per_game"], axis=0)

        # Drop the "minutes_played" column
        df = df.drop(columns=["minutes_per_game"])

        return df
    except Exception as e:
        raise Exception(e)

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
        df = df[columns_to_evaluate].groupby("team_id").sum().reset_index()
        return df
    except Exception as e:
        raise Exception(e)

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
        final_df.drop(columns=["team_id"], inplace=True)

        return final_df
    except Exception as e:
        raise Exception(e)

def grouping_prediction_dataframe_rows(df: pd.DataFrame, home_team_id: str, away_team_id:str) -> pd.DataFrame:

    try:
        players = df["player_id"].unique()

        if len(players) == 0:
            return pd.DataFrame()
        
        combined_df = pd.DataFrame()
        for player in players:
            team = df[df["player_id"] == player]["team_id"].values[0]
            is_home = team == home_team_id
            player_df = group_stats_by_player(df, player, is_home)
            combined_df = pd.concat([combined_df, player_df])

        if combined_df["team_id"].nunique() < 2:
            print("Not enough players in each team available for prediction")
            return pd.DataFrame()

        # df = create_player_stat_per_minute(df, pure_stats_columns)
        df = create_contribution_per_90_stats(combined_df, stats_columns)

        # Dataframe with one row per team
        df = group_stats_by_team(df, team_stats_columns)
        # Dataframe with one row representing the stats difference between the two teams
        df = convert_team_rows_to_single_row(df, home_team_id, away_team_id, stats_columns)
        return df
    except Exception as e:
        print(e)
        raise Exception(e)

def create_training_dataset(sql_connection) -> pd.DataFrame:
    """
    Creates a training dataset for match predictions.
    """
    try:
        final_combined_df = pd.read_csv("./files/final_combined_dataframe.csv", encoding="utf-8", index_col=False)
        latest_date = final_combined_df["date"].max() or 'None'
        all_matches = get_all_match_data(sql_connection, start_date=latest_date)
        complete_stats_df = pd.DataFrame()

        for match in all_matches.itertuples(index=False):
            match_id = match.match_id
            date = match.date
            season = match.season
            home_team_id = match.home_team_id
            away_team_id = match.away_team_id

            # Get player stats
            career_stats = get_player_stats_for_game(sql_connection, season, date, home_team_id, away_team_id)
            career_stats = grouping_prediction_dataframe_rows(career_stats, home_team_id, away_team_id)

            if career_stats.empty:
                logger.info(f"Insufficient data for match {match_id}")
                continue

            career_stats["match_id"] = match_id

            complete_stats_df = pd.concat([complete_stats_df, career_stats], ignore_index=True)
        
        # Merge with match outcomes
        dataset = pd.merge(complete_stats_df, all_matches, on="match_id")

        final_dataset = pd.concat([final_combined_df, dataset], ignore_index=True)
        final_dataset[stats_columns] = final_dataset[stats_columns].astype(float).round(10)
        final_dataset = final_dataset.drop_duplicates(subset=["match_id"])
        final_dataset = final_dataset.sort_values(by=["date", "match_id"], ascending=[True, True])

        logger.info(f"Training dataset created with {len(dataset)} records.")
        return final_dataset
    except Exception as e:
        logger.error(f"Error creating training dataset: {e}")
        raise e

def create_prediction_dataset(sql_connection, home_team_id: str, away_team_id: str) -> pd.DataFrame:
    """
    Creates a dataset for predicting a specific match.
    """
    try:
        season = get_current_season()
        date = get_current_date()
        print(f"Creating prediction dataset for {home_team_id} vs {away_team_id} on {date}...")

        career_stats = get_player_stats_for_game(sql_connection, season, date, home_team_id, away_team_id)
        career_stats = grouping_prediction_dataframe_rows(career_stats, home_team_id, away_team_id)

        if career_stats.empty:
            raise ValueError(f"Not enough players in each team for season {season} available for prediction.")

        logger.info(f"Prediction dataset created successfully for {home_team_id} vs {away_team_id}.")
        return career_stats
    except Exception as e:
        logger.error(f"Error creating prediction dataset: line {e.__traceback__.tb_lineno} : {e}")
        raise e
    