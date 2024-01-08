from flask import Flask, request, jsonify, render_template
from flask_rebar import Rebar
from flask_cors import CORS
from schemas import *
import pandas as pd
from db_connection import local_pl_stats_connector
from flask import render_template

db = local_pl_stats_connector
rebar = Rebar()
registry = rebar.create_handler_registry()

# Generate Flask Rebar views, routes, etc.
# registry.generate_swagger(generator=generator)

def list_to_list_of_objects(list_of_tuples:list, column_names: list) -> dict:
   """
   Convert a list of tuples to a dict

   Args:
         list_of_tuples (list): list of tuples
         column_names (list): list of column names in the order they appear in the tuples

   Returns:
         list: list of dicts
   """
   result_list = []
   for row in list_of_tuples:
      entry = {}
      for index_b, col in enumerate(row):
         entry[column_names[index_b]] = col
      result_list.append(entry)
   return result_list

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
   teams = db.get_list(f"""
      SELECT * from team ORDER BY name ASC
   """)
   teams = list_to_list_of_objects(teams, ['id', 'name'])
   return jsonify(teams)

# all teams
@registry.handles(
   rule='/active-teams',
   method='GET',
   response_body_schema=TeamSchema(many=True)
)
def get_active_teams() :
   teams = db.get_list(f"""
      WITH current_season AS (
         SELECT 
            MAX(season) AS season
         FROM
            player_team
      )
      SELECT
         DISTINCT(team.id) AS id,
         name AS team_name
      FROM
         team
      JOIN current_season ON TRUE
      JOIN player_team ON team.id = player_team.team_id 
         AND player_team.season = current_season.season
      ORDER BY team_name ASC
   """)
   teams = list_to_list_of_objects(teams, ['id','name'])
   return jsonify(teams)

# all players
@registry.handles(
   rule='/players',
   method='GET',
   response_body_schema=PlayerTeamNameSchema(many=True)
)
def get_all_players() :
   players = db.get_list(f"""
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
   players = list_to_list_of_objects(players, ["id", "first_name", "last_name", "birth_date", "position", "team_name", "active"])

   return jsonify(players)

# current team roster
@registry.handles(
   rule='/active-players/<team_name>',
   method='GET',
   response_body_schema=''
)
def get_team_current_roster(team_name:str) -> list:
   team_id = db.get_list(f"SELECT id FROM team WHERE name = '{team_name}'")[0][0] or None
   if team_id:
      players = db.get_list(f"""
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
      players = list_to_list_of_objects(players, ["id", "first_name", "last_name", "birth_date", "position"])
      return jsonify(players)

# run prediction model --- /predict/run POST
@registry.handles(
   rule='/predict',
   method='POST',
   response_body_schema=''
)
def show_prediction_form():
   return render_template('../views/prediction_form.html')
   # confirm lineups
# confirm lineups --- /predict/confirm-lineups
   	# set home team lineup --- /predict/confirm-lineups/home-start POST
      # set home team subs --- /predict/confirm-lineups/home-sub POST
      # set away team lineup  --- /predict/confirm-lineups/away-start POST
      # set away team subs  --- /predict/confirm-lineups/away-sub POST

# check current gameweek fixtures --- /gameweek/current
   # display predicted and actual (if inputted) stats
   # flag for whether lineups have been selected
   # pre lineup prediction (based on historic game time) and actual lineup
# check next gameweek fixtures --- /gameweek/next
# check entire schedule --- /schedule
# input match facts --- /update/match-facts
# update squads --- /update/squads

# data
   # update historic player stats
      # upload csv and handle operations in the backend
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
   # re-ingest squad data
   # re-ingest team data
   # re-ingest schedule data
   # re-ingest match facts
   # add player injury



# @registry.handles(
#    rule='/add/teams',
#    method='POST',
#    response_body_schema=TodoSchema()  # for versions <= 1.7.0, use marshal_schema
# )

app = Flask(__name__)
CORS(app, origins=["http://frontend:3000", "http://localhost:3000"],  supports_credentials=True)
rebar.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")
