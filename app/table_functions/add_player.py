from app.cli import cl_output
from utilities import unique_id, validation
from pandas import DataFrame


def collect(connector, **kwargs) -> None:
	print("\n++++++++++++++\n  Add player  \n++++++++++++++\n")

	team_id = kwargs.get("team_id")
	players = {}
	players_to_add = int(validation.validate("int", input(
		"How many players need to be added?: "), "How many players need to be added?: "))
	players_added = 0
	
	while players_to_add > players_added:
		player_id = unique_id.create_id("player", connector, players_added)
		first_name = validation.validate("text",
			input("\nPlayer first name/s: "), "Player first name/s: ").title()
		last_name = validation.validate("text",
			input("Player last name: "), "Player last name: ").title()
		birth_date = validation.get_valid_date_input(
			input("Player dob (YYYY-MM-DD): "), "Player dob (YYYY-MM-DD): ")
		team_id = team_id or validation.validate("text", input("Team id: "), "Team id: ").lower()
		season = validation.validate("season", input("Enter a season (YY/YY): "), "Enter a season (YY/YY): ")

		player = {
			"new_player": {
				"player_id": player_id,
				"team_id": team_id,
				"first_name": first_name,
				"last_name": last_name,
				"birth_date": birth_date,
				"season": season
			}
		}
		
		print("\n")
		cl_output.print_dict_table(player)
		confirm = validation.validate("yes_no", input("Confirm? (Y/N): "), "Confirm? (Y/N): ").upper()
		print("\n")
		if confirm == "Y":
			players[players_added] = player["new_player"]
			cl_output.print_dict_table(players)
			print("\n")
			players_added += 1
		else:
			continue

	return players


def add(connector, data: dict) -> None:
	for key in list(data.keys()):
		df = DataFrame(data[key])
		df[["player_id", "first_name", "last_name", "birth_date"]].to_sql('player', connector.conn, if_exists="append", index=False)
		df[["player_id", "team_id", "season"]].to_sql('player_team', connector.conn, if_exists="append", index=False)
	print("PLAYERS ADDED")