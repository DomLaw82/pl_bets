from flask import Flask, request, jsonify
from flask_rebar import Rebar
from schemas import *
import pandas as pd
from db_connection import local_pl_stats_connector

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

# current team roster
@registry.handles(
   rule='/<team_id>/current',
   method='GET',
   response_body_schema=PlayerSchema()
)
def get_team_current_roster(team_id:str) :
   players = db.get_list(f"""
      SELECT player.*
      FROM player
      JOIN player_team ON player.id = player_team.player_id
      WHERE player_team.team_id = {team_id}
      AND player_team.season = (
         SELECT MAX(season)
         FROM player_team
         WHERE team_id = {team_id}
      )
  """)
   return jsonify(players)

# run prediction model --- /predict/run POST
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
rebar.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8080")
