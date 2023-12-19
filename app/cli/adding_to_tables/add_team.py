from database.cli import cl_output
from database.utilities import validation
from database.table_functions import add_player
from pandas import DataFrame


def collect(connector) -> dict:
	print("""\n++++++++++++\n  Add team  \n++++++++++++\n""")
	abbreviations = connector.get_list("SELECT abbreviation FROM team")
	abbreviations = [abbr[0] for abbr in abbreviations]
	team_names = connector.get_list("SELECT team_name FROM team")
	team_names = [name[0] for name in team_names]
	
	abbreviation = validation.validate("length", input("Team 2 letter abbreviation: "), "Team 2 letter abbreviation: ", length=2)
	abbreviation = validation.validate("not_in_list", abbreviation, "Team 2 letter abbreviation: ", var_list=abbreviations)
	abbreviation = validation.validate("text", abbreviation, "Team 2 letter abbreviation: ").upper()
	
	team_name = input("Team full name: ")
	
	team_name = validation.validate("not_in_list", team_name, "Team full name: ", var_list=team_names)
	team_name = validation.validate("text", team_name, "Team full name: ").title()

	team = {
		"new_team": {
			"abbreviation": abbreviation,
			"team_name": team_name
		}
	}
	print("\n")
	cl_output.print_dict_table(team)
	confirm = validation.validate("yes_no", input("Confirm? (Y/N): "), "Confirm? (Y/N): ").upper()
	if confirm == 'N':
		return 'restart'


	add_players_flag = validation.validate("yes_no", input("\nAdd team players? (Y/N): "), "Add team players? (Y/N): ").upper()
	if add_players_flag == "Y":
		players = add_player.collect(connector, team_abbreviation=abbreviation)
		add_player.add(connector, players)
 
	return team["new_team"]


def add(connector, data: dict) -> None:
	df = DataFrame(data)
	df.to_sql('team', connector.conn, if_exists="append", index=False)
	print("TEAM ADDED")
