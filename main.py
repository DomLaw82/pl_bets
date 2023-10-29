from app.utilities import db_connector, unique_id, validation
from app.table_functions import add_match, add_performance, add_player, add_team, add_competition, add_country
from app.data_intake import squad_data, team_match_data
from app.cli import cl_output
import subprocess, os, sys

if __name__ == "__main__":

    os.chdir(sys.path[0])

    connector = db_connector.local_pl_stats_connector
    options = {
        "1": add_match,
        "2": add_performance,
        "3": add_player,
        "4": add_team,
        "5": add_country,
        "6": add_competition,
    }
    print(cl_output.intro)
    in_progress = True
    
    while in_progress:
        main_menu_option = validation.validate("int", input(cl_output.main_menu), "Select an option: ")
        if main_menu_option == "7":
            subprocess.run(["python", "data_intake/squad_data.py"])
        elif main_menu_option == "8":
            subprocess.run(["python", "data_intake/team_match_data.py"])
        elif main_menu_option == '9':
            break
        data_to_add = options[main_menu_option].collect(connector)
        if data_to_add == 'restart':
            continue
        options[main_menu_option].add(connector, data_to_add)