import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import { useState, useEffect } from "react";
import Header from './templates/header';
import {routeOptions} from './navigator';
import './App.css';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeSwitcher } from "./components/themeSwitcher";


function App() {
  const [teams, setTeams] = useState([]);
  const [currentTheme, setCurrentTheme] = useState(localStorage.getItem('currentTheme') || "dark");

  localStorage.setItem('currentTheme', currentTheme);

  useEffect(() => {
    localStorage.setItem('currentTheme', currentTheme);
  }, [currentTheme]);

  let theme = createTheme({
    palette: {
      mode: localStorage.getItem('currentTheme'),
    },
  });
  
  useEffect(() => {
		fetch(`${process.env.DATA_API_ROOT}/active-teams`)
			.then(response => response.json())
			.then(data => setTeams(data))
			.catch(error => console.log(error));
	}, []);

  return (
    <Router>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Header />
        <ThemeSwitcher currentTheme={currentTheme} setCurrentTheme={setCurrentTheme} />
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
      </ThemeProvider>
    </Router>
  );
}

export default App;
