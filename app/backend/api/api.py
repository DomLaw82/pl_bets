from flask import Flask, request, jsonify
from flask_rebar import Rebar
from schemas import *
import pandas as pd
from db_connection import local_pl_stats_connector

rebar = Rebar()
registry = rebar.create_handler_registry()

# Generate Flask Rebar views, routes, etc.
registry.generate_swagger(generator=generator)

### routes ###
# index
def index():
    return jsonify({"title": "Welcome to PL Bets"})

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


# run prediction model
   # confirm lineups
# confirm lineups
   	# set home team lineup
      # set home team subs
      # set away team lineup
      # set away team subs
# check current gameweek fixtures
   # display predicted and actual (if inputted) stats
   # flag for whether lineups have been selected
   # pre lineup prediction (based on historic game time) and actual lineup
# check next gameweek fixtures
# check entire schedule
# input match facts

# @registry.handles(
#    rule='/add/teams',
#    method='POST',
#    response_body_schema=TodoSchema()  # for versions <= 1.7.0, use marshal_schema
# )

app = Flask(__name__)
rebar.init_app(app)

if __name__ == '__main__':
    app.run()
