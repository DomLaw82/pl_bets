import { useEffect, useState } from "react";
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Grid, Button, FormControl, Divider, Select, InputLabel, MenuItem } from "@mui/material";
import { Tabs, Tab } from "@mui/material";
import SwipeableViews from 'react-swipeable-views';
import { useTheme } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
// import { FormStats } from "../components/formStats";


function TabPanel(props) {
	const { children, value, index, ...other } = props;
  
	return (
	  <div
		role="tabpanel"
		hidden={value !== index}
		id={`full-width-tabpanel-${index}`}
		aria-labelledby={`full-width-tab-${index}`}
		{...other}
	  >
		{value === index && (
		  <Box sx={{ p: 3 }}>
			<Typography>{children}</Typography>
		  </Box>
		)}
	  </div>
	);
}
  
TabPanel.propTypes = {
	children: PropTypes.node,
	index: PropTypes.number.isRequired,
	value: PropTypes.number.isRequired,
};

function a11yProps(index) {
	return {
	  id: `full-width-tab-${index}`,
	  'aria-controls': `full-width-tabpanel-${index}`,
	};
}

export default function Prediction(props) {

	const { teams } = props;

	const tabs = ["FORM", "AVERAGES", "HEAD TO HEAD", "SQUADS"];
	
	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		setValue(newValue);
	  };
	
	  const handleChangeIndex = (index) => {
		setValue(index);
	  };

	const [homeTeam, setHomeTeam] = useState('');
	const [awayTeam, setAwayTeam] = useState('');

	const [homeTeamFormStats, setHomeTeamFormStats] = useState([]);
	const [awayTeamFormStats, setAwayTeamFormStats] = useState([]);
	const [homeTeamAverageStats, setHomeTeamAverageStats] = useState([]);
	const [awayTeamAverageStats, setAwayTeamAverageStats] = useState([]);
	const [headToHeadStats, setHeadToHeadStats] = useState([]);

	const theme = useTheme();

	const runPrediction = () => {
		fetch('http://localhost:8080/predict')
			.then(response => response.json())
			.then(data => console.log(data))
			.catch(error => console.log(error));
	}

	const getPredictionStats = (homeTeam, awayTeam) => {
		fetch(`http://localhost:8080/prediction/stats?home_team=${homeTeam}&away_team=${awayTeam}`)
			.then(response => response.json())
			.then(data => {
				setHomeTeamFormStats(data.home_team_form);
				setAwayTeamFormStats(data.away_team_form);
				setHomeTeamAverageStats(data.home_team_average_stats);
				setAwayTeamAverageStats(data.away_team_average_stats);
				setHeadToHeadStats(data.head_to_head_stats);
			})
			.catch(error => console.log(error));
	}

	useEffect(() => {
		getPredictionStats(homeTeam, awayTeam);
	}, [homeTeam, awayTeam]);

	return (
		<Container component="main">
			<CssBaseline />
			<Box
				sx={{
					marginTop: 8,
					display: 'flex',
					flexDirection: 'column',
					alignItems: 'center'
				}}
			>
				<Typography
					variant="h1"
					sx={{
						display: 'flex',
						flexDirection: { xs: 'column', md: 'row' },
						alignSelf: 'center',
						textAlign: 'center',
						fontSize: 'clamp(3.5rem, 10vw, 4rem)',
					}}
				>
					Prediction
				</Typography>
				<Divider sx={{ width: '100%', height: 2 }} />
				<Box sx={{ width: '100%', height: 2 }}>
					<Divider sx={{ width: '100%', height: 2 }} />
					<Box component="form" noValidate onSubmit={runPrediction} sx={{ mt: 3 }}>
						<Grid container spacing={2}>
							<Grid item xs={12} sm={6}>
								<FormControl required fullWidth>
									<InputLabel id="home-team-label">Home Team</InputLabel>
									<Select
										labelId="home-team-label"
										id="home-team-required"
										value={homeTeam}
										label="Home Team *"
										onChange={(e) => setHomeTeam(e.target.value)}
									>
										<MenuItem value="">
											<em>None</em>
										</MenuItem>
										{teams.map((team) => (
											<MenuItem key={team.id} value={team.name}>
												{team.name}
											</MenuItem>
										))}
									</Select>
								</FormControl>
							</Grid>
							<Grid item xs={12} sm={6}>
								<FormControl required fullWidth>
									<InputLabel id="away-team-label">Away Team</InputLabel>
									<Select
										labelId="away-team-label"
										id="away-team-required"
										value={awayTeam}
										label="Away Team *"
										onChange={(e) => setAwayTeam(e.target.value)}
									>
										<MenuItem value="">
											<em>None</em>
										</MenuItem>
										{teams.map((team) => (
											<MenuItem key={team.id} value={team.name}>
												{team.name}
											</MenuItem>
										))}
									</Select>
								</FormControl>
							</Grid>
							<Grid item xs={12}>
								<AppBar position="static">
									<Tabs
										value={value}
										onChange={handleChange}
										indicatorColor="secondary"
										textColor="inherit"
										variant="fullWidth"
										aria-label="full width tabs example"
									>
										{tabs.map((tab, index) => (
											<Tab key={index} label={tab} {...a11yProps(index)} />
										))}
									</Tabs>
								</AppBar>
								<SwipeableViews
									axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
									index={value}
									onChangeIndex={handleChangeIndex}
								>
									{/* <TabPanel key="form" value={value} index={0} dir={theme.direction}>
										<FormStats/>
									</TabPanel>
									<TabPanel key="form" value={value} index={1} dir={theme.direction}>
										<FormStats/>
									</TabPanel>
									<TabPanel key="form" value={value} index={2} dir={theme.direction}>
										<FormStats/>
									</TabPanel> */}
								</SwipeableViews>
							</Grid>
						</Grid>
							{homeTeam && awayTeam && homeTeam !== awayTeam && (
								<Button
									type="submit"
									fullWidth
									variant="contained"
									sx={{ mt: 3, mb: 2 }}
								>
									Run Prediction
								</Button>
							)}
						<Grid container justifyContent="flex-end">
						</Grid>
					</Box>
				</Box>
			</Box>
		</Container>
	);
}