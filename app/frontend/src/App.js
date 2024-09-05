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
import { QueryClient, QueryClientProvider } from 'react-query';


function App() {
  const [teams, setTeams] = useState([]);
  const [currentTheme, setCurrentTheme] = useState(localStorage.getItem('currentTheme') || "dark");

  const queryClient = new QueryClient();

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
    const getActiveTeams = async () => {
      await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/teams?active=true`)
			.then(response => response.json())
			.then(data => setTeams(data))
        .catch(error => console.log(error));
    }

    getActiveTeams()
	}, []);

  return (
    <Router>
      <QueryClientProvider client={queryClient}>
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
                    element={<Component teams={teams} setTeams={setTeams} queryClient={queryClient} />}
                  />
                );
              })
            }
          </Routes>
        </ThemeProvider>
      </QueryClientProvider>
    </Router>
  );
}

export default App;
