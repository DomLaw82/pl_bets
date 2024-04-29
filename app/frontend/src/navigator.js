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
	}
};

export const settingsOptions = {
	"upload": {
		path: '/upload',
		component: Upload
	},
}