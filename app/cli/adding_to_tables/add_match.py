from database.cli import cl_output
from database.utilities import unique_id, validation
from database.table_functions import add_performance
from pandas import DataFrame

def collect(connector) -> None:
	print("""\n+++++++++++++\n  Add match  \n+++++++++++++\n""")

	match_facts = {}

	match_id = unique_id.create_id("match", connector)
	match_facts['match_id'] = match_id

	competitions = connector.get_dict(f"SELECT id, name FROM competition")
	competition_ids = [competition['id'] for competition in competitions.values()]
	cl_output.print_dict_table(competitions)
	
	selected_competition = validation.validate("in_list", input("\nSelect competition by id: "), "Select competition by id: ", var_list=competition_ids)
	selected_competition = validation.validate("int", selected_competition, "Select competition by id: ")
	match_facts["competition_id"] = selected_competition

	referees = connector.get_dict(f"SELECT id, name FROM referee")
	referee_ids = [ref['id'] for ref in referees.values()]
	cl_output.print_dict_table(referees)

	selected_ref = validation.validate("in_list", input("\nSelect referee by id: "), "Select referee by id: ", var_list=referee_ids)
	selected_ref = validation.validate("id", selected_ref, "Select referee by id: ")
	match_facts["referee_id"] = selected_ref

	match_length = int(validation.validate("int", input("Match length in minutes: "), "Match length in minutes: "))
	match_facts['match_length'] = match_length

	season = validation.validate("season", input("Season (YY/YY): "), "Season (YY/YY): ")
	match_facts['season'] = season

	selected_teams = []

	for location in ('HOME', 'AWAY'):

		teams = connector.get_dict(f"SELECT id, name FROM team ORDER BY id")
		team_ids = [team['id'] for team in teams.values()]
		cl_output.print_dict_table(teams)

		team_id = validation.validate("in_list", input(f"\nSelect {location} team id: ").lower(), f"Select {location} team id: ", var_list=team_ids)
		team_id = validation.validate("not_in_list", team_id, f"Select {location} team id: ", var_list=selected_teams)
		team_id = validation.validate("text", team_id, f"Select {location} team id: ").lower()
		match_facts[f"{location.lower()}_team_id"] = team_id
		selected_teams.append(team_id)

		number_of_players = int(validation.validate("int", input(f"How many players played for the {location} team?: "), f"How many players played for the {location} team?: "))
		
		team_performance = {}

		previously_selected_players = []

		# Team goals
		goals = int(validation.validate("int", input(f"{location.title()} goals: "), f"{location.title()} goals: "))
		match_facts[f"{location.lower()}_goals"] = goals
		# shots
		shots = int(validation.validate("int", input(f"{location.title()} shots: "), f"{location.title()} shots: "))
		match_facts[f"{location.lower()}_shots"] = shots
		# shots_on_target
		shots_on_target = int(validation.validate("int", input(f"{location.title()} shots on target: "), f"{location.title()} shots on target: "))
		match_facts[f"{location.lower()}_shots_on_target"] = shots_on_target
		# Team corners
		corners = int(validation.validate("int", input(f"{location.title()} corners: "), f"{location.title()} corners: "))
		match_facts[f"{location.lower()}_corners"] = corners
		# fouls
		fouls = int(validation.validate("int", input(f"{location.title()} fouls: "), f"{location.title()} fouls: "))
		match_facts[f"{location.lower()}_fouls"] = fouls
		# yellow_cards
		yellow_cards = int(validation.validate("int", input(f"{location.title()} yellow cards: "), f"{location.title()} yellow cards: "))
		match_facts[f"{location.lower()}_yellow_cards"] = yellow_cards
		# red_cards
		red_cards = int(validation.validate("int", input(f"{location.title()} red cards: "), f"{location.title()} red cards: "))
		match_facts[f"{location.lower()}_red_cards"] = red_cards
		
		# possession = int(validation.validate("int", input(f"{location.title()} possession %: "), f"{location.title()} possession %: "))
		# match_facts[f"{location.lower()}_possession"] = possession
		
		for player in range(number_of_players):
			player_data, previously_selected_players = add_performance.collect(connector, location=location, team_id=team_id, match_id=match_id, previously_selected_players=previously_selected_players)
			add_performance.add(connector, player_data)
			team_performance[player] = player_data
			cl_output.print_dict_table(team_performance)

	return match_facts 

def add(connector, data: dict) -> None:
	df = DataFrame(data)
	df.to_sql('match', connector.conn, if_exists="append", index=False)
	print("MATCH ADDED")