import Home from './pages/home';
import Teams from './pages/teams';
import Players from './pages/players';
import Matches from './pages/matches';
import Prediction from './pages/prediction';
import Visualisations from './pages/visualisations';
import Managers from './pages/managers';
import FPLSolver from './pages/fplSolver';
import FPLPlayerSearch from './pages/fplPlayerSearch';
import UpcomingMatches from './pages/upcomingMatches';
import { LeagueTable } from './pages/leagueTable';

export const routeOptions = {
	"home": {
		path: '/',
		component: Home
	},
	"teams": {
		path: '/stats/teams',
		component: Teams
	},
	"players": {
		path: '/stats/players',
		component: Players
	},
	"Matches": {
		path: '/stats/matches',
		component: Matches
	},
	"Prediction": {
		path: '/predict/match-facts',
		component: Prediction
	},
	"Upcoming Matches": {
		path: '/predict/upcoming-matches',
		component: UpcomingMatches
	},
	"Visualisations": {
		path: '/stats/visualisations',
		component: Visualisations
	},
	"Managers": {
		path: '/stats/managers',
		component: Managers
	},
	"Player Search": {
		path: '/fpl/player-search',
		component: FPLPlayerSearch,
	},
	"Solver": {
		path: '/fpl/solver',
		component: FPLSolver,
	},
	"League Table": {
		path: '/league-table',
		component: LeagueTable
	},
};

export const settingsOptions = {
	"Refresh - Data": {
		tooltip: "Download the latest game data",
		options: {
			game: `${process.env.REACT_APP_INGESTION_API_ROOT}/refresh/game-data`,
			squads: `${process.env.REACT_APP_INGESTION_API_ROOT}/refresh/squad-data`,
			schedule: `${process.env.REACT_APP_INGESTION_API_ROOT}/refresh/schedule-data`,
		}

	},
	"Refresh - Model": {
		tooltip: "Rebuild and save the prediction model",
		options: {
			rebuild: `${process.env.REACT_APP_PREDICT_API_ROOT}/model/rebuild`,
			retune: `${process.env.REACT_APP_PREDICT_API_ROOT}/model/rebuild`,
		}
	},
}

export const menuOptions = {
	"League Table": {
		path: '/league-table',
		component: LeagueTable
	},
	"Stats": {
		"players": {
			path: '/stats/players',
			component: Players
		},
		"teams": {
			path: '/stats/teams',
			component: Teams
		},
		"managers": {
			path: '/stats/managers',
			component: Managers
		},
		"matches": {
			path: '/stats/matches',
			component: Matches
		},
		"visualisations": {
			path: '/stats/visualisations',
			component: Visualisations
		},
	},
	"Prediction": {
		"Upcoming Matches": {
			path: '/predict/upcoming-matches',
			component: Prediction
		},
		"Match Facts": {
			path: '/predict/match-facts',
			component: Prediction
		},
	},
	"FPL": {
		"Player search": {
			path: '/fpl/player-search',
			component: FPLPlayerSearch
		},
		"Solver": {
			path: '/fpl/solver',
			component: FPLSolver
		}
	}
}