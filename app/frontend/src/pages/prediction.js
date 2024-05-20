import { Fragment, useState } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Button, FormControl, Divider, Select, InputLabel, MenuItem } from "@mui/material";
import { Tabs, Tab } from "@mui/material";
import AppBar from '@mui/material/AppBar';
import { FormStats } from "../components/predictionTabs/predictionFormStats";
import { AverageStats } from "../components/predictionTabs/predictionAverages";
import { HeadToHead } from "../components/predictionTabs/predictionHeadToHead";
import { Squads } from "../components/predictionTabs/predictionSquads";
import { TabPanel, a11yProps } from "../components/tabs";
import { PredictionModal } from "../components/modals";
import { useQuery } from "react-query";
import { PageLoading } from "../components/loaders";


export default function Prediction(props) {

	const { teams } = props;

	const tabs = ["FORM", "AVERAGES AT LOCATION", "HEAD TO HEAD", "SQUADS"];
	
	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		setValue(newValue);
	  };

	const [homeTeam, setHomeTeam] = useState('');
	const [awayTeam, setAwayTeam] = useState('');

	const [homeTeamFormStats, setHomeTeamFormStats] = useState([]);
	const [awayTeamFormStats, setAwayTeamFormStats] = useState([]);
	const [homeTeamAverageStats, setHomeTeamAverageStats] = useState([]);
	const [awayTeamAverageStats, setAwayTeamAverageStats] = useState([]);
	const [headToHeadStats, setHeadToHeadStats] = useState([]);

	const [isPredictionModalOpen, setIsPredictionModalOpen] = useState(false);
	

	const getTeamIdFromName = async (teamName) => {
		const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/prediction/team-id?team_name=${encodeURIComponent(teamName)}`,
			{
				method: 'GET',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			}
		);
		
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		const result = await response.json();
		return result.id;
	};

	const {
		data: homeId = "",
		isLoading: isLoadingHomeTeamId,
		// error: teamIdError,
	} = useQuery(
		[
			"teamId",
			homeTeam,
		],
		() => homeTeam && getTeamIdFromName(homeTeam),
		{
			staleTime: Infinity
		}
	);
	const {
		data: awayId = "",
		isLoading: isLoadingAwayTeamId,
		error: awayTeamIdError,
	} = useQuery(
		[
			"teamId",
			awayTeam,
		],
		() => awayTeam && getTeamIdFromName(awayTeam),
		{
			staleTime: Infinity,
		}
	);

	const getPredictionStats = async (homeTeam, awayTeam) => {
		const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/prediction/stats?home_team=${encodeURIComponent(homeTeam)}&away_team=${encodeURIComponent(awayTeam)}`,
			{
				method: 'GET',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			}
		);

		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	}

	const {
		data: predictionTabStats = {},
		isLoading: isLoadingPredictionStatsTabs,
		// error: predictionStatsError,
	} = useQuery(
		[
			"predictionStats",
			homeTeam,
			awayTeam,
			getPredictionStats
		],
		() => getPredictionStats(homeTeam, awayTeam),
		{
			enabled: !!homeTeam && !!awayTeam && homeTeam !== awayTeam,
			staleTime: Infinity,
			onSuccess: (data) => {
				console.log(data);
				setHomeTeamFormStats(data.home_team_form);
				setAwayTeamFormStats(data.away_team_form);
				setHomeTeamAverageStats(data.home_team_average_stats);
				setAwayTeamAverageStats(data.away_team_average_stats);
				setHeadToHeadStats(data.head_to_head_stats);
			}
		}
	);

	const getPredictionSquads = async (homeTeam, awayTeam) => {
		const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/prediction/squads?home_team=${encodeURIComponent(homeTeam)}&away_team=${encodeURIComponent(awayTeam)}`,
			{
				method: 'GET',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json'
				}
			}
		)
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	};

	const {
		data: predictionSquads = {},
		isLoading: isLoadingPredictionSquads,
		error: predictionSquadsError,
	} = useQuery(
		[
			"squads",
			homeTeam,
			awayTeam,
		],
		() => getPredictionSquads(homeTeam, awayTeam),
		{
			staleTime: Infinity,
		}

	);
	
	const runPrediction = async () => {
		const response = await fetch(`${process.env.REACT_APP_PREDICT_API_ROOT}/predict`, {
			method: 'POST',
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				homeTeamId: homeId,
				awayTeamId: awayId,
				homePlayers: [],
				awayPlayers: []
			})
		});

		if (!response.ok) {
			throw new Error("Network response was not ok");
		}

		return response.json();
	};
	
	const {
		data: predictionOutput = [],
		isLoading: isLoadingPredictionOutput,
		error: predictionOutputError,
	} = useQuery(
		[
			"predictionOutput",
			homeId,
			awayId,
		],
		() => runPrediction(),
		{	
			enabled: !!homeId && !!awayId && homeId !== awayId,
			staleTime: Infinity,
		}
		);
	
	console.log(predictionOutput)
	
	
	return (
		<Fragment>
			<Container component="main" sx={{height: "max-content"}}>
				<CssBaseline />
				<Box
					sx={{
						marginTop: 2,
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
					<Box sx={{ width: '100%'}}>
						<Divider sx={{ width: '100%', height: 2 }} />
						<Box component="div" sx={{ mt: 2, height: "60vh" }}>
							<Box component="form" noValidate sx={{ mt: 1, display: "flex", flexDirection: "row" }}>
								<Box sx={{width: "50%"}}>
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
								</Box>
								<Box sx={{width: "50%"}}>
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
								</Box>
							</Box>
							<Box sx={{ alignItems: "center", height: "55vh" }} >
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
								{
									isLoadingPredictionStatsTabs || isLoadingPredictionSquads || isLoadingPredictionSquads || isLoadingHomeTeamId || isLoadingAwayTeamId || !(homeId && awayId)  ?
									<Box sx={{ height: '100%', overflowY: 'scroll', alignItems: "center" }}>
										<TabPanel key="formStats" value={value} index={0} dir={"right"}>
											<PageLoading/>
										</TabPanel>
										<TabPanel key="averageAtLocationStats" value={value} index={1} dir={"right"}>
											<PageLoading/>
										</TabPanel>
										<TabPanel key="form" value={value} index={2} dir={"right"}>
											<PageLoading/>
										</TabPanel>
										<TabPanel key="squads" value={value} index={3} dir={"right"}>
											<PageLoading/>
										</TabPanel>
									</Box> :
									<Box sx={{ height: '100%', overflowY: 'scroll', alignItems: "center", overflow: "hidden"}}>
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
												<Squads homeTeamSquad={predictionSquads.home_team_squad} awayTeamSquad={predictionSquads.away_team_squad} isError={predictionSquadsError} />
										</TabPanel>
									</Box>
								}
							</Box>
							<Box sx={{ alignItems: "center", height: "max-content"}} >
								{homeTeam && awayTeam && homeTeam !== awayTeam && (
									<Button
										fullWidth
										onClick={() => { setIsPredictionModalOpen(true) }}
										variant="outlined"
									>
										<span>Run Prediction</span>
									</Button>
								)}
							</Box>
						</Box>
					</Box>
				</Box>
				{homeTeam && awayTeam && predictionOutput &&
					< PredictionModal homeTeam={homeTeam} awayTeam={awayTeam} predictionOutput={predictionOutput} isOpen={isPredictionModalOpen} setIsOpen={setIsPredictionModalOpen} isLoading={isLoadingPredictionOutput} isError={predictionOutputError} />
				}
			</Container>
		</Fragment>
	);
}