
window.onload = async function load() {
	await fetch_team_data();
}

async function fetch_team_data() {
	const res = await fetch(`http://127.0.0.1:8080/teams`, {
		method: 'GET',
		credentials: 'include'
	})
	const data = await res.json()

	create_team_divs(data);
}

function create_team_divs(data) {
	const teamsContainer = document.getElementById('teamsContainer');
	data.forEach(team => {
		const teamDiv = document.createElement('div');
		teamDiv.className = 'card';
		teamDiv.id = `card-${team.id}`;

		// Create an image element for the team badge
		// const teamBadge = document.createElement('img');
		// teamBadge.src = team.badgeUrl;

		// Create a span element for the team name
		const teamNameDiv = document.createElement('div');
		const teamName = document.createElement('span');
		teamName.textContent = team.name;

		teamNameDiv.appendChild(teamName);
		// Append the badge and name elements to the team div
		// teamDiv.appendChild(teamBadge);
		teamDiv.appendChild(teamNameDiv);

		// Append the team div to the teams container
		teamsContainer.appendChild(teamDiv);
	});
}