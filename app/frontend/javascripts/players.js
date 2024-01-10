window.onload = async function load() {
	await fetch_player_data();

	// document.getElementById('submit-button').addEventListener('click', handleSearchSubmit);
}

async function fetch_player_data() {
	const res = await fetch(`http://127.0.0.1:8080/players`, {
		method: 'GET',
		credentials: 'include'
	})
	const data = await res.json()

	create_player_divs(data);
}

function create_player_divs(data) {
	const playersContainer = document.getElementById('playersContainer');
	data.forEach(player => {
		const playerDiv = document.createElement('div');
		playerDiv.className = 'player-card';
		playerDiv.id = `${player.id}`;

		let cols = ["id", "first_name", "last_name", "birth_date", "position", "team_name", "active"]

		cols.forEach(col => {
			let value = player[col] || "";
			const playerKeyDiv = document.createElement('div');
			playerKeyDiv.className = `player-card-element player-card-${col}`;
			const playerKeySpan = document.createElement('span');
			playerKeySpan.textContent = `${value}`;

			playerKeyDiv.appendChild(playerKeySpan);
			playerDiv.appendChild(playerKeyDiv);
		});

		playersContainer.appendChild(playerDiv);
	});
}

function handleSearchSubmit() {
	const searchInput = document.getElementById('player-search-box');
	const searchTerm = searchInput.value;

	fetch(`http://example.com/search?term=${searchTerm}`, {
		method: 'GET',
		credentials: 'include'
	})
		.then(res => res.json())
		.then(data => {
			// Process the fetched data
			console.log(data);
		})
		.catch(error => {
			// Handle any errors
			console.error(error);
		});
}


function showPopUp(popUpID, buttonID) {
	const popUp = document.getElementById(popUpID);
	const button = document.getElementById(buttonID);

	// Show the filter pop-up
	popUp.style.display = 'block';

	document.addEventListener('click', function(event) {
		// Check if the clicked element is outside the filter pop-up
		if (!popUp.contains(event.target) && !button.contains(event.target)) {
			// Hide the filter pop-up
			popUp.style.display = 'none';
		}
	});
}
