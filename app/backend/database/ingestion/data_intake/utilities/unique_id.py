from rapidfuzz import process, fuzz, utils
from db_connection import SQLConnection
import pandas as pd
from app_logger import FluentLogger

log_class = FluentLogger("unique-id")
logger = log_class.get_logger()

def find_most_similar(item: str, options: list) -> tuple[str, float, int]:
    result, score, index = process.extractOne(item, options, processor=utils.default_process) or (None, 0, 0)
    return result, score, index

def get_player_id(connector, row) -> str:
    row.first_name = row.first_name.replace("'", " ")
    row.last_name = row.last_name.replace("'", " ")

    # Fetch data from the database for comparison
    database_data = connector.get_list(f"SELECT id, first_name, last_name, birth_year FROM player WHERE birth_year = '{row.birth_year}'")

    # Apply fuzzy matching to find the most similar player in the database
    matched_player = None
    score = 0
    for db_player in database_data:
        db_full_name = f"{db_player[1]} {db_player[2]}"
        current_match = find_most_similar(f"{row.first_name} {row.last_name}", [db_full_name])
        if not current_match:
            continue
        if current_match[1] and current_match[1] > score:
            matched_player = db_player
            score = current_match[1]

    if matched_player:
        return matched_player[0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found
    
def get_id_from_name(db_connector: SQLConnection, name: str, table: str) -> str:
    """Function to get the id of a name from the database."""
    try:
        name = name.replace("'", " ")
        query_options = {
            "team": "SELECT id, name FROM team",
            "competition": "SELECT id, name FROM competition",
            "player": "SELECT id, first_name || ' ' || last_name as name FROM player",
            "referee": "SELECT id, name FROM referee",
            "country": "SELECT id, name FROM country"
        }
        name_dict = {
            "team": {
                "Wolves": "Wolverhampton Wanderers",
                "Spurs": "Tottenham Hotspur",
                "Man City": "Manchester City",
                "Man United": "Manchester United",
            },
            "competition": {},
            "player": {
                # "Danny Williams": "Daniel Williams",
                # "Bruno": "Bruno Saltor",
                # "Tom Ince": "Thomas Ince",
                # "Matty James": "Matthew James",
                # "Allan Nyom": "Allan-Roméo Nyom",
                # "Jazz Richards": "Ashley Richards",
                # "Jon Rowe": "Jonathan Rowe",
                # "Andrew Moran": "Andy Moran",
                # "Joshua Acheampong": "Josh-Kofi Acheampong",
            },
            "referee": {}
        }
        query = query_options.get(table)
        if not query:
            logger.error(f"Invalid table name '{table}' when looking for ids")
            raise Exception(f"Invalid table name '{table}' when looking for ids")
        
        name = name_dict.get(table).get(name) or name
        
        database_data = db_connector.get_df(query)
        best_match, score, index = find_most_similar(name, database_data["name"].tolist())

        if best_match and score >= 70:
            if score < 95:
                logger.debug(f"Found matching name {name} with {best_match} scoring {score}")
            return database_data[database_data["name"] == best_match]["id"].values[0]
        elif best_match and 50 < score < 70:
            logger.error(f"""
                Error finding suitable matching name {name}, closest match {best_match} scored {score}\n
                Other possible matches: {process.extract(name, database_data['name'].tolist(), limit=5)}
            """)
        else:
            # Handle the case where no result is found
            logger.error(f"Unable to find matching name for {name}")
            raise Exception(f"Unable to find matching name for {name}") 
        return None
    except Exception as e:
        logger.error(f"Error getting id from name - line {e.__traceback__.tb_lineno} - {e}")
        raise Exception(e)

def get_name_from_database(db_connector: SQLConnection, name: str, table: str) -> str:
    """Function to match a name to one from the database"""
    try:
        query_options = {
            "team": "SELECT id, name FROM team",
            "competition": "SELECT id, name FROM competition",
            "player": "SELECT id, first_name || ' ' || last_name as name FROM player",
            "referee": "SELECT id, name FROM referee",
            "country": "SELECT id, name FROM country"
        }
        query = query_options.get(table)
        if not query:
            raise Exception(f"Invalid table name '{table}' when looking for names")
        
        name_dict = {
            "team": {
                "Wolves": "Wolverhampton Wanderers",
                "Spurs": "Tottenham Hotspur",
                "Man City": "Manchester City",
                "Man United": "Manchester United",
            },
            "competition": {},
            "player": {
                # "Danny Williams": "Daniel Williams",
                # "Bruno": "Bruno Saltor",
                # "Tom Ince": "Thomas Ince",
                # "Matty James": "Matthew James",
                # "Allan Nyom": "Allan-Roméo Nyom",
                # "Jazz Richards": "Ashley Richards",
                # "Jon Rowe": "Jonathan Rowe",
                # "Andrew Moran": "Andy Moran",
                # "Joshua Acheampong": "Josh-Kofi Acheampong",
            },
            "referee": {}
        }
        edited_name = name_dict.get(table).get(name)
        if edited_name:
            name = edited_name
        
        database_data = db_connector.get_df(query)
        best_match, score, index = find_most_similar(name, database_data["name"].tolist())
        if best_match and score >= 70:
            if score < 95:
                logger.debug(f"Found matching name {name} with {best_match} scoring {score}")
            return best_match
        elif best_match and 50 < score < 70:
            logger.warning(f"""
                Issue finding suitable matching name {name}, closest match {best_match} scored {score}\n
                Possible matches: {process.extract(name, database_data['name'].tolist(), limit=5)}
            """)
            return best_match
        else:
            # Handle the case where no result is found
            logger.error(f"Unable to find matching name for {name}")
            return None 
    except Exception as e:
        logger.error(f"Error getting name from database - line {e.__traceback__.tb_lineno} - {e}")
        raise e