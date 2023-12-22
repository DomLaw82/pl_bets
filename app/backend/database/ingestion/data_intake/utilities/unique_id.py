from fuzzywuzzy import process

def find_most_similar(player, options):
    result, score = process.extractOne(player, options)
    return result, score

def get_team_id(connector, team_name: str) -> str:
    team_name = team_name.replace("'", " ")

    # Fetch data from the database for comparison
    database_data = connector.get_list(f"SELECT id, name FROM team WHERE name = '{team_name}'")

    # Apply fuzzy matching to find the most similar team in the database
    matched_team = None
    score = 0
    for db_team in database_data:
        current_match = find_most_similar(team_name, [db_team[1]])
        if not current_match:
            continue
        if current_match[1] and current_match[1] > score:
            matched_team = db_team
            score = current_match[1]
    if matched_team:
        return matched_team[0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found
        
def get_team_id_from_player_team(connector, player_id: str, season: str) -> str:
    query = f"SELECT team_id FROM player_team WHERE player_id = '{player_id}' AND season = '{season}' ORDER BY season"
    result = connector.get_list(query)

    if len(result) > 1:
        return [row[0] for row in result]
    elif result:
        return result[0][0]  # Assuming the first column is id
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
    
def get_player_id_per_ninety(connector, row) -> str:
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
    if matched_player:
        return matched_player[0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found


def get_referee_id(connector, referee_name: str) -> str:
    referee_name = referee_name.replace("'", " ")
    query = f"SELECT id FROM referee WHERE name = '{referee_name}'"
    result = connector.get_list(query)
    
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        print(query)
        return None  # Handle the case where no result is found

def get_team_id(connector, team_name: str) -> str:
    query = f"SELECT id FROM team WHERE name = '{team_name}'"
    result = connector.get_list(query)
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found
def get_team_id_from_player_team(connector, player_id: str, season: str) -> str:
    query = f"SELECT team_id FROM player_team WHERE player_id = '{player_id}' AND season = '{season}' ORDDER BY season"
    result = connector.get_list(query)

    if len(result) > 1:
        return [row[0] for row in result]
    elif result:
        return result[0][0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found