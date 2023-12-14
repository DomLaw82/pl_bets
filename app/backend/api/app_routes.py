from flask import Flask
from flask_rebar import Rebar, ResponseSchema
from marshmallow import fields

rebar = Rebar()
registry = rebar.create_handler_registry()

# class TeamSchema(ResponseSchema):
#     id = fields.Integer()

# add teams
# view teams
# add competition
# view competition
# add country
# view country
# add match
# view match
# add player
# view player
# add performance
# view performance

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

# add teams
# view teams
# add competition
# view competition
# add country
# view country
# add match
# view match
# add player
# view player
# add performance
# view performance

# replace team season stats

# ingest squad data
# ingest team data
# ingest schedule data
# ingest match facts
# ingest historic player season stats

# predict match stats
	# set home team lineup
	# set home team subs
	# set away team lineup
	# set away team subs