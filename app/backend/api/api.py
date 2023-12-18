from flask import Flask
from flask_rebar import Rebar, ResponseSchema

rebar = Rebar()
registry = rebar.create_handler_registry()

### routes ###
# data
   # update historic player stats
      # upload csv and handle operations in the backend
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

@registry.handles(
   rule='/add/teams',
   method='GET',
   response_body_schema=TodoSchema()  # for versions <= 1.7.0, use marshal_schema
)

@registry.handles(
   rule='/add/competition',
   method='GET',
   response_body_schema=TodoSchema()  # for versions <= 1.7.0, use marshal_schema
)

@registry.handles(
   rule='/add/country',
   method='GET',
   response_body_schema=TodoSchema()  # for versions <= 1.7.0, use marshal_schema
)

@registry.handles(
   rule='/add/match',
   method='GET',
   response_body_schema=TodoSchema()  # for versions <= 1.7.0, use marshal_schema
)

app = Flask(__name__)
rebar.init_app(app)

if __name__ == '__main__':
    app.run()

# replace team season stats



# predict match stats
