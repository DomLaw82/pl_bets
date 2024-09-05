import { Fragment, useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import {
	Grid,
	Button,
	FormControl,
	Divider,
	Select,
	InputLabel,
	MenuItem,
} from "@mui/material";
import { Tabs, Tab } from "@mui/material";
import AppBar from "@mui/material/AppBar";
import { FormStats } from "../components/predictionTabs/predictionFormStats";
import { AverageStats } from "../components/predictionTabs/predictionAverages";
import { HeadToHead } from "../components/predictionTabs/predictionHeadToHead";
import { Squads } from "../components/predictionTabs/predictionSquads";
import { TabPanel, a11yProps } from "../components/tabs";
import { PredictionOutputModal } from "../components/modals";
import HistoryIcon from "@mui/icons-material/History";
import { PredictionHistoryModal } from "../components/modals";
import { useQuery } from "react-query";

export default function Prediction(props) {
	const { teams } = props;

	const tabs = ["FORM", "AVERAGES AT LOCATION", "HEAD TO HEAD", "SQUADS"];

	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		setValue(newValue);
	};

	const [homeTeam, setHomeTeam] = useState("");
	const [homeTeamId, setHomeTeamId] = useState("");
	const [awayTeam, setAwayTeam] = useState("");
	const [awayTeamId, setAwayTeamId] = useState("");
	const [homeTeamSquad, setHomeTeamSquad] = useState([]);
	const [awayTeamSquad, setAwayTeamSquad] = useState([]);

	const [homeTeamFormStats, setHomeTeamFormStats] = useState([]);
	const [awayTeamFormStats, setAwayTeamFormStats] = useState([]);
	const [homeTeamAverageStats, setHomeTeamAverageStats] = useState([]);
	const [awayTeamAverageStats, setAwayTeamAverageStats] = useState([]);
	const [headToHeadStats, setHeadToHeadStats] = useState([]);

	const [originX, setOriginX] = useState(0);
	const [originY, setOriginY] = useState(0);

	const [predictionOutput, setPredictionOutput] = useState({});
	const [isPredictionOutputModalOpen, setIsPredictionOutputModalOpen] =
		useState(false);
	const [isPredictionHistoryModalOpen, setIsPredictionHistoryModalOpen] =
		useState(false);
	const [fetchPrediction, setFetchPrediction] = useState(false);

	const [predictionHistory, setPredictionHistory] = useState([]);

	// const [originX, setOriginX] = useState(0);
	// const [originY, setOriginY] = useState(0);

	function addToPredictionHistory(prediction) {
		let temp = predictionHistory;
		temp = temp.filter(
			(obj) =>
				obj.home_team !== prediction.home_team ||
				obj.away_team !== prediction.away_team
		);
		temp.push(prediction);
		setPredictionHistory(temp);
	}

	const getTeamIdFromName = async (teamName) => {
		try {
			const response = await fetch(
				`${
					process.env.REACT_APP_DATA_API_ROOT
				}/teams/team-id?team_name=${encodeURIComponent(teamName)}`
			);
			const data = await response.json();
			return data.id;
		} catch (error) {
			console.error("Failed to fetch team ID:", error);
			return null;
		}
	};

	const runPrediction = async (event) => {
		try {
			const response = await fetch(
				`${process.env.REACT_APP_PREDICT_API_ROOT}/predict`,
				{
					method: "POST",
					credentials: "include",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						homeTeamId: homeTeamId,
						awayTeamId: awayTeamId,
						homePlayers: [],
						awayPlayers: [],
					}),
				}
			);
			const prediction = await response.json();
			console.log(prediction);
			setOriginX(event.clientX);
			setOriginY(event.clientY);
			setIsPredictionOutputModalOpen(true);
			setPredictionOutput(prediction);
			prediction.home_team = homeTeam;
			prediction.away_team = awayTeam;
			addToPredictionHistory(prediction);
			return prediction;
		} catch (error) {
			console.error("Prediction failed:", error);
		}
	};

	const getPredictionStats = async (homeTeam, awayTeam) => {
		const response = await fetch(
			`${
				process.env.REACT_APP_DATA_API_ROOT
			}/prediction/stats?home_team=${encodeURIComponent(
				homeTeam
			)}&away_team=${encodeURIComponent(awayTeam)}`,
			{
				method: "GET",
				credentials: "include",
				headers: {
					"Content-Type": "application/json",
				},
			}
		);

		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	};
	const {
		data: predictionTabStats = {},
		// isLoading: isLoadingPredictionStatsTabs,
		// error: predictionStatsError,
	} = useQuery(
		["predictionStats", homeTeam, awayTeam, getPredictionStats],
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
			},
		}
	);

	const getPredictionSquads = async (homeTeam, awayTeam) => {
		fetch(
			`${
				process.env.REACT_APP_DATA_API_ROOT
			}/prediction/squads?home_team=${encodeURIComponent(
				homeTeam
			)}&away_team=${encodeURIComponent(awayTeam)}`
		)
			.then((response) => response.json())
			.then((data) => {
				console.log(data);
				setHomeTeamSquad(data.home_team_squad);
				setAwayTeamSquad(data.away_team_squad);
			})
			.catch((error) => console.log(error));
	};

	useEffect(() => {
		const getTeamIds = async (homeTeam, awayTeam) => {
			if (homeTeam) {
				const homeTeamId = await getTeamIdFromName(homeTeam);
				setHomeTeamId(homeTeamId);
			}
			if (awayTeam) {
				const awayTeamId = await getTeamIdFromName(awayTeam);
				setAwayTeamId(awayTeamId);
			}
		};
		const getStats = async (homeTeam, awayTeam) => {
			if (homeTeam && awayTeam && homeTeam !== awayTeam) {
				await getPredictionStats(homeTeam, awayTeam);
				await getPredictionSquads(homeTeam, awayTeam);
			}
		};

		getTeamIds(homeTeam, awayTeam);
		getStats(homeTeam, awayTeam);
	}, [homeTeam, awayTeam]);

	return (
		<Fragment>
			<Container component="main" sx={{ height: "max-content" }}>
				<CssBaseline />
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Box sx={{ width: "100%", maxHeight: "min-content" }}>
						<Divider sx={{ width: "100%", height: 2 }} />
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
								{homeTeam && awayTeam && predictionTabStats ? (
									<Grid
										item
										xs={12}
										sx={{
											maxHeight: "60vh",
											height: "min-content",
											overflow: "hidden",
											alignItems: "center",
										}}
									>
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
										<Box
											sx={{
												height: "100%",
												overflowY: "auto",
												alignItems: "center",
											}}
										>
											<TabPanel
												key="formStats"
												value={value}
												index={0}
												dir={"right"}
											>
												<FormStats
													homeTeamFormStats={homeTeamFormStats}
													awayTeamFormStats={awayTeamFormStats}
												/>
											</TabPanel>
											<TabPanel
												key="averageAtLocationStats"
												value={value}
												index={1}
												dir={"right"}
											>
												<AverageStats
													homeTeamAverageStats={homeTeamAverageStats}
													awayTeamAverageStats={awayTeamAverageStats}
												/>
											</TabPanel>
											<TabPanel
												key="form"
												value={value}
												index={2}
												dir={"right"}
											>
												<HeadToHead headToHeadStats={headToHeadStats} />
											</TabPanel>
											<TabPanel
												key="squads"
												value={value}
												index={3}
												dir={"right"}
											>
												<Squads
													homeTeamSquad={homeTeamSquad}
													awayTeamSquad={awayTeamSquad}
												/>
											</TabPanel>
										</Box>
									</Grid>
								) : (
									<Box sx={{ width: "100%", textAlign: "center", alignItems: "center", margin: "10%" }}>
										<Box>
											<Typography variant="h3" sx={{ textAlign: "center"}}>
												Select a home and away team to view predictions
											</Typography>
										</Box>
									</Box>
								)}
								<Grid item xs={12} sx={{ alignItems: "center" }}>
									<Box
										sx={{
											display: "flex",
											flexDirection: "row",
										}}
									>
										{homeTeam && awayTeam && homeTeam !== awayTeam && (
											<Button
												fullWidth
												onClick={(event) => {
													runPrediction(event);
												}}
												variant="outlined"
											>
												<span>Run Prediction</span>
											</Button>
										)}
										{predictionHistory.length >= 1 && (
											<Button
												variant="outlined"
												onClick={() => {
													setIsPredictionHistoryModalOpen(true);
												}}
											>
												<HistoryIcon />
											</Button>
										)}
									</Box>
									{homeTeam && awayTeam && predictionOutput && (
										<Grid
											item
											xs={12}
											sx={{ alignItems: "center", textAlign: "center" }}
										>
											<Box sx={{ width: "100%" }}>
												<PredictionOutputModal
													homeTeam={homeTeam}
													awayTeam={awayTeam}
													predictionOutput={predictionOutput}
													isOpen={isPredictionOutputModalOpen}
													setFetchPrediction={setFetchPrediction}
													fetchPrediction={fetchPrediction}
													setIsOpen={setIsPredictionOutputModalOpen}
													originX={originX}
													originY={originY}
												/>
											</Box>
										</Grid>
									)}
									{predictionHistory.length >= 1 && (
										<Grid>
											<Box sx={{ width: "100%" }}>
												<PredictionHistoryModal
													homeTeam={homeTeam}
													awayTeam={awayTeam}
													history={predictionHistory}
													isOpen={isPredictionHistoryModalOpen}
													setIsOpen={setIsPredictionHistoryModalOpen}
													originX={originX}
													originY={originY}
												/>
											</Box>
										</Grid>
									)}
								</Grid>
							</Grid>
						</Box>
					</Box>
				</Box>
			</Container>
		</Fragment>
	);
}
