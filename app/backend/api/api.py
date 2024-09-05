from flask import Flask, request, jsonify
from flask_rebar import Rebar
from flask_cors import CORS
import pandas as pd
from db_connection import SQLConnection
from app_logger import FluentLogger
from datetime import datetime
import os, datetime
import numpy as np

db = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))
logger = FluentLogger("api").get_logger()


rebar = Rebar()
registry = rebar.create_handler_registry()

### Helper functions ###
def get_top_n_all_time(df:pd.DataFrame, n:int, stat:str) -> list:
   try:
      df = df[["full_name", f"{stat}"]].sort_values(by=stat, ascending=False)
      values = df.head(n).to_dict(orient='records')
      logger.info(f"Top {n} all-time {stat} retrieved")
      return values
   except Exception as e:
      logger.error(f"Error creating top {n} {stat} dataframe: {str(e)}")
      raise Exception(f"Error creating top {n} {stat} dataframe: {str(e)}")

def decompose_season(season: str) -> tuple:
   start_year, end_year = season.split('-')
   start_month = '08'
   end_month = '05'
   
   start_date = datetime.datetime.strptime(f"{start_year}-{start_month}-01", "%Y-%m-%d")
   end_date = datetime.datetime.strptime(f"{end_year}-{end_month}-31", "%Y-%m-%d")
   
   return (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

### Routes ###
# /health
@registry.handles(
   rule='/health',
   method='GET',
)
def health():
   try:
      # logger.debug("Health check")
      return jsonify({"status": "healthy"})
   except Exception as e:
      print(e)
      logger.error(f"Error with endpoint /health: {str(e)}")
      raise

# /
@registry.handles(
   rule='/',
   method='GET',
)
def index():
   #  logger.info("Index page")
    return jsonify({"title": "Welcome to PL Bets"})

# /teams
@registry.handles(
   rule='/teams',
   method='GET',
)
def get_teams():
   try:
      is_active = request.args.get('active')
      all_teams = "SELECT * from team ORDER BY name ASC"
      active_teams = """
         WITH current_season AS (
            SELECT 
               MAX(season) AS season
            FROM
               player_team
         )
         SELECT
            DISTINCT(team.id) AS id,
            name
         FROM
            team
         JOIN current_season ON TRUE
         JOIN player_team ON team.id = player_team.team_id 
            AND player_team.season = current_season.season
         ORDER BY name ASC
      """
      teams = db.get_dict(all_teams) if is_active != 'true' else db.get_dict(active_teams)
      logger.info(f"{'Active t' if is_active else 'T'}eams retrieved")
      return jsonify(teams)
   except Exception as e:
      logger.error(f"Error with endpoint /teams{'?active=true' if is_active else ''}: {str(e)}")
      raise

@registry.handles(
   rule="/prediction/team-id",
   method="GET",
)
def get_team_id():
   try:
      team_name = request.args.get('team_name')
      team_id = db.get_dict(f"SELECT id FROM team WHERE name = '{team_name}'")[0]
      logger.info(f"Team id for {team_name} retrieved")
      return jsonify(team_id)
   except Exception as e:
      logger.error(f"Error with endpoint /prediction/team-id: {str(e)}")
      raise

@registry.handles(
   rule='/teams/profile',
   method='GET',
)
def get_team_profile():
   try:
      team_id = request.args.get('team_id')
      team_profile = db.get_dict(f"""
         SELECT 
            season,
            '{team_id}' AS team_id,
            t.name AS team_name,
            COUNT(*) AS matches_played,
            SUM(
               CASE
                  WHEN home_team_id = '{team_id}'
                  AND SPLIT_PART(result, ' - ', 1) > SPLIT_PART(result, ' - ', 2) THEN 3
                  WHEN away_team_id = '{team_id}'
                  AND SPLIT_PART(result, ' - ', 2) > SPLIT_PART(result, ' - ', 1) THEN 3
                  WHEN SPLIT_PART(result, ' - ', 1) = SPLIT_PART(result, ' - ', 2) THEN 1
                  ELSE 0
               END
            ) AS total_points,
            SUM(
               CASE
                  WHEN home_team_id = '{team_id}'
                  AND SPLIT_PART(result, ' - ', 1) > SPLIT_PART(result, ' - ', 2) THEN 1
                  WHEN away_team_id = '{team_id}'
                  AND SPLIT_PART(result, ' - ', 2) > SPLIT_PART(result, ' - ', 1) THEN 1
                  ELSE 0
               END
            ) AS wins,
            SUM(
               CASE
                  WHEN SPLIT_PART(result, ' - ', 1) = SPLIT_PART(result, ' - ', 2) THEN 1
                  ELSE 0
               END
            ) AS draws,
            SUM(
               CASE
                  WHEN home_team_id = '{team_id}'
                  AND SPLIT_PART(result, ' - ', 1) < SPLIT_PART(result, ' - ', 2) THEN 1
                  WHEN away_team_id = '{team_id}'
			         AND SPLIT_PART(result, ' - ', 2) < SPLIT_PART(result, ' - ', 1) THEN 1
                  ELSE 0
               END
            ) AS losses,
            SUM(
               CASE
                  WHEN home_team_id = '{team_id}' THEN CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER)
                  ELSE CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER)
               END
            ) AS goals_for,
            SUM(
               CASE
                  WHEN home_team_id = '{team_id}' THEN CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER)
                  ELSE CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER)
               END
            ) AS goals_against,
            SUM(
               CASE
                  WHEN home_team_id = '{team_id}' THEN CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER) - CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER)
                  ELSE CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER) - CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER)
               END
            ) AS goal_difference
         FROM schedule
            JOIN team t ON t.id = '{team_id}'
         WHERE (
               home_team_id = '{team_id}'
               OR away_team_id = '{team_id}'
            )
            AND result != '-'
         GROUP BY season,
            t.name
         ORDER BY season DESC;
      """)
      logger.info(f"Team profile for {team_id} retrieved")
      return jsonify(team_profile)
   except Exception as e:
      logger.error(f"Error with endpoint /teams/profile?team_id={team_id}: {str(e)}")
      raise

@registry.handles(
   rule='/teams/all-time-stats',
   method='GET',
)
def get_all_time_player_stats():
   tab_columns = {
		"appearances": ["appearances", "minutes"],
		"goals": ["goals", "goals_per_ninety", "expected_goals", "expected_goals_per_ninety"],
		"assists": ["assists", "assists_per_ninety", "expected_assists", "expected_assists_per_ninety"],
		"goalkeeping": ["saves", "clean_sheets"],
		"defending": ["tackles", "interceptions", "clearances"],
		"discipline": ["yellow_cards", "red_cards"],
		"errors": ["errors_leading_to_shot", "dispossessed", "miscontrols"],
	}
   
   try:
      # The player must have played at least 10 games for the team
      team_id = request.args.get('team_id')
      all_time_player_stats = db.get_df(f"""
         WITH player_name AS (
            SELECT
                  DISTINCT CONCAT(player.first_name, ' ', player.last_name) AS full_name,
                  player.id AS player_id
            FROM
               player
            JOIN
                  historic_player_per_ninety ON player.id = historic_player_per_ninety.player_id
            WHERE
               historic_player_per_ninety.team_id = '{team_id}'
               AND matches_played > 10
         ),
         
         sums AS (
            SELECT
               pn.full_name,
               SUM(ninetys) AS ninetys,
               SUM(matches_played) AS appearances,
               SUM(minutes_played) AS minutes,
               SUM(goals) AS goals,
               SUM(assists) AS assists,
               SUM(expected_goals) AS expected_goals,
               SUM(expected_assists) AS expected_assists,
               SUM(yellow_cards) AS yellow_cards,
               SUM(red_cards) AS red_cards,
               SUM(clean_sheets) AS clean_sheets,
               SUM(saves) AS saves,
               SUM(interceptions) AS interceptions,
               SUM(tackles) AS tackles,
               SUM(clearances) AS clearances,
               SUM(errors_leading_to_shot) AS errors_leading_to_shot,
               SUM(miscontrols) AS miscontrols,
               SUM(dispossessed) AS dispossessed
            FROM
               historic_player_per_ninety
            JOIN
               player_name pn ON historic_player_per_ninety.player_id = pn.player_id
            WHERE
               historic_player_per_ninety.team_id = '{team_id}'
               AND ninetys > 0
            GROUP BY
               pn.full_name
         )

         SELECT
            full_name,
            ninetys,
            appearances,
            minutes,
            goals,
            ROUND((goals/ninetys)::numeric, 2) AS goals_per_ninety,
            assists,
            ROUND((assists/ninetys)::numeric, 2) AS assists_per_ninety,
            ROUND(expected_goals::numeric, 2) AS expected_goals,
            ROUND((expected_goals/ninetys)::numeric, 2) AS expected_goals_per_ninety,
            ROUND(expected_assists::numeric, 2) AS expected_assists,
            ROUND((expected_assists/ninetys)::numeric, 2) AS expected_assists_per_ninety,
            yellow_cards,
            red_cards,
            clean_sheets,
            saves,
            interceptions,
            tackles,
            clearances,
            errors_leading_to_shot,
            miscontrols,
            dispossessed
         FROM
            sums;
      """)
      logger.info(f"Team all time stats for {team_id} retrieved")
      top_performers = {}
      for key, columns in tab_columns.items():
         top_performers[key] = {}
         for column in columns:
            top_performers[key][column] = get_top_n_all_time(all_time_player_stats, 5, column)
      logger.info(f"Top performers for all time stats for {team_id} retrieved:\n{top_performers}")
      return jsonify(top_performers)
   except Exception as e:
      logger.error(f"Error with endpoint /teams/all-time-stats?team_id={team_id}: {str(e)}")
      raise

# /players
@registry.handles(
   rule='/players',
   method='GET',
)
def get_players() :
   try:
      is_active = request.args.get('active')
      team_id = request.args.get('team_id')
      all_players_query = """
         WITH current_season AS (
            SELECT 
               MAX(season) AS season
            FROM
               player_team
         )
                            
         SELECT 
            DISTINCT(player.id) AS id,
            player.first_name,
            player.last_name,
            player.birth_year,
            player.position,
            player.nationality,
            team.name AS team_name,
            CASE WHEN pt2.season = current_season.season THEN 'True' ELSE 'False' END AS active
         FROM player
         JOIN current_season ON TRUE
         JOIN (
            SELECT player_id, MAX(season) AS max_season
            FROM player_team
            GROUP BY player_id
         ) AS pt ON player.id = pt.player_id
         JOIN player_team AS pt2 ON pt.player_id = pt2.player_id AND pt.max_season = pt2.season
         JOIN team ON pt2.team_id = team.id
         ORDER BY player.id ASC
      """
      all_active_players_query = f"""
         WITH current_season AS (
            SELECT 
               MAX(season) AS season
            FROM
               player_team
         )
                           
         SELECT
            player.id AS id,
            player.first_name AS first_name,
            player.last_name AS last_name,
            player.birth_year AS birth_year,
            player.position AS position,
            team.name AS team_name
         FROM
            player
         JOIN current_season ON TRUE
         JOIN player_team ON player.id = player_team.player_id
         JOIN team ON player_team.team_id = {team_id if team_id else "team.id"}
         WHERE player_team.season = current_season.season
         ORDER BY player.last_name ASC
      """
      if request.args.get('active') == 'true':
         players = db.get_dict(all_active_players_query)
      else:
         players = db.get_dict(all_players_query)

      logger.info("Players' information retrieved")
      return jsonify(players)
   except Exception as e:
      query_params = []
      if is_active:
         query_params.append('active=true')
      if team_id:
         query_params.append(f'team_id={team_id}')

      query_string = '?' + '&'.join(query_params) if query_params else ''
      logger.error(f"Error with endpoint /players{query_string}: {str(e)}")
      raise

@registry.handles(
   rule='/players/historic-stats',
   method='GET',
)
def get_player_historic_stats_by_season() -> list:
   try:
      player_id = request.args.get('player_id')
      player_historic_stats_by_season = db.get_dict(f"""
         SELECT 
            historic_player_per_ninety.season,
            player.first_name,
            player.last_name,
            team.name AS team,
            minutes_played AS minutes,
            starts,
            matches_played,
            ROUND((goals/ninetys)::numeric, 2) AS goals_per_90,
            ROUND((assists/ninetys)::numeric, 2) AS assists_per_90,
            ROUND((direct_goal_contributions/ninetys)::numeric, 2) AS direct_goal_contributions_per_90,
            ROUND((non_penalty_goals/ninetys)::numeric, 2) AS non_penalty_goals_per_90,
            ROUND((penalties_scored/ninetys)::numeric, 2) AS penalties_scored_per_90,
            ROUND((penalties_attempted/ninetys)::numeric, 2) AS penalties_attempted_per_90,
            ROUND((yellow_cards/ninetys)::numeric, 2) AS yellow_cards_per_90,
            ROUND((red_cards/ninetys)::numeric, 2) AS red_cards_per_90,
            ROUND((expected_goals/ninetys)::numeric, 2) AS expected_goals_per_90,
            ROUND((non_penalty_expected_goals/ninetys)::numeric, 2) AS non_penalty_expected_goals_per_90,
            ROUND((expected_assisted_goals/ninetys)::numeric, 2) AS expected_assisted_goals_per_90,
            ROUND((non_penalty_expected_goals_plus_expected_assisted_goals/ninetys)::numeric, 2) AS non_penalty_expected_goals_plus_expected_assisted_goals_per_90,
            ROUND((progressive_carries/ninetys)::numeric, 2) AS progressive_carries_per_90,
            ROUND((progressive_passes/ninetys)::numeric, 2) AS progressive_passes_per_90,
            ROUND((progressive_passes_received/ninetys)::numeric, 2) AS progressive_passes_received_per_90,
            ROUND((total_passing_distance/ninetys)::numeric, 2) AS total_passing_distance_per_90,
            ROUND((total_progressive_passing_distance/ninetys)::numeric, 2) AS total_progressive_passing_distance_per_90,
            ROUND((short_passes_completed/ninetys)::numeric, 2) AS short_passes_completed_per_90,
            ROUND((short_passes_attempted/ninetys)::numeric, 2) AS short_passes_attempted_per_90,
            ROUND((medium_passes_completed/ninetys)::numeric, 2) AS medium_passes_completed_per_90,
            ROUND((medium_passes_attempted/ninetys)::numeric, 2) AS medium_passes_attempted_per_90,
            ROUND((long_passes_completed/ninetys)::numeric, 2) AS long_passes_completed_per_90,
            ROUND((long_passes_attempted/ninetys)::numeric, 2) AS long_passes_attempted_per_90,
            ROUND((expected_assists/ninetys)::numeric, 2) AS expected_assists_per_90,
            ROUND((assists_minus_expected_assisted_goals/ninetys)::numeric, 2) AS assists_minus_expected_assisted_goals_per_90,
            ROUND((key_passes/ninetys)::numeric, 2) AS key_passes_per_90,
            ROUND((passes_into_final_third/ninetys)::numeric, 2) AS passes_into_final_third_per_90,
            ROUND((passes_into_penalty_area/ninetys)::numeric, 2) AS passes_into_penalty_area_per_90,
            ROUND((crosses_into_penalty_area/ninetys)::numeric, 2) AS crosses_into_penalty_area_per_90,
            ROUND((shots/ninetys)::numeric, 2) AS shots_per_90,
            ROUND((shots_on_target/ninetys)::numeric, 2) AS shots_on_target_per_90,
            ROUND((goals_per_shot/ninetys)::numeric, 2) AS goals_per_shot_per_90,
            ROUND((goals_per_shot_on_target/ninetys)::numeric, 2) AS goals_per_shot_on_target_per_90,
            ROUND((average_shot_distance/ninetys)::numeric, 2) AS average_shot_distance_per_90,
            ROUND((shots_from_free_kicks/ninetys)::numeric, 2) AS shots_from_free_kicks_per_90,
            ROUND((penalties_made/ninetys)::numeric, 2) AS penalties_made_per_90,
            ROUND((non_penalty_expected_goals_per_shot/ninetys)::numeric, 2) AS non_penalty_expected_goals_per_shot_per_90,
            ROUND((goals_minus_expected_goals/ninetys)::numeric, 2) AS goals_minus_expected_goals_per_90,
            ROUND((non_penalty_goals_minus_non_penalty_expected_goals/ninetys)::numeric, 2) AS non_penalty_goals_minus_non_penalty_expected_goals_per_90,
            ROUND((touches/ninetys)::numeric, 2) AS touches_per_90,
            ROUND((touches_in_defensive_penalty_area/ninetys)::numeric, 2) AS touches_in_defensive_penalty_area_per_90,
            ROUND((touches_in_defensive_third/ninetys)::numeric, 2) AS touches_in_defensive_third_per_90,
            ROUND((touches_in_middle_third/ninetys)::numeric, 2) AS touches_in_middle_third_per_90,
            ROUND((touches_in_attacking_third/ninetys)::numeric, 2) AS touches_in_attacking_third_per_90,
            ROUND((touches_in_attacking_penalty_area/ninetys)::numeric, 2) AS touches_in_attacking_penalty_area_per_90,
            ROUND((live_ball_touches/ninetys)::numeric, 2) AS live_ball_touches_per_90,
            ROUND((take_ons_attempted/ninetys)::numeric, 2) AS take_ons_attempted_per_90,
            ROUND((take_ons_succeeded/ninetys)::numeric, 2) AS take_ons_succeeded_per_90,
            ROUND((times_tackled_during_take_on/ninetys)::numeric, 2) AS times_tackled_during_take_on_per_90,
            ROUND((carries/ninetys)::numeric, 2) AS carries_per_90,
            ROUND((total_carrying_distance/ninetys)::numeric, 2) AS total_carrying_distance_per_90,
            ROUND((progressive_carrying_distance/ninetys)::numeric, 2) AS progressive_carrying_distance_per_90,
            ROUND((carries_into_final_third/ninetys)::numeric, 2) AS carries_into_final_third_per_90,
            ROUND((carries_into_penalty_area/ninetys)::numeric, 2) AS carries_into_penalty_area_per_90,
            ROUND((miscontrols/ninetys)::numeric, 2) AS miscontrols_per_90,
            ROUND((dispossessed/ninetys)::numeric, 2) AS dispossessed_per_90,
            ROUND((passes_received/ninetys)::numeric, 2) AS passes_received_per_90,
            ROUND((tackles/ninetys)::numeric, 2) AS tackles_per_90,
            ROUND((tackles_won/ninetys)::numeric, 2) AS tackles_won_per_90,
            ROUND((defensive_third_tackles/ninetys)::numeric, 2) AS defensive_third_tackles_per_90,
            ROUND((middle_third_tackles/ninetys)::numeric, 2) AS middle_third_tackles_per_90,
            ROUND((attacking_third_tackles/ninetys)::numeric, 2) AS attacking_third_tackles_per_90,
            ROUND((dribblers_tackled/ninetys)::numeric, 2) AS dribblers_tackled_per_90,
            ROUND((dribbler_tackles_attempted/ninetys)::numeric, 2) AS dribbler_tackles_attempted_per_90,
            ROUND((shots_blocked/ninetys)::numeric, 2) AS shots_blocked_per_90,
            ROUND((passes_blocked/ninetys)::numeric, 2) AS passes_blocked_per_90,
            ROUND((interceptions/ninetys)::numeric, 2) AS interceptions_per_90,
            ROUND((clearances/ninetys)::numeric, 2) AS clearances_per_90,
            ROUND((errors_leading_to_shot/ninetys)::numeric, 2) AS errors_leading_to_shot_per_90,
            ROUND((goals_against/ninetys)::numeric, 2) AS goals_against_per_90,
            ROUND((shots_on_target_against/ninetys)::numeric, 2) AS shots_on_target_against_per_90,
            ROUND((saves/ninetys)::numeric, 2) AS saves_per_90,
            ROUND((clean_sheets/ninetys)::numeric, 2) AS clean_sheets_per_90,
            ROUND((penalties_faced/ninetys)::numeric, 2) AS penalties_faced_per_90,
            ROUND((penalties_allowed/ninetys)::numeric, 2) AS penalties_allowed_per_90,
            ROUND((penalties_saved/ninetys)::numeric, 2) AS penalties_saved_per_90,
            ROUND((penalties_missed/ninetys)::numeric, 2) AS penalties_missed_per_90
         FROM
            historic_player_per_ninety
         JOIN
            player_team ON historic_player_per_ninety.player_id = player_team.player_id
            AND historic_player_per_ninety.season = player_team.season
         JOIN
            team ON player_team.team_id = team.id
         JOIN
            player ON historic_player_per_ninety.player_id = player.id
         WHERE
            historic_player_per_ninety.player_id = '{player_id}'
         ORDER BY
            historic_player_per_ninety.season ASC;
      """)
      logger.info(f"Player historic stats for {player_id} retrieved")
      return jsonify(player_historic_stats_by_season)
   except Exception as e:
      logger.error(f"Error with endpoint /players/historic-stats/{player_id}: {str(e)}")
      raise

@registry.handles(
   rule='/players/player-profile',
   method='GET',
   response_body_schema=''
)
def get_player_profile():
   try:
      player_id = request.args.get('player_id')
      player_profile = db.get_dict(f"""
         SELECT
            player.first_name,
            player.last_name,
            player.birth_year,
            player.position,
            historic_player_per_ninety.nationality,
            team.name AS team
         FROM player
         JOIN player_team ON player.id = player_team.player_id
         JOIN team ON player_team.team_id = team.id
         JOIN historic_player_per_ninety ON player.id = historic_player_per_ninety.player_id
         WHERE player.id = '{player_id}' AND player_team.season = (SELECT MAX(season) FROM player_team WHERE player_id = '{player_id}')
         LIMIT 1
      """)
      logger.info(f"Player profile for {player_id} retrieved")
      return jsonify(player_profile)
   except Exception as e:
      logger.error(f"Error with endpoint /players/player-profile/{player_id}: {str(e)}")
      return jsonify({"error": f"Error with endpoint /players/player-profile/{player_id}: {str(e)}"}), 500
   
# /seasons
@registry.handles(
   rule='/seasons',
   method='GET'
)
def get_all_seasons() -> list:
   try:
      seasons = db.get_list(f"""
         SELECT DISTINCT(season) FROM schedule ORDER BY season ASC;
      """)
      seasons = [season[0] for season in seasons]
      logger.info("All seasons retrieved")
      return jsonify(seasons)
   except Exception as e:
      logger.error(f"Error with endpoint /seasons: {str(e)}")
      raise

# /schedule
@registry.handles(
   rule='/schedule',
   method='GET',
)
def get_schedule_by_season() -> list:
   try:
      season = request.args.get('season')
      current_gameweek = request.args.get('get_current_gameweek')
      if current_gameweek:
         current_date = datetime.date.today().strftime("%Y-%m-%d")
         schedule = db.get_list(f"""
            SELECT 
               MIN(round_number) AS game_week
            FROM 
               schedule s
            WHERE 
               date > '{current_date}';
         """)
         logger.info(f"Current gameweek retrieved: {schedule[0][0]}")
         return jsonify(schedule[0][0])
      season_start, season_end = decompose_season(season)
      schedule = db.get_dict(f"""
         SELECT 
            CAST(s.date AS VARCHAR) AS date,
            CAST(s.round_number AS VARCHAR) AS game_week,
            CAST(home_team.name AS VARCHAR) AS home_team,
            CAST(away_team.name AS VARCHAR) AS away_team,
            home_team.id AS home_team_id,
            away_team.id AS away_team_id,
            CAST(s.result AS VARCHAR) AS result,
            s.competition_id AS competition_id
         FROM schedule s
         JOIN team home_team ON s.home_team_id = home_team.id
         JOIN team away_team ON s.away_team_id = away_team.id
         WHERE DATE(s.date) > '{season_start}' AND DATE(s.date) < '{season_end}'
         ORDER BY s.date ASC;
      """)
      logger.info(f"Schedule for season {season} retrieved")
      return jsonify(schedule)
   except Exception as e:
      logger.error(f"Error with endpoint /schedule{'?season='+season if season else ''}: {str(e)}")
      raise

# /matches
@registry.handles(
   rule='/matches',
   method='GET',
)
def get_match_facts():
   date = request.args.get('date') 
   home_team = request.args.get('home_team')
   away_team = request.args.get('away_team')
   try:
      data = db.get_dict(f"""
         SELECT 
            home_team.name AS home_team,
            away_team.name AS away_team,
            m.home_goals,
            m.away_goals,
            m.home_shots,
            m.away_shots,
            m.home_shots_on_target,
            m.away_shots_on_target,
            m.home_corners,
            m.away_corners,
            m.home_fouls,
            m.away_fouls,
            m.home_yellow_cards,
            m.away_yellow_cards,
            m.home_red_cards,
            m.away_red_cards
         FROM match m
         JOIN team home_team ON m.home_team_id = home_team.id
         JOIN team away_team ON m.away_team_id = away_team.id
         WHERE
            date = '{date}' AND
            home_team.name = '{home_team}' AND
            away_team.name = '{away_team}'
      """)
      logger.info(f"Match facts for {home_team} vs {away_team} on {date} retrieved")
      return jsonify(data[0])
   except Exception as e:
      query_params = []
      if date:
         query_params.append(f'date={date}')
      if home_team:
         query_params.append(f'home_team={home_team}')
      if away_team:
         query_params.append(f'away_team={away_team}')
      query_params = '?' + '&'.join(query_params) if query_params else ''
      logger.error(f"Error with endpoint /matches{query_params}: {str(e)}")
      raise

# /prediction
@registry.handles(
   rule='/prediction/stats',
   method='GET',
)
def get_prediction_stats():
   home_team = request.args.get('home_team')
   away_team = request.args.get('away_team')
   try:
      home_team_form = db.get_dict(f"""
         SELECT
            home_team.name AS home_team,
            away_team.name AS away_team,
            CASE
               WHEN home_team.name = '{home_team}' THEN true
               ELSE false
            END AS isHome,
            m.home_goals,
            m.away_goals
         FROM match m
         JOIN team home_team ON m.home_team_id = home_team.id
         JOIN team away_team ON m.away_team_id = away_team.id
         WHERE home_team.name = '{home_team}'
            OR away_team.name = '{home_team}'
         ORDER BY date DESC
         LIMIT 5;
      """)
      away_team_form = db.get_dict(f"""
         SELECT
            home_team.name AS home_team,
            away_team.name AS away_team,
            CASE
               WHEN home_team.name = '{away_team}' THEN true
               ELSE false
            END AS isHome,
            m.home_goals,
            m.away_goals
         FROM match m
         JOIN team home_team ON m.home_team_id = home_team.id
         JOIN team away_team ON m.away_team_id = away_team.id
         WHERE home_team.name = '{away_team}'
            OR away_team.name = '{away_team}'
         ORDER BY date DESC
         LIMIT 5;
      """)

      home_team_average_stats = db.get_dict(f"""
         SELECT 
            ROUND(AVG(home_goals), 2) AS home_goals,
            ROUND(AVG(home_shots), 2) AS home_shots,
            ROUND(AVG(home_shots_on_target), 2) AS home_shots_on_target,
            ROUND(AVG(home_corners), 2) AS home_corners,
            ROUND(AVG(home_fouls), 2) AS home_fouls,
            ROUND(AVG(home_yellow_cards), 2) AS home_yellow_cards,
            ROUND(AVG(home_red_cards), 2) AS home_red_cards
         FROM match m
         JOIN team home_team ON m.home_team_id = home_team.id
         WHERE home_team.name = '{home_team}'
         LIMIT 5
      """)
      away_team_average_stats = db.get_dict(f"""
         SELECT 
            ROUND(AVG(away_goals), 2) AS away_goals,
            ROUND(AVG(away_shots), 2) AS away_shots,
            ROUND(AVG(away_shots_on_target), 2) AS away_shots_on_target,
            ROUND(AVG(away_corners), 2) AS away_corners,
            ROUND(AVG(away_fouls), 2) AS away_fouls,
            ROUND(AVG(away_yellow_cards), 2) AS away_yellow_cards,
            ROUND(AVG(away_red_cards), 2) AS away_red_cards
         FROM match m
         JOIN team away_team ON m.away_team_id = away_team.id
         WHERE away_team.name = '{away_team}'
         LIMIT 5
      """)

      head_to_head_stats = db.get_dict(f"""
         SELECT
            home_team.name AS home_team,
            away_team.name AS away_team,
            home_goals AS home_goals,
            away_goals AS away_goals,
            home_shots AS home_shots,
            away_shots AS away_shots,
            home_shots_on_target AS home_shots_on_target,
            away_shots_on_target AS away_shots_on_target,
            home_corners AS home_corners,
            away_corners AS away_corners,
            home_fouls AS home_fouls,
            away_fouls AS away_fouls,
            home_yellow_cards AS home_yellow_cards,
            away_yellow_cards AS away_yellow_cards,
            home_red_cards AS home_red_cards,
            away_red_cards AS away_red_cards
         FROM match m
         JOIN team home_team ON m.home_team_id = home_team.id
         JOIN team away_team ON m.away_team_id = away_team.id
         WHERE (
            home_team.name = '{home_team}' AND
            away_team.name = '{away_team}'
         ) OR (
            home_team.name = '{away_team}' AND
            away_team.name = '{home_team}'
         )
         LIMIT 5
      """)
      logger.info(f"Prediction stats for {home_team} vs {away_team} retrieved")
      return jsonify(
         {
            "home_team_form": home_team_form, 
            "away_team_form": away_team_form,
            "home_team_average_stats": home_team_average_stats, 
            "away_team_average_stats": away_team_average_stats,
            "head_to_head_stats": head_to_head_stats
         }
      )
   except Exception as e:
      logger.error(f"Error with endpoint /prediction/stats: {str(e)}")
      raise
   
@registry.handles(
   rule='/prediction/squads',
   method='GET',
)
def get_prediction_squads() -> list:
   try:
      home_team = request.args.get('home_team')
      away_team = request.args.get('away_team')

      home_team_squad = db.get_dict(f"""
         WITH current_season AS (
            SELECT 
               MAX(season) AS season
            FROM
               player_team
         )
                                    
         SELECT
            player.first_name,
            player.last_name,
            player.position
         FROM player
         JOIN player_team ON player.id = player_team.player_id
         JOIN team ON player_team.team_id = team.id
         JOIN current_season ON TRUE
         WHERE team.name = '{home_team}'
            AND player_team.season = current_season.season
         ORDER BY player.last_name ASC
      """)
      
      away_team_squad = db.get_dict(f"""
         WITH current_season AS (
            SELECT 
               MAX(season) AS season
            FROM
               player_team
         )
                                    
         SELECT
            player.first_name,
            player.last_name,
            player.position
         FROM player
         JOIN player_team ON player.id = player_team.player_id
         JOIN team ON player_team.team_id = team.id
         JOIN current_season ON TRUE
         WHERE team.name = '{away_team}'
            AND player_team.season = current_season.season
         ORDER BY player.last_name ASC
      """)
      logger.info(f"Prediction squads for {home_team} vs {away_team} retrieved")
      return jsonify({"home_team_squad": home_team_squad, "away_team_squad": away_team_squad})
   except Exception as e:
      logger.error(f"Error with endpoint /prediction/squads: {str(e)}")
      raise

# /visualisation
@registry.handles(
   rule='/visualisation',
   method='GET',
)
def get_stats_for_charts() -> list:
   try:
      table_name = request.args.get('table_name')
      entity_ids = request.args.get('entities', "")
      stats = request.args.get('stats', "")
      start_season = f"'{request.args.get('start_season', '2017-2018')}'"
      end_season = f"'{request.args.get('end_season', '2024-2025')}'"
      per_ninety = bool(int(request.args.get('per_ninety', 0)))
      x_axis = request.args.get('x_axis', "season")

      if len(entity_ids.split(",")) == 0 or len(stats.split(",")) == 0:
         raise Exception("No entity ids or stats provided")
      sum_stats = ",".join([(f'SUM({stat}) AS {stat}') for stat in stats.split(",")])

      player_query = f"""
         SELECT player_id, player.first_name || ' ' || player.last_name as name, season, 
         SUM(ninetys), {sum_stats}
         FROM historic_player_per_ninety
         LEFT JOIN player ON player.id = player_id
         WHERE player_id IN ({entity_ids}) AND season >= {start_season} AND season <= {end_season}
         GROUP BY player_id, season, player.first_name, player.last_name
      """
      team_query = f"""
         SELECT team_id, season, team.name as name, {sum_stats}
         FROM historic_player_per_ninety
         LEFT JOIN team ON team.id = team_id
         WHERE team_id IN ({entity_ids}) AND season >= {start_season} AND season <= {end_season}
         GROUP BY team_id, season, team.name
      """

      query = player_query if table_name == "player" else team_query
      print(query)

      logger.info(f"Query: {query}")
      df = db.get_df(query)
      print(df)

      if per_ninety:
         df[stats] = df[stats].div(df["ninetys"], axis=0)

      x_axis_values = []
      y_axis_values = {}

      if x_axis == "season":
         x_axis_values = sorted(df["season"].unique().tolist())

      for stat in stats.split(","):
         entity_stats = []
         for entity_id in entity_ids.replace("'", "").split(","):
            entity_data = df[df[f"{table_name}_id"] == entity_id]
            if len(entity_data) < len(x_axis_values):
               missing_seasons = list(set(x_axis_values) - set(entity_data["season"]))
               print(missing_seasons)
               for season in missing_seasons:
                  new_row = entity_data.iloc[0].copy()
                  new_row["season"] = season
                  new_row[stat] = 0 # Change to allow missing values, None/np.nan/"NaN" does not work
                  print(new_row)
                  entity_data = pd.concat([entity_data, pd.DataFrame([new_row])], ignore_index=True)
                  print(entity_data)

            entity_data = entity_data.sort_values(by="season")
            entity_data["x"] = entity_data["season"]
            entity_data["y"] = entity_data[stat]
            ent_id = entity_data["name"].to_list()[0]

            y_axis = entity_data["y"].to_list()
            entity_stats.append({"data": y_axis, "label": ent_id, })
         y_axis_values[stat] = entity_stats

      if table_name == "team":
         pass

      print("\n\n")
      print(x_axis_values)
      print(y_axis_values)

      print(jsonify([x_axis_values, y_axis_values]).json)
      return jsonify([x_axis_values, y_axis_values])
   except Exception as e:
      query_params = []
      if table_name:
         query_params.append(f'table_name={table_name}')
      if entity_ids:
         query_params.append(f'entities={entity_ids}')
      if stats:
         query_params.append(f'stats={stats}')
      if start_season:
         query_params.append(f'start_season={start_season}')
      if end_season:
         query_params.append(f'end_season={end_season}')
      if per_ninety:
         query_params.append(f'per_ninety={per_ninety}')
      if x_axis:
         query_params.append(f'x_axis={x_axis}')
      query_string = '?' + '&'.join(query_params) if query_params else ''
      logger.error(f"Error with endpoint /visualisation{query_string}: {str(e)}")
      raise

@registry.handles(
   rule='/visualisation/player-columns',
   method='GET',
)
def get_player_comp_columns() -> list:
   try:
      comp_cols = db.get_list("""
         SELECT column_name
         FROM information_schema.columns
         WHERE table_name = 'historic_player_per_ninety'
      """)
      comp_cols = [col[0] for col in comp_cols if col[0] not in ["id", "season", "player_id", "team_id"] and not any(op in col[0] for op in ["plus", "minus", "divided"])]
      logger.info(f"Player comparison columns retrieved: {comp_cols}")
      return jsonify(sorted(comp_cols))
   except Exception as e:
      logger.error(f"Error getting player comparison columns: {str(e)}")
      raise

@registry.handles(
   rule='/visualisation/team-columns',
   method='GET',
)
def get_team_comp_columns() -> list:
   try:
      comp_cols = db.get_list("""
         SELECT column_name
         FROM information_schema.columns
         WHERE table_name = 'historic_player_per_ninety'
      """)
      comp_cols = [col[0] for col in comp_cols if col[0] not in ["id", "season", "ninetys", "player_id", "team_id"] and not any(op in col[0] for op in ["plus", "minus", "divided"])]

      # all = ["league_finishes", "league_points", "league_goals_for", "league_goals_against", "league_goal_difference"]+comp_cols
      logger.info(f"Team comparison columns retrieved: {comp_cols}")
      return jsonify(sorted(comp_cols))
   except Exception as e:
      logger.error(f"Error getting team comparison columns: {str(e)}")
      raise

# /league-table
@registry.handles(
   rule="/league-table",
   method="GET",
)
def get_league_table():
   try:
      season = request.args.get('season') 
      query = f"""
      WITH league_table AS (
         SELECT
            team.id,
            team.name,
            COUNT(*) AS matches_played,
            SUM(
               CASE
                  WHEN home_team_id = team.id
                  AND SPLIT_PART(result, ' - ', 1) > SPLIT_PART(result, ' - ', 2) THEN 3
                  WHEN away_team_id = team.id
                  AND SPLIT_PART(result, ' - ', 2) > SPLIT_PART(result, ' - ', 1) THEN 3
                  WHEN SPLIT_PART(result, ' - ', 1) = SPLIT_PART(result, ' - ', 2) THEN 1
                  ELSE 0
               END
            ) AS total_points,
            SUM(
               CASE
                  WHEN home_team_id = team.id
                  AND SPLIT_PART(result, ' - ', 1) > SPLIT_PART(result, ' - ', 2) THEN 1
                  WHEN away_team_id = team.id
                  AND SPLIT_PART(result, ' - ', 2) > SPLIT_PART(result, ' - ', 1) THEN 1
                  ELSE 0
               END
            ) AS wins,
            SUM(
               CASE
                  WHEN SPLIT_PART(result, ' - ', 1) = SPLIT_PART(result, ' - ', 2) THEN 1
                  ELSE 0
               END
            ) AS draws,
            SUM(
               CASE
                  WHEN home_team_id = team.id
                  AND SPLIT_PART(result, ' - ', 1) < SPLIT_PART(result, ' - ', 2) THEN 1
                  WHEN away_team_id = team.id
                  AND SPLIT_PART(result, ' - ', 2) < SPLIT_PART(result, ' - ', 1) THEN 1
                  ELSE 0
               END
            ) AS losses,
            SUM(
               CASE
                  WHEN home_team_id = team.id THEN CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER)
                  ELSE CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER)
               END
            ) AS goals_for,
            SUM(
               CASE
                  WHEN home_team_id = team.id THEN CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER)
                  ELSE CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER)
               END
            ) AS goals_against,
            SUM(
               CASE
                  WHEN home_team_id = team.id THEN CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER) - CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER)
                  ELSE CAST(SPLIT_PART(result, ' - ', 2) AS INTEGER) - CAST(SPLIT_PART(result, ' - ', 1) AS INTEGER)
               END
            ) AS goal_difference
         FROM
            schedule
         JOIN team ON team.id = home_team_id OR team.id = away_team_id
         WHERE 
            season = '{season}' AND result != '-'
         GROUP BY 
            team.id, team.name
      )

      SELECT
         ROW_NUMBER() OVER(ORDER BY total_points DESC, goal_difference DESC, goals_for DESC) AS position,
         id,
         name,
         matches_played,
         wins,
         draws,
         losses,
         goals_for,
         goals_against,
         goal_difference,
         total_points
      FROM
         league_table
      """

      league_table = db.get_dict(query)
      logger.info(f"League table for {season} retrieved")
      return jsonify(league_table)
   except Exception as e:
      logger.error(f"Error with endpoint /league-table?season={season}: {str(e)}")
      raise

# /managers
@registry.handles(
   rule="/managers",
   method="GET",
)
def get_all_managers():
   try:
      all_managers = db.get_dict("""
         SELECT 
            manager.id,
            first_name,
            last_name,
            team_id,
            team.name AS team_name,
            start_date,
            end_date,
            end_date = 'current' AS current_job
         FROM
            manager
         JOIN
            team ON manager.team_id = team.id
         ORDER BY
            last_name ASC;
      """)
      logger.info("All managers retrieved")
      return jsonify(all_managers)
   except Exception as e:
      logger.error(f"Error with endpoint /managers: {str(e)}")
      raise

app = Flask(__name__)
CORS(app, origins=["http://frontend:3000", "http://localhost:3000", "http://frontend:3001", "http://localhost:3001"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")
