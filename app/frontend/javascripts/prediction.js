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
		teamOption.value = team.id;
		teamOption.id = team.id;
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

function getSelectedPlayers(selectId) {
	const playersSelectOptions = document.getElementById(selectId).childNodes;
	
	const playersSelected = [];
	playersSelectOptions.forEach(option => {
		if (option.selected) {
			playersSelected.push(option.value);
		}
	});
	return playersSelected;
}

function updateSelectedPlayerList(selectId, playerListId) {
	playersSelected = getSelectedPlayers(selectId);
	const playerList = document.getElementById(playerListId);

	playerList.innerHTML = '';
	playersSelected.forEach(player => {
		const playerListItem = document.createElement('li');
		playerListItem.textContent = player;
		playerList.appendChild(playerListItem);
	});
}

async function runPrediction() {

	homeTeamId = document.getElementById('home-team').value;
	homePlayersSelected = getSelectedPlayers('home-players');
	awayTeamId = document.getElementById('away-team').value;
	awayPlayersSelected = getSelectedPlayers('away-players');
	
	await fetch(`http://localhost:8008/predict`, {
		method: 'POST',
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			homeTeamId: homeTeamId,
			homePlayers: homePlayersSelected,
			awayTeamId: awayTeamId,
			awayPlayers: awayPlayersSelected
		})
	})
		.then(res => res.json())
		.then((data) => {
			
			const predictionContainer = document.getElementById('prediction-results-table');
			
			predictionContainer.innerHTML = '';
			const predictionTableLocationHeader = document.createElement('tr');
			const predictionTableStatsHeader = document.createElement('tr');
			const predictionTableRow = document.createElement('tr');

			const stats = ["goals", "shots", "shots_on_target", "corners", "fouls", "yellow_cards", "red_cards"]
			const locations = ["home", "away"];
			
			stats.forEach(stat => {
				const predictionTableStatsHeaderData = document.createElement('th');
				predictionTableStatsHeaderData.className = 'prediction-results-header prediction-result';
				predictionTableStatsHeaderData.textContent = stat;
				predictionTableStatsHeaderData.colSpan = 2;

				predictionTableStatsHeader.appendChild(predictionTableStatsHeaderData);

				locations.forEach(loc => {
					const predictionTableLocationHeaderData = document.createElement('th');
					predictionTableLocationHeaderData.className = 'prediction-results-header prediction-result';
					predictionTableLocationHeaderData.textContent = loc;

					const predictionTableData = document.createElement('td');
					predictionTableData.className = 'prediction-results-data prediction-result';
					predictionTableData.id = stat;
					predictionTableData.textContent = data[loc+"_"+stat];
		
					predictionTableLocationHeader.appendChild(predictionTableLocationHeaderData);
					predictionTableRow.appendChild(predictionTableData);
				});
			});
			
			predictionContainer.appendChild(predictionTableStatsHeader);
			predictionContainer.appendChild(predictionTableLocationHeader);
			predictionContainer.appendChild(predictionTableRow);

			document.getElementById('prediction-results').style.display = 'flex';
		});
	
}

