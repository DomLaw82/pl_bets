from app.cli import cl_output
from utilities import unique_id, validation
from app.table_functions import add_performance
from pandas import DataFrame

def collect(connector) -> None:
	print("""\n+++++++++++++++\n  Add country  \n+++++++++++++++\n""")

	countries: dict = connector.get_dict(f"SELECT id, name FROM country;")
	countries_list = [country['name'] for country in countries.values()]
	cl_output.print_dict_table(countries)
	print("\n")

	country_id = unique_id.create_id("country", connector)
	# TODO - Select competition(league) for match

	country = validation.validate("not_in_list", input("Country name: ").title(), "Country name: ", var_list=countries_list)
	country = validation.validate("text", country, "What country would you like to add: ").title()

	return {
		"id": country_id,
		"name": country,
	}

def add(connector, data) -> None:
	df = DataFrame(data)
	df.to_sql("country", connector.conn, if_exists="append", index=False)
	print("COUNTRY ADDED")