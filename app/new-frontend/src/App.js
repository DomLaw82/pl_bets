import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import Header from './templates/header';
import {routeOptions} from './navigator';
import './App.css';

function App() {
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
                element={<Component />}
              />
            );
          })
        }
      </Routes>
    </Router>
  );
}

export default App;
