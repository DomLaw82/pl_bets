window.onload = async function load() {
	await fetch_player_data();
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
		playerDiv.className = 'player';
		playerDiv.id = `player-${player.id}`;

		Object.keys(player).forEach(key => {
			const playerKeyDiv = document.createElement('div');
			playerKeyDiv.className = `player-${key}`;
			const playerKeySpan = document.createElement('span');
			playerKeySpan.textContent = `${key}: ${player[key]}`;

			playerKeyDiv.appendChild(playerKeySpan);
			playerDiv.appendChild(playerKeyDiv);
		});

		playersContainer.appendChild(playerDiv);
	});
}