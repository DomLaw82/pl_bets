window.onload = async function load() {
	await fetch_team_data();
}

async function fetch_team_data() {
	console.log('fetching team data: ',`${process.env.API_URL}/teams`);
	const res = await fetch(`${process.env.API_URL}/teams`, {
		method: 'GET',
		credentials: 'include'
	})
	const data = await res.json()
	
	console.log(data);
	create_team_divs(data);
}

function create_team_divs(data) {
	const teamsContainer = document.getElementById('teamsContainer');
	data.forEach(team => {
		const teamDiv = document.createElement('div');
		teamDiv.className = 'team';
		teamDiv.id = `team-${team.id}`;

		// Create an image element for the team badge
		// const teamBadge = document.createElement('img');
		// teamBadge.src = team.badgeUrl;

		// Create a span element for the team name
		const teamName = document.createElement('span');
		teamName.textContent = team.name;

		// Append the badge and name elements to the team div
		teamDiv.appendChild(teamBadge);
		teamDiv.appendChild(teamName);

		// Append the team div to the teams container
		teamsContainer.appendChild(teamDiv);
	});
}