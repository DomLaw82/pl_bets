id_specs = {
    "match": {
        "length": 6,
        "prefix": "m-"
    },
    "team": {
        "length": 3,
        "prefix": "t-"
    },
    "player": {
        "length": 5,
        "prefix": "p-"
    },
    "country": {
        "length": 3,
        "prefix": "c-"
    },
    "competition" : {
        "length": 2,
        "prefix": "x-"
    },
    "referee" : {
        "length": 5,
        "prefix": "r-"
    },
}

def create_id(id_type: str, connector, offset: int = 0) -> str:
    highest_id = connector.get_list(f"SELECT MAX(id) from {id_type}")[0][0] or 0
    new_id = str(int(highest_id.split('-')[1]) + offset + 1) if highest_id else str(highest_id + offset + 1)
    while len(new_id) < id_specs[id_type]["length"]:
        new_id = '0' + new_id
    new_id = id_specs[id_type]["prefix"] + new_id
    return new_id

def get_team_id(connector, team_name: str) -> str:
    query = f"SELECT id FROM team WHERE name = '{team_name}'"
    result = connector.get_list(query)
    
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        return None  # Handle the case where no result is found

def convert_team_name_to_team_id(connector, team_name:str) -> str:
	return connector.get_list(f"SELECT id FROM team WHERE name = '{team_name}'")[0][0]

def get_player_id(connector, row) -> str:
	row.first_name = row.first_name.replace("'", "''")
	row.last_name = row.last_name.replace("'", "''")
	return connector.get_list(f"SELECT id FROM player WHERE first_name = '{row.first_name}' AND last_name = '{row.last_name}' AND birth_date = '{row.birth_date}'")[0][0]


def get_referee_id(connector, referee_name: str) -> str:
    referee_name = referee_name.replace("''", "''''")
    query = f"SELECT id FROM referee WHERE name = '{referee_name}'"
    result = connector.get_list(query)
    
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        print(query)
        return None  # Handle the case where no result is found