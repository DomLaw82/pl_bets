window.onload = async function () {
	await createSeasonButtons();
	
	const thisForm = document.getElementById('add-result-form');
	thisForm.addEventListener('submit', async function (e) {
		e.preventDefault();
		const formData = new FormData(thisForm).entries()
		const response = await fetch('http://localhost:8080/matches/add-result', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(Object.fromEntries(formData))
		});
	
		const result = await response.json();
		console.log(result)
	});
};

async function createSeasonButtons() {
	fetch('http://localhost:8080/matches/all-seasons')
		.then(response => response.json())
		.then(seasons => {
			const buttonContainer = document.getElementById('seasons');
			seasons.forEach(season => {
				const button = document.createElement('button');
				button.className = 'match-season';
				button.id = "season-"+season;
				button.innerText = season;
				button.onclick = function() {
					fetchMatches(season);
				};
				buttonContainer.appendChild(button);
			});
		})
		.catch(error => {
			console.error('Error:', error);
		});
}
	
async function fetchMatches(season) {
    try {
        const matches = await getMatches(season);
		clearMatches();
		allocateMatches(matches);
        showMatches();
    } catch (error) {
        console.error('Error:', error);
    }
}

// Fetch matches from the API
async function getMatches(season) {
    const response = await fetch(`http://localhost:8080/matches/season/${season}`);
    const matches = await response.json();
    return matches;
}

// Clear the existing content of past and upcoming matches
function clearMatches() {
    const pastMatches = document.getElementById('past-matches');
    const upcomingMatches = document.getElementById('upcoming-matches');
    pastMatches.innerHTML = '';
    upcomingMatches.innerHTML = '';
}

function allocateMatches(matches) {
	const pastMatchesDiv = document.getElementById('past-matches');
	const upcomingMatchesDiv = document.getElementById('upcoming-matches');

	matches.forEach(match => {
		if (match.result != "-") {
			pastMatchesDiv.appendChild(createMatchContainer(match));
		} else {
			upcomingMatchesDiv.appendChild(createMatchContainer(match));
		}
	});
}

function createMatchContainer(match) {
	const matchContainer = document.createElement('div');
    matchContainer.className = 'single-match-container';
	
    const matchGameWeek = createMatchElement('div', 'match-game-week', match.game_week);
    const matchDate = createMatchElement('div', 'match-date', match.date);
    const homeTeam = createMatchElement('div', 'match-home-team', match.home_team);
    const awayTeam = createMatchElement('div', 'match-away-team', match.away_team);
	const matchResult = createMatchElement('div', 'match-result', match.result);
	
    matchContainer.appendChild(matchDate);
    matchContainer.appendChild(matchGameWeek);
    matchContainer.appendChild(homeTeam);
    matchContainer.appendChild(awayTeam);
	matchContainer.appendChild(matchResult);
	
	if (match.result == "-") {
		const addResultButton = createMatchElement('button', 'add-result-button', 'Add Result');
		addResultButton.onclick = function () {
			addResult(match.game_week, match.date, match.home_team, match.away_team, match.competition_id);
		}
		matchContainer.appendChild(addResultButton);
	}
	
    return matchContainer;
}

// Helper function to create a match element
function createMatchElement(elementType, className, content) {
	const matchElement = document.createElement(elementType);
    matchElement.className = className;
	matchElement.innerText = content;
    return matchElement;
}

// Show the matches on the webpage
function showMatches() {
	const pastSchedule = document.getElementById('past-matches');
	const upcomingSchedule = document.getElementById('upcoming-matches');

	const pastContainer = document.getElementById('past-container');
	const futureContainer = document.getElementById('future-container');

	if (pastSchedule.children.length > 0) {
		pastContainer.style.display = 'flex';
	}
	if (pastSchedule.children.length == 0) {
		futureContainer.style.display = 'none';
	}

	if (upcomingSchedule.children.length > 0) {
		futureContainer.style.display = 'flex';
	}
	if (upcomingSchedule.children.length == 0) {
		futureContainer.style.display = 'none';
	}
};

function addResult(gameWeekValue, date, homeTeamName, awayTeamName, competitionIdValue) {
	const homeTeam = document.getElementById('add-result-home-team')
	const awayTeam = document.getElementById('add-result-away-team')
	const matchDate = document.getElementById('add-result-match-date')
	const gameWeek = document.getElementById('add-result-game-week')
	const competitionId = document.getElementById('add-result-competition-id')
	const resultPopup = document.getElementById('add-result-popup')

	let onlyDate = date.split(' ')[0]+"T"+date.split(' ')[1];

	homeTeam.value = homeTeamName;
	awayTeam.value = awayTeamName;
	matchDate.value = onlyDate;
	gameWeek.value = gameWeekValue;
	competitionId.value = competitionIdValue;

	resultPopup.style.display = 'block';

	document.addEventListener('click', function(event) {
		if ((!resultPopup.contains(event.target) && !event.target.className.includes('add-result-button')) || event.target.className.includes('submission')) {
			resultPopup.style.display = 'none';
		}
	});
}

function showMatchFacts(flag) {
	if (flag) {
		document.getElementById('match-facts').style.display = 'block';
		document.getElementById('add-match-facts-button-close').style.display = 'block';
		requiredMatchFactsFields(true);
	}
	else {
		document.getElementById('match-facts').style.display = 'none';
		document.getElementById('add-match-facts-button-close').style.display = 'none';
		requiredMatchFactsFields(false);
	}
}
function requiredMatchFactsFields(flag) {
	if (flag) {
		const matchFactsDiv = document.getElementById('match-facts');
	    const inputs = matchFactsDiv.querySelectorAll('input');
		
		inputs.forEach(input => {
			input.required = true;
		});
	}
	else {
		const matchFactsDiv = document.getElementById('match-facts');
	    const inputs = matchFactsDiv.querySelectorAll('input');
		
		inputs.forEach(input => {
			input.required = false;
		});
	}
}

function closePopUp (popup) {
	document.getElementById(popup).style.display = 'none';
}

// TODO - Autofill as many columns in the add result popup as possible
// TODO - Add function to submit data from addResultsPopUp to database
// TODO - Add filtering to the matches page, on team, gameweek, date(month/year)