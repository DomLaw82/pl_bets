import {useEffect, useState } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import {Grid, Button, FormControl, Divider, Select, InputLabel, MenuItem} from "@mui/material";


export default function Prediction(props) {
	const { teams } = props;

	const [homeTeam, setHomeTeam] = useState('');
	const [awayTeam, setAwayTeam] = useState('');

	const [homeTeamFormStats, setHomeTeamFormStats] = useState([]);
	const [awayTeamFormStats, setAwayTeamFormStats] = useState([]);
	const [homeTeamAverageStats, setHomeTeamAverageStats] = useState([]);
	const [awayTeamAverageStats, setAwayTeamAverageStats] = useState([]);
	

	const runPrediction = () => {
		fetch('http://localhost:8080/predict')
			.then(response => response.json())
			.then(data => console.log(data))
			.catch(error => console.log(error));
	}

	const getPredictionStats = () => {
		fetch('http://localhost:8080/prediction/stats')
			.then(response => response.json())
			.then(data => {
				console.log(data)
			})
			.catch(error => console.log(error));
	}

	useEffect(() => {

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