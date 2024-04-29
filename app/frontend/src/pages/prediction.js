import { Fragment, useEffect, useState } from "react";
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Grid, Button, FormControl, Divider, Select, InputLabel, MenuItem } from "@mui/material";
import { Tabs, Tab } from "@mui/material";
import AppBar from '@mui/material/AppBar';
import { FormStats } from "../components/predictionFormStats";
import { AverageStats } from "../components/predictionAverages";
import { HeadToHead } from "../components/predictionHeadToHead";
import { Squads } from "../components/predictionSquads";
import { PredictionOutputCard } from "../components/cards";


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
			<Box>{children}</Box>
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

	const tabs = ["FORM", "AVERAGES AT LOCATION", "HEAD TO HEAD", "SQUADS"];
	
	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		setValue(newValue);
	  };

	const [homeTeam, setHomeTeam] = useState('');
	const [homeTeamId, setHomeTeamId] = useState('');
	const [awayTeam, setAwayTeam] = useState('');
	const [awayTeamId, setAwayTeamId] = useState('');

	const [homeTeamFormStats, setHomeTeamFormStats] = useState([]);
	const [awayTeamFormStats, setAwayTeamFormStats] = useState([]);
	const [homeTeamAverageStats, setHomeTeamAverageStats] = useState([]);
	const [awayTeamAverageStats, setAwayTeamAverageStats] = useState([]);
	const [headToHeadStats, setHeadToHeadStats] = useState([]);
	const [homeTeamSquad, setHomeTeamSquad] = useState([]);
	const [awayTeamSquad, setAwayTeamSquad] = useState([]);

	const [predictionOutput, setPredictionOutput] = useState([]);


	const getTeamIdFromName = async (teamName) => {
		try {
		  const response = await fetch(`http://localhost:8080/prediction/team-id?team_name=${encodeURIComponent(teamName)}`);
		  const data = await response.json();
		  return data.id;
		} catch (error) {
		  console.error("Failed to fetch team ID:", error);
		  return null;
		}
	};
	  

	const runPrediction = async (event) => {
		try {
			const response = await fetch(`http://localhost:8008/predict`, {
				method: 'POST',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					homeTeamId: homeTeamId,
					awayTeamId: awayTeamId,
					homePlayers: [],
					awayPlayers: []
				})
			});
			const data = await response.json();
			console.log(data);
			setPredictionOutput(data); // or set some state
		} catch (error) {
			console.error('Prediction failed:', error);
		}
	};

	const getPredictionStats = async (homeTeam, awayTeam) => {
		fetch(`http://localhost:8080/prediction/stats?home_team=${encodeURIComponent(homeTeam)}&away_team=${encodeURIComponent(awayTeam)}`)
			.then(response => response.json())
			.then(data => {
				console.log(data);
				setHomeTeamFormStats(data.home_team_form);
				setAwayTeamFormStats(data.away_team_form);
				setHomeTeamAverageStats(data.home_team_average_stats);
				setAwayTeamAverageStats(data.away_team_average_stats);
				setHeadToHeadStats(data.head_to_head_stats);
			})
			.catch(error => console.log(error));
	}
	const getPredictionSquads = async (homeTeam, awayTeam) => {
		fetch(`http://localhost:8080/prediction/squads?home_team=${encodeURIComponent(homeTeam)}&away_team=${encodeURIComponent(awayTeam)}`)
			.then(response => response.json())
			.then(data => {
				console.log(data);
				setHomeTeamSquad(data.home_team_squad);
				setAwayTeamSquad(data.away_team_squad);
			})
			.catch(error => console.log(error));
		
	}

	useEffect(() => {
		const getTeamIds = async (homeTeam, awayTeam) => {
			if (homeTeam) {
				const homeTeamId = await getTeamIdFromName(homeTeam)
				setHomeTeamId(homeTeamId);
			}
			if (awayTeam) {
				const awayTeamId = await getTeamIdFromName(awayTeam)
				setAwayTeamId(awayTeamId);
			}
		}
		const getStats = async (homeTeam, awayTeam) => {
			if (homeTeam && awayTeam && homeTeam !== awayTeam) {
				await getPredictionStats(homeTeam, awayTeam);
				await getPredictionSquads(homeTeam, awayTeam);
			}
		}

		getTeamIds(homeTeam, awayTeam);
		getStats(homeTeam, awayTeam);
	}, [homeTeam, awayTeam]);

	return (
		<Fragment>
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
						<Box component="div" sx={{ mt: 3 }}>
							<Grid container spacing={2}>
								<Grid item xs={12} sm={6}>
									<FormControl key={"home-team-select"} required fullWidth>
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
									<FormControl key={"away-team-select"} required fullWidth>
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
								<Grid item xs={12} sx={{ maxHeight:300, height:"min-content", overflow:"hidden", alignItems: "center" }} >
									<AppBar position="static">
										<Tabs
											value={value}
											onChange={handleChange}
											indicatorColor="secondary"
											textColor="inherit"
											variant="fullWidth"
											aria-label="full width tabs"
										>
											{tabs.map((tab, index) => (
												<Tab key={index} label={tab} {...a11yProps(index)} />
											))}
										</Tabs>
									</AppBar>
									<Box sx={{ height: '100%', overflowY: 'auto', alignItems: "center" }}>
										<TabPanel key="formStats" value={value} index={0} dir={"right"}>
										<FormStats homeTeamFormStats={homeTeamFormStats} awayTeamFormStats={awayTeamFormStats} />
										</TabPanel>
										<TabPanel key="averageAtLocationStats" value={value} index={1} dir={"right"}>
										<AverageStats homeTeamAverageStats={homeTeamAverageStats} awayTeamAverageStats={awayTeamAverageStats} />
										</TabPanel>
										<TabPanel key="form" value={value} index={2} dir={"right"}>
										<HeadToHead headToHeadStats={headToHeadStats} />
										</TabPanel>
										<TabPanel key="squads" value={value} index={3} dir={"right"}>
										<Squads homeTeamSquad={homeTeamSquad} awayTeamSquad={awayTeamSquad} />
										</TabPanel>
									</Box>
								</Grid>
								<Grid item xs={12} sx={{ alignItems: "center" }} >
									{homeTeam && awayTeam && homeTeam !== awayTeam && (
										<Button
											fullWidth
											onClick={() => { runPrediction(homeTeam, awayTeam) }}
											variant="outlined"
										>
											<span>Run Prediction</span>
										</Button>
									)}
									{homeTeam && awayTeam && predictionOutput &&
										<Grid item xs={12} sx={{ alignItems: "center", textAlign: "center" }} >				
											<Box sx={{ width: '100%', height: 2 }}>
												<PredictionOutputCard homeTeam={ homeTeam } awayTeam={awayTeam} predictionOutput={predictionOutput} />
											</Box>
										</Grid>
									}
								</Grid>
								
							</Grid>
						</Box>
					</Box>
				</Box>
			</Container>
		</Fragment>
	);
}