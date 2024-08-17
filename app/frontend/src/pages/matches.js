import { useEffect, useState, useCallback, useMemo, Fragment } from "react";
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

export default function Matches() {
	const [selectedSeason, setSelectedSeason] = useState("2024-2025");
	const [matchFacts, setMatchFacts] = useState([]);
	const [originX, setOriginX] = useState(0);
	const [originY, setOriginY] = useState(0);
	const [formattedDate, setCurrentDate] = useState("");

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
		return matchFacts;
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
	
	const pastMatches = useMemo(() => {
		return matches.filter(match => match.date < formattedDate);
	}, [matches, formattedDate]);

	if (isLoadingSeasons) {
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
						{!isLoadingMatches ? (
							<Box
								sx={{ width: "100%", overflowY: "scroll", maxHeight: "70vh" }}>
								<Divider sx={{ width: "100%", height: 2 }} />
								{pastMatches.length > 0 ? (
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
												futureMatch={formattedDate < match.date ? true : false}
											/>
										))}
									</Box>
								) : 
									<Typography variant="h3">
										No past matches available for this season
									</Typography>}
							</Box>
						) : <PageLoading /> }
					</Box>
				</Box>
				{ matchFacts ?
					<MatchModal
						isMatchFactsModalOpen={isMatchFactsModalOpen}
						handleCloseMatchFactsModal={handleCloseMatchFactsModal}
						matchFacts={matchFacts}
						originX={originX}
						originY={originY}
					/>
					:
					<ModalDataLoading />
				}
			</Container>
		</Fragment>
	);
}
