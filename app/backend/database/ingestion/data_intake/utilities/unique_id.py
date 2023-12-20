def get_team_id(connector, team_name: str) -> str:
    query = f"SELECT id FROM team WHERE name = '{team_name}'"
    result = connector.get_list(query)
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found

def get_player_id(connector, row) -> str:
    row.first_name = row.first_name.replace("'", " ")
    row.last_name = row.last_name.replace("'", " ")
    result = connector.get_list(f"SELECT id FROM player WHERE lower(first_name) = '{row.first_name.strip().lower()}' AND lower(last_name) = '{row.last_name.strip().lower()}' AND birth_date = '{row.birth_date}'")
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found
def get_player_id_per_ninety(connector, row) -> str:
    row.first_name = row.first_name.replace("'", " ")
    row.last_name = row.last_name.replace("'", " ")
    result = connector.get_list(f"SELECT id FROM player WHERE lower(first_name) = '{row.first_name.strip().lower()}' AND lower(last_name) = '{row.last_name.strip().lower()}'")

    if result:
        return result[0][0]  # Assuming the first column is id
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