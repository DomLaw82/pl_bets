import {useEffect, useState } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Grid, Button, FormControl, Divider, Select, InputLabel, MenuItem } from "@mui/material";
import { Tabs, Tab } from "@mui/material";
import SwipeableViews from 'react-swipeable-views';
import { TabPanel, a11yProps } from "../components/tabs";


export default function Prediction(props) {
	const { teams } = props;

	const [homeTeam, setHomeTeam] = useState('');
	const [awayTeam, setAwayTeam] = useState('');

	const [homeTeamFormStats, setHomeTeamFormStats] = useState([]);
	const [awayTeamFormStats, setAwayTeamFormStats] = useState([]);
	const [homeTeamAverageStats, setHomeTeamAverageStats] = useState([]);
	const [awayTeamAverageStats, setAwayTeamAverageStats] = useState([]);
	const [headToHeadStats, setHeadToHeadStats] = useState([]);


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
								<Tabs
									value={value}
									onChange={handleChange}
									indicatorColor="secondary"
									textColor="inherit"
									variant="fullWidth"
									aria-label="full width tabs example"
									>
									<Tab label="Item One" {...a11yProps(0)} />
									<Tab label="Item Two" {...a11yProps(1)} />
									<Tab label="Item Three" {...a11yProps(2)} />
								</Tabs>
								<SwipeableViews
									axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
									index={value}
									onChangeIndex={handleChangeIndex}
								>
									<TabPanel value={value} index={0} dir={theme.direction}>
										Item One
									</TabPanel>
									<TabPanel value={value} index={1} dir={theme.direction}>
										Item Two
									</TabPanel>
									<TabPanel value={value} index={2} dir={theme.direction}>
										Item Three
									</TabPanel>
								</SwipeableViews>
							</Grid>
						</Grid>
						<Button
							type="submit"
							fullWidth
							variant="contained"
							sx={{ mt: 3, mb: 2 }}
						>
							Run Prediction
						</Button>
						<Grid container justifyContent="flex-end">
						</Grid>
					</Box>
				</Box>
			</Box>
		</Container>
	);
}