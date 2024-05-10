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
		tooltip: "Download the latest game data",
		options: {
			game: `${process.env.INGESTION_API_ROOT}/refresh/game-data`,
			squads: `${process.env.INGESTION_API_ROOT}/refresh/squad-data`,
			schedule: `${process.env.INGESTION_API_ROOT}/refresh/schedule-data`,
		}

	},
	"Refresh - Model": {
		tooltip: "Rebuild and save the prediction model",
		options: {
			rebuild: `${process.env.PREDICT_API_ROOT}/model/rebuild`,
			retune: `${process.env.PREDICT_API_ROOT}/model/rebuild`,
		}
	},
}