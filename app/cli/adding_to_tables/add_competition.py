from database.cli import cl_output
from database.utilities import unique_id, validation
from database.table_functions import add_performance
from pandas import DataFrame

def collect(connector) -> None:
	print("""\n+++++++++++++++++++\n  Add competition  \n+++++++++++++++++++\n""")

	countries = connector.get_dict(f"SELECT id, name FROM country;")
	countries_ids = [country['id'] for country in countries.values()]
	competition_names = connector.get_list(f"SELECT name FROM competition;")
	competition_names = [comp[0] for comp in competition_names]
	cl_output.print_dict_table(countries)
	print("\n")

	country_id = unique_id.create_id("country", connector)
	# TODO - Select competition(league) for match

	country_id = validation.validate("in_list", input("\nWhat country is this competition in by id: "), "What country is this competition in by id: ", var_list=countries_ids)
	country_id = validation.validate("int", country_id, "What country is this competition in by id: ")

	competition_name = validation.validate("text", input("\nCompetition name: ").title(), f"Competition name: ")
	competition_name = validation.validate("not_in_list", competition_name.title(), "Competition name: ", var_list=competition_names)

	return {
		"id": country_id,
		"country_id": country_id,
		"name": competition_name,
	}

def add(connector, data) -> None:
	df = DataFrame(data)
	df.to_sql("competition", connector.conn, if_exists="append", index=False)
	print("COMPETITION ADDED")