from flask import Flask, request, jsonify, render_template
from flask_rebar import Rebar
from flask_cors import CORS
from schemas import *
import pandas as pd
from db_connection import local_pl_stats_connector
from flask import render_template
from datetime import datetime
import urllib.parse

db = local_pl_stats_connector
rebar = Rebar()
registry = rebar.create_handler_registry()

# Generate Flask Rebar views, routes, etc.
# registry.generate_swagger(generator=generator)

### routes ###

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
def get_teams() :
   teams = db.get_dict(f"""
      SELECT * from team ORDER BY name ASC
   """)
   return jsonify(teams)

# all teams
@registry.handles(
   rule='/active-teams',
   method='GET',
   response_body_schema=TeamSchema(many=True)
)
def get_active_teams() :
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

# all players
@registry.handles(
   rule='/players',
   method='GET',
   response_body_schema=PlayerTeamNameSchema(many=True)
)
def get_all_players() :
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

# current team roster
@registry.handles(
   rule='/all-active-players',
   method='GET',
   response_body_schema=''
)
def get_all_current_players(team_id:str) -> list:
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

@registry.handles(
   rule='/active-players/<team_id>',
   method='GET',
   response_body_schema=''
)
def get_team_current_roster(team_id:str) -> list:
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

@registry.handles(
   rule='/matches/all-seasons',
   method='GET'
)
def get_all_seasons() -> list:
   seasons = db.get_list(f"""
      SELECT DISTINCT(season) FROM match ORDER BY season ASC
   """)

   seasons = [season[0] for season in seasons]
   return jsonify(seasons)

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
   print(schedule)
   return jsonify(schedule)

@registry.handles(
   rule='/matches/add-result',
   method='POST',
   response_body_schema=''
)
def add_match_result():
   try:
      data = request.get_json()

      game_week = data.get("game-week")
      match_date = data.get("match-date")
      home_team = data.get("home-team")
      away_team = data.get("away-team")
      home_goals = data.get("home-goals")
      away_goals = data.get("away-goals")

      season = data.get("season")
      competition_id = data.get("competition-id")
      referee_id = data.get("referee-id")
      home_shots = data.get("home-shots")
      away_shots = data.get("away-shots")
      home_shots_on_target = data.get("home-shots-on-target")
      away_shots_on_target = data.get("away-shots-on-target")
      home_corners = data.get("home-corners")
      away_corners = data.get("away-corners")
      home_fouls = data.get("home-fouls")
      away_fouls = data.get("away-fouls")
      home_yellow_cards = data.get("home-yellow-cards")
      away_yellow_cards = data.get("away-yellow-cards")
      home_red_cards = data.get("home-red-cards")
      away_red_cards = data.get("away-red-cards")

      home_team_id = db.get_list(f"SELECT id FROM team WHERE name = '{home_team}'")[0][0]
      away_team_id = db.get_list(f"SELECT id FROM team WHERE name = '{away_team}'")[0][0]

      if home_team and away_team and home_goals and away_goals and match_date and game_week:
         db.execute(f"""
            UPDATE schedule
            SET result = '{home_goals}-{away_goals}'
            WHERE home_team_id = '{home_team_id}' AND away_team_id = '{away_team_id}' AND date = '{match_date.split("T")[0]} {match_date.split("T")[1]}:00' AND round_number = '{game_week}' AND competition_id = '{competition_id}'
         """)
         return jsonify({"message": "Match result added successfully"}), 200
      if away_red_cards:
         db.execute(f"""
            INSERT INTO match (season, competition_id, home_team_id, away_team_id, referee_id, home_goals, away_goals, home_shots, away_shots, home_shots_on_target, away_shots_on_target, home_corners, away_corners, home_fouls, away_fouls, home_yellow_cards, away_yellow_cards, home_red_cards, away_red_cards)
            VALUES ('{season}', '{competition_id}', '{home_team_id}', '{away_team_id}', '{referee_id}', '{home_goals}', '{away_goals}', '{home_shots}', '{away_shots}', '{home_shots_on_target}', '{away_shots_on_target}', '{home_corners}', '{away_corners}', '{home_fouls}', '{away_fouls}', '{home_yellow_cards}', '{away_yellow_cards}', '{home_red_cards}', '{away_red_cards}')
         """)
         return jsonify({"message": "Match result added successfully"}), 200
   except Exception as e:
      return jsonify({"error": str(e)}), 500

@registry.handles(
   rule='/update/historic_per_ninety/submit',
   method='POST',
)
def update_historic_per_ninety(content:str):
   try:
        if 'file' not in request.files:
            return jsonify({'ERROR': 'No file part'}), 400
        file = request.files['file']

        if file.filename == '':
            return jsonify({'ERROR': 'No selected file'}), 400
        if not file.filename.endswith('.csv'):
            return jsonify({'ERROR': 'Invalid file format. Must be a CSV file'}), 400

        df = pd.read_csv(file)
        df.to_sql("historic_player_per_ninety", local_pl_stats_connector.conn, if_exists="append", )
        return jsonify({'message': 'CSV file uploaded successfully'}), 200
   
   except Exception as e:
        return jsonify({'error': str(e)}), 500

@registry.handles(
   rule='/matches/match-facts',
   method='GET',
)
def get_match_facts():
   date = request.args.get('date')
   home_team = request.args.get('home_team')
   away_team = request.args.get('away_team')

   date = urllib.parse.unquote(date)
   home_team = urllib.parse.unquote(home_team)
   away_team = urllib.parse.unquote(away_team)
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
      return jsonify({'error': str(e)}), 500

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
CORS(app, origins=["http://localhost:3000", "http://10.127.67.163:3001", "http://frontend:3000"], supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")
