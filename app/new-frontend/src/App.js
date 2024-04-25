import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import { useState, useEffect } from "react";
import Header from './templates/header';
import {routeOptions} from './navigator';
import './App.css';

function App() {
  const [teams, setTeams] = useState([]);
  
  useEffect(() => {
		fetch('http://localhost:8080/active-teams')
			.then(response => response.json())
			.then(data => setTeams(data))
			.catch(error => console.log(error));
	}, []);

  return (
    <Router>
      <Header />
      <Routes>
        {
          Object.keys(routeOptions).map((key, index) => {
            const { path, component: Component} = routeOptions[key];
            return (
              <Route
                key={index}
                path={path}
                element={<Component teams={teams} setTeams={setTeams} />}
              />
            );
          })
        }
      </Routes>
    </Router>
  );
}

export default App;
