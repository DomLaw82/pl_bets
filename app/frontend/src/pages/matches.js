import { useEffect, useState, useCallback, Fragment } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import { Divider } from "@mui/material";
import { MatchCards } from "../components/cards";
import Button from "@mui/material/Button";
import ButtonGroup from "@mui/material/ButtonGroup";
import { MatchModal } from "../components/modals";
import { useQuery } from "react-query";
import { PageLoading, ModalDataLoading } from "../components/loaders";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

export default function Matches(props) {
	const [selectedSeason, setSelectedSeason] = useState("2024-2025");
	const [matchFacts, setMatchFacts] = useState([]);
	const [originX, setOriginX] = useState(0);
	const [originY, setOriginY] = useState(0);
	const [formattedDate, setCurrentDate] = useState("");
	const [currentGameWeekMatches, setCurrentGameWeekMatches] = useState([]);	
	const [nextGameWeekMatches, setNextGameWeekMatches] = useState([]);
	const [pastMatches, setPastMatches] = useState([]);

	const [isMatchFactsModalOpen, setIsMatchFactsModalOpen] = useState(false);

	async function getMatchFacts(date, homeTeamName, awayTeamName) {
		const formattedDate = date.split(" ")[0].replace(/\//g, "-");
		const response = await fetch(
			`${
				process.env.REACT_APP_DATA_API_ROOT
			}/matches/match-facts?date=${formattedDate}&home_team=${homeTeamName.replace(
				/&/g,
				"%26"
			)}&away_team=${awayTeamName.replace(/&/g, "%26")}`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);
		const matchFacts = await response.json();
		return matchFacts[0];
	}

	const handleOpenMatchFactsModal = useCallback(
		async (event, date, homeTeamName, awayTeamName) => {
			setOriginX(event.clientX);
			setOriginY(event.clientY);
			const facts = await getMatchFacts(date, homeTeamName, awayTeamName);
			setIsMatchFactsModalOpen(true);
			setMatchFacts(facts);
		},
		[setIsMatchFactsModalOpen, setMatchFacts]
	);

	const handleCloseMatchFactsModal = useCallback(() => {
		setIsMatchFactsModalOpen(false);
	}, []);

	async function getMatches(season) {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/matches/season/${season}`,
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

	// Rest of the component code

	async function getSeasons() {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/matches/all-seasons`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);
		const seasons = await response.json();
		return seasons;
	}
	const {
		data: seasons = [],
		isLoading: isLoadingSeasons,
		// error: errorSeasons,
	} = useQuery("seasons", getSeasons, { staleTime: Infinity });

	async function getCurrentGameWeek() {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/matches/current-gameweek`,
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

	useEffect(() => {
		let currentDate = new Date();

		let year = currentDate.getFullYear(); // Gets the full year (4 digits)
		let month = currentDate.getMonth() + 1; // Gets the month (0-11, so add 1)
		let day = currentDate.getDate(); // Gets the day of the month (1-31)

		// Pad the month and day with a leading zero if necessary
		month = month < 10 ? "0" + month : month;
		day = day < 10 ? "0" + day : day;

		// Combine into a final date string in YYYY-MM-DD format
		let formattedDate = `${year}/${month}/${day}`;
		setCurrentDate(formattedDate);
	}, [selectedSeason]);

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

	useEffect(() => {
		let currentGameWeekMatches = matches.filter(
			(match) =>
				(match.date > formattedDate) & (match.game_week === currentGameWeek)
		);
		let nextGameWeekMatches = matches.filter(
			(match) =>
				(match.game_week === (parseInt(currentGameWeek) + 1).toString()) &
				(match.date > formattedDate)
		);
		let pastMatches = matches.filter(
			(match) =>
				(match.date < formattedDate) & (match.game_week === currentGameWeek)
		);

		// Update the state with the filtered matches
		setCurrentGameWeekMatches(currentGameWeekMatches);
		setNextGameWeekMatches(nextGameWeekMatches);
		setPastMatches(pastMatches);
	}, [matches, formattedDate, currentGameWeek]);

	if (isLoadingMatches | isLoadingSeasons) {
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
					<Typography
						variant="h1"
						sx={{
							display: "flex",
							flexDirection: { xs: "column", md: "row" },
							alignSelf: "center",
							textAlign: "center",
							fontSize: "clamp(3.5rem, 10vw, 4rem)",
						}}
					>
						Matches
					</Typography>
					<Divider sx={{ width: "100%", height: 2 }} />
					<Box sx={{ width: "100%", overflow: "hidden", overflowY: "scroll" }}>
						<Container sx={{ marginTop: 2, marginBottom: 2, textAlign: "center" }}>
							<ButtonGroup size="large" aria-label="Large button group">
								{seasons.map((season) => {
									return (
										<Button
											key={season}
											onClick={() => setSelectedSeason(season)}
											variant={
												selectedSeason === season ? "contained" : "outlined"
											}
										>
											{season}
										</Button>
									);
								})}
							</ButtonGroup>
						</Container>
						<Divider sx={{ width: "100%", height: 2 }} />
						<Divider sx={{ width: "100%", height: 2 }} />
						{!isLoadingCurrentGameWeek && !isLoadingPredictions && (
							<Box
								sx={{ width: "100%", overflowY: "scroll", maxHeight: "60vh" }}
							>
								{currentGameWeekMatches.length > 0 && (
									<Accordion>
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
															handleOpenMatchFactsModal={
																handleOpenMatchFactsModal
															}
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
														handleOpenMatchFactsModal={
															handleOpenMatchFactsModal
														}
													/>
												))}
											</Box>
										</AccordionDetails>
									</Accordion>
								)}
								<Divider sx={{ width: "100%", height: 2 }} />
								{pastMatches.length > 0 && (
									<Accordion>
										<AccordionSummary
											expandIcon={<ExpandMoreIcon />}
											aria-controls="panel3-content"
											id="panel3-header"
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
												Past Matches
											</Typography>
										</AccordionSummary>
										<AccordionDetails>
											<Box id="past-matches">
												{pastMatches.map((match) => (
													<MatchCards
														key={`${match.home_team}-${match.away_team}-${match.date}`}
														gameWeek={match.game_week}
														date={match.date}
														homeTeam={match.home_team}
														awayTeam={match.away_team}
														result={match.result}
														handleOpenMatchFactsModal={
															handleOpenMatchFactsModal
														}
													/>
												))}
											</Box>
										</AccordionDetails>
									</Accordion>
								)}
							</Box>
						)}
						{(isLoadingCurrentGameWeek || isLoadingPredictions) && (
							<PageLoading />
						)}
					</Box>
				</Box>
				{
					<MatchModal
						isMatchFactsModalOpen={isMatchFactsModalOpen}
						handleCloseMatchFactsModal={handleCloseMatchFactsModal}
						matchFacts={matchFacts}
						originX={originX}
						originY={originY}
					/>
				}
			</Container>
		</Fragment>
	);
}
