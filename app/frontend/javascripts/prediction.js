window.onload = async function load() {
	await fetch_team_data();
}


async function fetch_team_data() {
	const res = await fetch(`http://localhost:8080/active-teams`, {
		method: 'GET',
		credentials: 'include'
	})
	const data = await res.json()
	homeTeamSelectId = 'home-team';
	awayTeamSelectId = 'away-team';

	create_team_options(homeTeamSelectId, data);
	create_team_options(awayTeamSelectId, data);
}
function create_team_options(elementId, data) {
	const teamSelect = document.getElementById(elementId);
	data.forEach(team => {
		const teamOption = document.createElement('option');
		teamOption.value = team.name;
		teamOption.textContent = team.name;
		teamSelect.appendChild(teamOption);
	});
}


async function update_player_dropdowns(selectId, playerSelectId) {
	const team = document.getElementById(selectId).value
	await fetch_player_data(playerSelectId, team);
}
async function fetch_player_data(playerSelectId, team_name) {
	
	const res = await fetch(`http://localhost:8080/active-players/${team_name}`, {
		method: 'GET',
		credentials: 'include'
	})
	const data = await res.json()
	
	create_player_options(playerSelectId, data)
	create_player_options(playerSelectId, data)
}
function create_player_options(playerSelectId, data) {
	const playerSelect = document.getElementById(playerSelectId);
	playerSelect.innerHTML = '';
	playerSelect.innerHTML = '<option value="" disabled selected>Select a player</option>';
	data.forEach(player => {
		const playerOption = document.createElement('option');
		playerOption.value = `${player.first_name} ${player.last_name}`;
		playerOption.textContent = `${player.first_name} ${player.last_name}`;
		playerSelect.appendChild(playerOption);
	});
}
function updateSelectedPlayerList(selectId, playerListId) {
	const playersSelectOptions = document.getElementById(selectId).childNodes;
	const playerList = document.getElementById(playerListId);
	
	const playersSelected = [];
	playersSelectOptions.forEach(option => {
		if (option.selected) {
			playersSelected.push(option.value);
		}
	});
	playerList.innerHTML = '';
	playersSelected.forEach(player => {
		const playerListItem = document.createElement('li');
		playerListItem.textContent = player;
		playerList.appendChild(playerListItem);
	});
}