from database.utilities import unique_id, validation
from database.cli import cl_output
from pandas import DataFrame

def collect(connector, **kwargs) -> None:
	print("""\n+++++++++++++++++++\n  Add performance  \n+++++++++++++++++++\n""")
	
	abbreviation = kwargs.get("abbreviation")
	match_id = kwargs.get("match_id")
	previously_selected_players = kwargs.get("previously_selected_players")
	if previously_selected_players:
		team_players = connector.get_dict(f"SELECT id, first_name, last_name, team FROM player JOIN player_team ON player_team.player_id = player.id WHERE team = '{abbreviation}' AND id NOT IN ({','.join(previously_selected_players)})")
	else:
		team_players = connector.get_dict(f"SELECT id, first_name, last_name, team FROM player JOIN player_team ON player_team.player_id = player.id WHERE team = '{abbreviation}'")
	
	player_ids = [player['id'] for player in team_players.values()]
	cl_output.print_dict_table(team_players)

	player_id = validation.validate("int", input("Select player by id: "), "Select player by id: ")
	player_id = validation.validate("in_list", player_id, var_list=player_ids)
	
	previously_selected_players.append(player_id)

	player_data = {}

	performance_columns = {
		"red_cards": "int",
		"blocks": "int",
		"interceptions": "int",
		"clearances": "int",
		"fouls": "int",
		"yellow_cards": "int",
		"minutes_played": "int",
		"goals": "int",
		"x_goals": "float",
		"assists": "int",
		"x_assists": "float",
		"shots":	"int",
		"shots_on_target": "int",
		"passes_attempted": "int",
		"passes_completed": "int",
		"progressive_passes_completed": "int",
		"take_ons_attempted": "int",
		"take_ons_completed": "int",
		"touches_def_third": "int",
		"touches_mid_third": "int",
		"touches_att_third": "int",
		"carries": "int",
		"total_carrying_distance": "float",
		"tackles": "int",
		"role": "text",
		"position": "text",
	}

	performance_columns = connector.get_list(f"SELECT column_name FROM information_schema.columns WHERE table_name = 'performance';")
	performance_columns = [col[0] for col in performance_columns]

	for col in performance_columns:
		
		if col == "match_id":
			player_data["match_id"] = match_id
			continue
		if col == "team_played_for":
			player_data["team_played_for"] = abbreviation
			continue
		if col == "player_id":
			player_data["player_id"] = player_id
			continue

		column = validation.validate(performance_columns[col], input(f"Enter stat value - {col}: "), f"Enter stat value - {col}: ")
		player_data[col] = column

	return player_data, previously_selected_players



def add(connector, data: dict) -> None:
	df = DataFrame(data)
	df.to_sql('performance', connector.conn, if_exists="append", index=False)
	print("PERFORMANCE ADDED")