import Home from './pages/home';
import Teams from './pages/teams';
import Players from './pages/players';
import Matches from './pages/matches';
import Prediction from './pages/prediction';
import Upload from './pages/upload';
import Visualisations from './pages/visualisations';

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
	// "Upload": {
	// 	path: '/upload',
	// 	component: Upload
	// },
	"Visualisations": {
		path: '/visualisations',
		component: Visualisations
	}
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