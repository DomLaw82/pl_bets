window.onload = async function load() {
	await fetchTeamData();
}


async function fetchTeamData() {
	const res = await fetch(`http://localhost:8080/active-teams`, {
		method: 'GET',
		credentials: 'include'
	})
	const data = await res.json()
	homeTeamSelectId = 'home-team';
	awayTeamSelectId = 'away-team';

	createTeamOptions(homeTeamSelectId, data);
	createTeamOptions(awayTeamSelectId, data);
}
function createTeamOptions(elementId, data) {
	const teamSelect = document.getElementById(elementId);
	data.forEach(team => {
		const teamOption = document.createElement('option');
		teamOption.value = team.id;
		teamOption.id = team.id;
		teamOption.textContent = team.name;
		teamSelect.appendChild(teamOption);
	});
}


async function updatePlayerCards(selectId, playerCardContainerId) {
	const team = document.getElementById(selectId).value
	await fetchPlayerData(playerCardContainerId, team);
}
async function fetchPlayerData(playerCardContainerId, team_name) {
	
	const res = await fetch(`http://localhost:8080/active-players/${team_name}`, {
		method: 'GET',
		credentials: 'include'
	})
	const data = await res.json()

	const keyOrderList = ["id", "first_name", "last_name"]
	
	attachCards(playerCardContainerId, data, keyOrderList)
}

function attachCards(playerCardContainerId, data, keyOrderList) {
	const playerCardsContainer = document.getElementById(playerCardContainerId);

	data.forEach(player => {
		const playerCard = createPlayerCard(player, keyOrderList);
		playerCardsContainer.appendChild(playerCard);
	});

}
function createPlayerCard(playerData, keyOrder) {

	const card = document.createElement('div');
	card.classList.add('player-card');
	card.classList.add('card');
	
	keyOrder.forEach(key => {
		const cardElement = document.createElement('div');
		cardElement.classList.add('card-element');
		cardElement.textContent = `${playerData[key]}`;
		card.appendChild(cardElement);
	});

	let isActive = false;

	card.addEventListener('click', function() {
		let isHome = card.parentElement.id == 'home-player-cards' ? true : false;
		let isMax = moveSelectedPlayers(playerData["first_name"], playerData["last_name"], playerData["id"], isActive, isHome)

		if (!isMax) {
			isActive = !isActive;
			card.classList.toggle('active', isActive)
		}
	});


	return card;
}

function getSelectedPlayers(selectedPlayersListId) {
	const selectedPlayersList = document.getElementById(selectedPlayersListId);
	const selectedPlayers = [];

	for (let i = 0; i < selectedPlayersList.childElementCount; i++) {
		selectedPlayers.push(selectedPlayersList.children[i].id);
	}
	return selectedPlayers;
}

async function runPrediction() {

	const homeTeamId = document.getElementById('home-team').value;
	const homePlayersSelected = getSelectedPlayers('home-selected-players-list');
	awayTeamId = document.getElementById('away-team').value;
	awayPlayersSelected = getSelectedPlayers('away-selected-players-list');
	
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

			const resultsDiv = document.getElementById('prediction-results');
			const overlay = document.getElementById('pop-up-background');

			resultsDiv.style.display = 'block';
			overlay.style.display = 'block';

			document.addEventListener('click', function(event) {
				if ( event.target.id == 'pop-up-background' ) {
					resultsDiv.style.display = 'none';
					overlay.style.display = 'none';
				}
			});
		});
	
}

function rebuildModel() {
	modelPopUp = document.getElementById('model-pop-up')
	div = document.createElement('div');
	div.className = 'model-pop-up-content';
	div.innerHTML = '<p>Rebuilding model...</p>';
	modelPopUp.style.display = 'block';
}

function retuneAndRebuildModel() {
	modelPopUp = document.getElementById('model-pop-up')
	modelPopUp.style.display = 'block';
}

function moveSelectedPlayers(firstName, lastName, id, active, isHome) {
	const selectedPlayersList = isHome ? document.getElementById('home-selected-players-list') : document.getElementById('away-selected-players-list');
	
	const numberOfListElements = selectedPlayersList.childElementCount;

	if (numberOfListElements >= 20 && !active) {
		createWarningPopUp("You can only select up to 20 players.-Please deselect a player before selecting another.");
		return true;
	}

	if (!active) {
		const listElement = document.createElement('li');
		listElement.id = id;
		listElement.textContent = `${firstName} ${lastName}`;

		selectedPlayersList.appendChild(listElement);
	} else {
		const listElement = document.getElementById(id);
		selectedPlayersList.removeChild(listElement);
	}
	return false;
	
};

function createWarningPopUp(message) {
	const popUpBackground = document.getElementById('pop-up-background');
	const warningPopUp = document.getElementById('warning-pop-up');
	const warningPopUpContent = document.getElementById('warning-pop-up-content');

	warningPopUpContent.innerHTML = message;

	warningPopUp.style.display = 'block';
	popUpBackground.style.display = 'block';

	document.addEventListener('click', function(event) {
		if ( event.target.id == 'pop-up-background' ) {
			warningPopUp.style.display = 'none';
			popUpBackground.style.display = 'none';
		}
	});
}