from fuzzywuzzy import process
import pandas as pd

def find_most_similar(item: str, options: list) -> tuple:
    result, score = process.extractOne(item, options)
    return result, score

def get_team_id(connector, team_name: str) -> str:
    try:
        team_name = team_name.replace("'", " ")

        # Fetch data from the database for comparison
        database_data = connector.get_list(f"SELECT id, name FROM team")

        team_names = [pair[1] for pair in database_data]
        best_match = find_most_similar(team_name, team_names)
    except Exception as e:
        raise RuntimeError(f"Error: {e}")
        return None

    if best_match:
        return [pair[0] for pair in database_data if pair[1] == best_match[0]][0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found

def get_player_id(connector, row) -> str:
    row.first_name = row.first_name.replace("'", " ")
    row.last_name = row.last_name.replace("'", " ")

    # Fetch data from the database for comparison
    database_data = connector.get_list(f"SELECT id, first_name, last_name, birth_date FROM player WHERE birth_date = '{row.birth_date}'")

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
    
def get_id_from_name(name: str, options: list) -> str:
    try:
        name = name.replace("'", " ")
        best_match, score = find_most_similar(name, options)

        if best_match and score >= 40:
            return best_match  # Assuming the first column is id
        elif best_match and score < 40:
            raise f"Error finding suitable matching name {name}, closest match {best_match} scored {score}" 
        else:
            raise f"Error - Unable to find matching name {name}"  # Handle the case where no result is found
    except Exception as e:
        raise e
    
def get_player_id_per_ninety(connector, row) -> str:
    try:
        row.first_name = row.first_name.replace("'", " ")
        row.last_name = row.last_name.replace("'", " ")
        database_data = connector.get_list("SELECT id, first_name, last_name FROM player")

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
    
        if matched_player and score >= 40:
            return matched_player[0]  # Assuming the first column is id
        elif matched_player and score < 40:
            raise f"Error finding suitable matching name for player {row.first_name} {row.last_name}, closest match {matched_player} scored {score}" 
        else:
            raise f"Error - Unable to find matching name for player {row.first_name} {row.last_name}"  # Handle the case where no result is found
    except Exception as e:
        raise RuntimeError(f"Error: {e}")
        return None
    


def get_referee_id(connector, referee_name: str) -> str:
    referee_name = referee_name.replace("'", " ")
    query = f"SELECT id FROM referee WHERE name = '{referee_name}'"
    result = connector.get_list(query)
    
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        print(query)
        return None  # Handle the case where no result is found
