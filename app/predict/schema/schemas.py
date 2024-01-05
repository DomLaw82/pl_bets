from flask_rebar import Rebar, SwaggerV2Generator
from marshmallow import Schema, fields

rebar = Rebar()
generator = SwaggerV2Generator()

# Define Flask Rebar schemas using Marshmallow
class match_facts_schema(Schema):
	home_goals = fields.Float()
	away_goals = fields.Float()
	home_shots = fields.Float()
	away_shots = fields.Float()
	home_shots_on_target = fields.Float()
	away_shots_on_target = fields.Float()
	home_corners = fields.Float()
	away_corners = fields.Float()
	home_fouls = fields.Float()
	away_fouls = fields.Float()
	home_yellow_cards = fields.Float()
	away_yellow_cards = fields.Float()
	home_red_cards = fields.Float()
	away_red_cards = fields.Float()

class retune_schema(Schema):
	batch_size = fields.Integer()
	dropout = fields.Float(), 
	epochs = fields.Integer()
	hidden_layer_one =fields.Integer()
	learn_rate =	fields.Float()
	n_h_layers =	fields.Integer()
	score = fields.Float()
