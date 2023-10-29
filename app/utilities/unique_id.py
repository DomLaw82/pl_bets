# Match ID
# m-xxxxxx
def create_match_id(connector, row_number: int = 0) -> str:
    highest_id = connector.get_list("SELECT MAX(id) from match")[0][0] or 0
    new_id = str(int(highest_id.split('-')[1]) + row_number + 1) if highest_id else str(highest_id + row_number + 1)
    while len(new_id) < 6:
        new_id = '0' + new_id
    new_id = "m-" + new_id
    return new_id

# Team ID
# t-xxx
def create_team_id(connector, team:int, row_number: int = 0) -> str:
    highest_id : str = connector.get_list("SELECT MAX(id) from team")[0][0] or 0
    new_id = str(int(highest_id.split('-')[1]) + row_number + 1) if highest_id else str(highest_id + row_number + 1)
    while len(new_id) < 3:
        new_id = '0' + new_id
    new_id = "t-" + new_id
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

# Player ID
# p-xxxxx
def create_player_id(connector, **kwargs) -> str:
    offset = kwargs.get("offset") or 0

    highest_id = connector.get_list("SELECT MAX(id) from player")[0][0]
    if not highest_id:
        highest_id = "p-00000"
    new_id = str(int(highest_id.split("-")[1]) + 1 + int(offset))
    while len(new_id) < 5:
        new_id = '0' + new_id
    new_id = "p-" + new_id
    return new_id

def get_player_id(connector, row) -> str:
	row.first_name = row.first_name.replace("'", "''")
	row.last_name = row.last_name.replace("'", "''")
	return connector.get_list(f"SELECT id FROM player WHERE first_name = '{row.first_name}' AND last_name = '{row.last_name}' AND birth_date = '{row.birth_date}'")[0][0]

# Country ID
# c-xxx
def create_country_id(connector) -> str:
    highest_id = connector.get_list("SELECT MAX(id) from country")[0][0]
    if not highest_id:
        highest_id = 0
    new_id = str(int(highest_id) + 1)
    while len(new_id) < 3:
        new_id = '0' + new_id
    return new_id

def create_competition_id(connector) -> str:
    highest_id = connector.get_list("SELECT MAX(id) from competition")[0][0]
    if not highest_id:
        highest_id = 0
    new_id = str(int(highest_id) + 1)
    while len(new_id) < 3:
        new_id = '0' + new_id
    return new_id

# Referee ID
# r-xxxx
def create_referee_id(connector, row_number:int) -> str:
    highest_id = connector.get_list("SELECT MAX(id) from referee")[0][0] or 0
    new_id = str(int(highest_id.split('-')[1]) + row_number + 1) if highest_id else str(highest_id + row_number + 1)
    while len(new_id) < 4:
        new_id = '0' + new_id
    new_id = "r-" + new_id
    return new_id

def get_referee_id(connector, referee_name: str) -> str:
    referee_name = referee_name.replace("''", "''''")
    query = f"SELECT id FROM referee WHERE name = '{referee_name}'"
    result = connector.get_list(query)
    
    if result:
        return result[0][0]  # Assuming the first column is id
    else:
        print(query)
        return None  # Handle the case where no result is found