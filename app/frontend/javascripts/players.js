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
	
	const cols = ["id", "first_name", "last_name", "birth_date", "position", "team_name", "active"]

	headerDiv = document.createElement('div');
	headerDiv.className = 'card';
	headerDiv.id = 'header-card';

	cols.forEach(col => {
		const headerKeyDiv = document.createElement('div');
		headerKeyDiv.className = `card-element card-${col}`;
		const headerKeySpan = document.createElement('span');
		headerKeySpan.textContent = `${col}`;

		headerKeyDiv.appendChild(headerKeySpan);
		headerDiv.appendChild(headerKeyDiv);
	});
	playersContainer.appendChild(headerDiv);


	data.forEach(player => {
		const playerDiv = document.createElement('div');
		playerDiv.className = 'card';
		playerDiv.id = `${player.id}`;


		cols.forEach(col => {
			let value = player[col] || "";
			const playerKeyDiv = document.createElement('div');
			playerKeyDiv.className = `card-element card-${col}`;
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



