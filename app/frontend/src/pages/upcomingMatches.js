import { useEffect, useState, useMemo, Fragment } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import { Divider } from "@mui/material";
import { MatchCards } from "../components/cards";
import { useQuery } from "react-query";
import { PageLoading, ModalDataLoading } from "../components/loaders";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

export default function UpcomingMatches() {
	const [selectedSeason, setSelectedSeason] = useState("2024-2025");
	const [formattedDate, setCurrentDate] = useState("");

	useEffect(() => {
		const currentDate = new Date();

		let currentMonth = currentDate.getMonth() + 1;
		const currentYear = currentDate.getFullYear();
		let currentDay = currentDate.getDate();

		const season = currentMonth >= 8 ? `${currentYear}-${currentYear + 1}` : `${currentYear - 1}-${currentYear}`;

		currentMonth = currentMonth < 10 ? "0" + currentMonth : currentMonth;
		currentDay = currentDay < 10 ? "0" + currentDay : currentDay;
		let formattedDate = `${currentYear}/${currentMonth}/${currentDay}`;
		
		setCurrentDate(formattedDate);
		setSelectedSeason(season);
	}, []);

	async function getCurrentGameWeek() {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/schedule?get_current_gameweek=true`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);
		const gameweek = await response.json();
		return gameweek.toString();
	}
	const {
		data: currentGameWeek = [],
		isLoading: isLoadingCurrentGameWeek,
		// error: errorCurrentGameWeek,
	} = useQuery("currentGameWeek", getCurrentGameWeek, { staleTime: Infinity });

	async function getMatches(season) {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/schedule?season=${season}`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);
		const matches = await response.json();
		return matches;
	}

	const {
		data: matches = [],
		isLoading: isLoadingMatches,
		// error: errorMatches,
	} = useQuery(["matches", selectedSeason], () => getMatches(selectedSeason), {
		staleTime: Infinity,
	});

	async function getCurrentGameWeekMatchesPrediction() {
		const response = await fetch(
			`${process.env.REACT_APP_PREDICT_API_ROOT}/win-prediction`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);
		const predictions = await response.json();
		return predictions;
	}
	const {
		data: currentGameWeekMatchesPrediction = [],
		isLoading: isLoadingPredictions,
		// error: errorPredictions,
	} = useQuery("predictions", getCurrentGameWeekMatchesPrediction, {
		staleTime: Infinity,
	});

	const currentGameWeekMatches = useMemo(() => {
		return matches.filter(match => match.date > formattedDate && match.game_week === currentGameWeek);
	}, [matches, formattedDate, currentGameWeek]);
	
	const nextGameWeekMatches = useMemo(() => {
		return matches.filter(match => match.game_week === (parseInt(currentGameWeek) + 1).toString() && match.date > formattedDate);
	}, [matches, formattedDate, currentGameWeek]);

	if (isLoadingMatches) {
		return <PageLoading />;
	}

	return (
		<Fragment>
			<Container component="main">
				<CssBaseline />
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Box sx={{ width: "100%", overflow: "hidden", overflowY: "scroll" }}>
						<Divider sx={{ width: "100%", height: 2 }} />
						<Divider sx={{ width: "100%", height: 2 }} />
						{!isLoadingCurrentGameWeek && !isLoadingPredictions ? (
							<Box
								sx={{ width: "100%", overflowY: "scroll", maxHeight: "80vh" }}
							>
								{currentGameWeekMatches.length > 0 && (
									<Accordion defaultExpanded>
										<AccordionSummary
											expandIcon={<ExpandMoreIcon />}
											aria-controls="panel1-content"
											id="panel1-header"
										>
											<Typography
												variant="h2"
												sx={{
													display: "flex",
													flexDirection: { xs: "column", md: "row" },
													alignSelf: "center",
													textAlign: "center",
													fontSize: "clamp(2.5rem, 8vw, 2.5rem)",
												}}
											>
												Current Game Week
											</Typography>
										</AccordionSummary>
										<AccordionDetails>
											<Box id="current-game-week">
												{currentGameWeekMatches.map((match) => {
													const prediction =
														currentGameWeekMatchesPrediction.find(
															(pred) =>
																pred.home_team_id === match.home_team_id &&
																pred.away_team_id === match.away_team_id
														);
													return (
														<MatchCards
															key={`${match.home_team}-${match.away_team}-${match.date}`}
															gameWeek={match.game_week}
															date={match.date}
															homeTeam={match.home_team}
															awayTeam={match.away_team}
															result={match.result}
															homeWinProb={
																prediction ? prediction.home_win_prob : null
															}
															awayWinProb={
																prediction ? prediction.away_win_prob : null
															}
															drawProb={
																prediction ? prediction.draw_prob : null
															}
															prediction={
																prediction ? prediction.prediction : null
															}
															futureMatch={formattedDate < match.date ? true : false}
														/>
													);
												})}
											</Box>
										</AccordionDetails>
									</Accordion>
								)}
								<Divider sx={{ width: "100%", height: 2 }} />
								{nextGameWeekMatches.length > 0 && (
									<Accordion>
										<AccordionSummary
											expandIcon={<ExpandMoreIcon />}
											aria-controls="panel2-content"
											id="panel2-header"
										>
											<Typography
												variant="h2"
												sx={{
													display: "flex",
													flexDirection: { xs: "column", md: "row" },
													alignSelf: "center",
													textAlign: "center",
													fontSize: "clamp(2.5rem, 8vw, 2.5rem)",
												}}
											>
												Next Week
											</Typography>
										</AccordionSummary>
										<AccordionDetails>
											<Box id="upcoming-matches">
												{nextGameWeekMatches.map((match) => (
													<MatchCards
														key={`${match.home_team}-${match.away_team}-${match.date}`}
														gameWeek={match.game_week}
														date={match.date}
														homeTeam={match.home_team}
														awayTeam={match.away_team}
														result={match.result}
														futureMatch={formattedDate < match.date ? true : false}
													/>
												))}
											</Box>
										</AccordionDetails>
									</Accordion>
								)}
							</Box>
						) : <PageLoading />}
					</Box>
				</Box>
			</Container>
		</Fragment>
	);
}
