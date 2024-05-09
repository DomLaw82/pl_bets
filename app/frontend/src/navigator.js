import Home from './pages/home';
import Teams from './pages/teams';
import Players from './pages/players';
import Matches from './pages/matches';
import Prediction from './pages/prediction';
import Upload from './pages/upload';

export const routeOptions = {
	"home": {
		path: '/',
		component: Home
	},
	"teams": {
		path: '/teams',
		component: Teams
	},
	"players": {
		path: '/players',
		component: Players
	},
	"Matches": {
		path: '/matches',
		component: Matches
	},
	"Prediction": {
		path: '/prediction',
		component: Prediction
	},
	"Upload": {
		path: '/upload',
		component: Upload
	},
};

export const settingsOptions = {
	"Refresh - Data": {
		modal: "",
		tooltip: "Download the latest game data",
		options: {
			game: "api endpoint",
			squads: "api endpoint",
			schedule: "api endpoint",
		}

	},
	"Refresh - Model": {
		modal: "",
		tooltip: "Rebuild and save the prediction model",
		options: {
			rebuild: "api endpoint",
			retuneAndRebuild: "api endpoint"
		}
	},
}