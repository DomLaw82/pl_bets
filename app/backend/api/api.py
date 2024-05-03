from flask import Flask, request, jsonify, render_template
from flask_rebar import Rebar
from flask_cors import CORS
from schemas import *
import pandas as pd
from db_connection import local_pl_stats_connector
from flask import render_template
from datetime import datetime

db = local_pl_stats_connector
rebar = Rebar()
registry = rebar.create_handler_registry()

# Generate Flask Rebar views, routes, etc.
# registry.generate_swagger(generator=generator)

### routes ###

@registry.handles(
   rule='/health',
   method='GET',
)
def health():
      return jsonify({"status": "healthy"})

# index
@registry.handles(
   rule='/',
   method='GET',
)
def index():
    return jsonify({"title": "Welcome to PL Bets"})

# all teams
@registry.handles(
   rule='/teams',
   method='GET',
   response_body_schema=TeamSchema(many=True)
)
def get_teams():
   try:
      teams = db.get_dict(f"""
         SELECT * from team ORDER BY name ASC
      """)
      return jsonify(teams)
   except Exception as e:
      return jsonify({"error":f"Error with endpoint /teams: {str(e)}"}), 500

# all teams
@registry.handles(
   rule='/active-teams',
   method='GET',
   response_body_schema=TeamSchema(many=True)
)
def get_active_teams() :
   try:
      teams = db.get_dict(f"""
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
      """)
      return jsonify(teams)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /active-teams: {str(e)}"}), 500

# all players
@registry.handles(
   rule='/players',
   method='GET',
   response_body_schema=PlayerTeamNameSchema(many=True)
)
def get_all_players() :
   try:
      players = db.get_dict(f"""
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
            player.birth_date,
            player.position,
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
      """)
      return jsonify(players)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /players: {str(e)}"}), 500

# current team roster
@registry.handles(
   rule='/all-active-players',
   method='GET',
   response_body_schema=''
)
def get_all_active_players() -> list:
   try:
      players = db.get_dict(f"""
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
            player.birth_date AS birth_date,
            player.position AS position,
            team.name AS team_name
         FROM
            player
         JOIN current_season ON TRUE
         JOIN player_team ON player.id = player_team.player_id
         JOIN team ON player_team.team_id = team.id
         WHERE player_team.season = current_season.season
         ORDER BY player.last_name ASC
      """)
      return jsonify(players)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /all-active-players: {str(e)}"}), 500

@registry.handles(
   rule='/active-players/<team_id>',
   method='GET',
   response_body_schema=''
)
def get_team_current_roster(team_id:str) -> list:
   try:
      players = db.get_dict(f"""
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
            player.birth_date AS birth_date,
            player.position AS position
         FROM
            player
         JOIN current_season ON TRUE
         JOIN player_team ON player.id = player_team.player_id
         WHERE player_team.team_id = '{team_id}'
         AND player_team.season = current_season.season
         ORDER BY player.last_name ASC
      """)
      return jsonify(players)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /active-players/{team_id}: {str(e)}"}), 500

@registry.handles(
   rule='/matches/all-seasons',
   method='GET'
)
def get_all_seasons() -> list:
   try:
      seasons = db.get_list(f"""
         SELECT DISTINCT(season) FROM match ORDER BY season ASC
      """)

      seasons = [season[0] for season in seasons]
      return jsonify(seasons)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /matches/all-seasons: {str(e)}"}), 500

def decompose_season(season: str) -> tuple:
   start_year, end_year = season.split('-')
   start_month = '08'
   end_month = '05'
   
   start_date = datetime.strptime(f"{start_year}-{start_month}-01", "%Y-%m-%d")
   end_date = datetime.strptime(f"{end_year}-{end_month}-31", "%Y-%m-%d")
   
   return (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))


@registry.handles(
   rule='/matches/season/<season>',
   method='GET',
   response_body_schema=ScheduleSchema(many=True)
)
def get_schedule_by_season(season:str) -> list:
   try:
      season_start, season_end = decompose_season(season)
      schedule = db.get_dict(f"""
         SELECT 
            CAST(s.date AS VARCHAR) AS date,
            CAST(s.round_number AS VARCHAR) AS game_week,
            CAST(home_team.name AS VARCHAR) AS home_team,
            CAST(away_team.name AS VARCHAR) AS away_team,
            CAST(s.result AS VARCHAR) AS result,
            s.competition_id AS competition_id
         FROM schedule s
         JOIN team home_team ON s.home_team_id = home_team.id
         JOIN team away_team ON s.away_team_id = away_team.id
         WHERE DATE(s.date) > '{season_start}' AND DATE(s.date) < '{season_end}'
         ORDER BY s.date ASC;
      """)
      return jsonify(schedule)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /matches/season/{season}: {str(e)}"}), 500
   
@registry.handles(
   rule='/matches/match-facts',
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
      return jsonify(data)
   except Exception as e:
      return jsonify({'error': f"Error with endpoint /matches/match-facts: {str(e)}"}), 500
   
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
      return jsonify({'error': f"Error with endpoint /prediction/stats: {str(e)}"}), 500
   
@registry.handles(
   rule='/prediction/squads',
   method='GET',
   response_body_schema=''
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
      return jsonify({"home_team_squad": home_team_squad, "away_team_squad": away_team_squad})
   except Exception as e:
      return jsonify({'error': f"Error with endpoint /prediction/squads: {str(e)}"}), 500


@registry.handles(
   rule="/prediction/team-id",
   method="GET",
   response_body_schema=""
)
def get_team_id():
   try:
      team_name = request.args.get('team_name')
      team_id = db.get_dict(f"SELECT id FROM team WHERE name = '{team_name}'")[0]
      return jsonify(team_id)
   except Exception as e:
      return jsonify({'error': f"Error with endpoint /prediction/team-id: {str(e)}"}), 500

@registry.handles(
   rule='/players/historic-stats/<player_id>',
   method='GET',
   response_body_schema=''
)
def get_player_historic_stats_by_season(player_id:str) -> list:
   try:
      player_historic_stats_by_season = db.get_dict(f"""
         SELECT 
            historic_player_per_ninety.season,
            player.first_name,
            player.last_name,
            team.name AS team,
            minutes_played AS minutes,
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
      return jsonify(player_historic_stats_by_season)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /players/historic-stats/{player_id}: {str(e)}"}), 500

@registry.handles(
   rule='/players/recent-minutes/<player_id>',
   method='GET',
   response_body_schema=''
)
def get_player_recent_minutes_stats_by_season(player_id:str) -> list:
   try:
      player_recent_minutes_stats_by_season = db.get_dict(f"""
         SELECT 
            season,
            minutes_played AS minutes,
            ninetys AS ninetys
         FROM
            historic_player_per_ninety
         WHERE
            player_id = '{player_id}'
            AND season = (SELECT MAX(season) FROM historic_player_per_ninety)
         ORDER BY
            season ASC;
      """)
      return jsonify(player_recent_minutes_stats_by_season)
   except Exception as e:
      return jsonify({"error": f"Error with endpoint /players/recent-minutes/{player_id}: {str(e)}"}), 500



# @registry.handles(
#    rule='/download-latest-data',
#    method='GET',
#    response_body_schema=''
# )
# def download_latest_data():
#    # module will be available in the container, but is not in the path locally (see app/backend/database/ingestion/__init__.py)
#    # TODO - refactor this so that the module is available locally/create empty file locally
#    message = download_and_insert_latest_data()
#    return jsonify(message)


app = Flask(__name__)
CORS(app, origins=["http://frontend:3000", "http://localhost:3000", "http://frontend:3001", "http://localhost:3001"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")
