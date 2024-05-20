import { useState, useCallback, Fragment } from "react";
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
import { PageLoading } from "../components/loaders";

export default function Matches(props) {
	const [selectedSeason, setSelectedSeason] = useState("2023-2024");
	const [originX, setOriginX] = useState(0);
	const [originY, setOriginY] = useState(0);
	const [date, setDate] = useState("");
	const [homeTeam, setHomeTeam] = useState("");
	const [awayTeam, setAwayTeam] = useState("");
	const [isMatchFactsModalOpen, setIsMatchFactsModalOpen] = useState(false);

	const handleOpenMatchFactsModal = useCallback(
		async (event, date, homeTeam, awayTeam) => {
			setOriginX(event.clientX);
			setOriginY(event.clientY);
			setDate(date);
			setHomeTeam(homeTeam);
            setAwayTeam(awayTeam);
			setIsMatchFactsModalOpen(true);
		},
		[setIsMatchFactsModalOpen]
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
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	}

	const {
		data: matches = [],
		isLoading: isLoadingMatches,
		// error: matchesError,
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
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	}

	const {
		data: seasons = [],
		isLoading: isLoadingSeasons,
		// error: seasonsError,
	} = useQuery("seasons", getSeasons, {
        staleTime: Infinity,
	});
    
	const getMatchFacts = async (date, homeTeam, awayTeam) => {
		const formattedDate = date.split(" ")[0].replace(/\//g, "-");
		const response = await fetch(
			`${
				process.env.REACT_APP_DATA_API_ROOT
			}/matches/match-facts?date=${formattedDate}&home_team=${homeTeam.replace(
				/&/g,
				"%26"
			)}&away_team=${awayTeam.replace(/&/g, "%26")}`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);

		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	};

	const {
		data: matchFacts = {},
		isLoading: isLoadingMatchFacts,
		// error: matchFactsError,
	} = useQuery(
            [
                "matchFacts",
                date,
                homeTeam,
                awayTeam
            ],
            () => getMatchFacts(date, homeTeam, awayTeam),
        {
                enabled: !!homeTeam && !!awayTeam && !!date,
                staleTime: Infinity,
            }
        );
    
	if (isLoadingMatches || isLoadingSeasons) {
		return <PageLoading />;
    }

	return (
		<Fragment>
			<Container component="main">
				<CssBaseline />
				<Box
					sx={{
						marginTop: 1,
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
					<Box>
						<Container sx={{ marginTop: 2, marginBottom: 2 }}>
							<ButtonGroup size="large" aria-label="Large button group">
								{seasons.map((season) => {
									return (
										<Button
											key={season}
                                            onClick={() => setSelectedSeason(season)}
                                            variant={selectedSeason === season ? "contained" : "outlined"}
										>
											{season}
										</Button>
									);
								})}
							</ButtonGroup>
						</Container>
						<Divider sx={{ width: "100%", height: 2 }} />
                        <Divider sx={{ width: "100%", height: 2 }} />
                        <Box  sx={{ width: "100%", overflowY: "scroll", maxHeight:"60vh" }}>
                            <Box id="past-matches">
                                {matches.map((match) => {
                                    return (
                                        <MatchCards
                                            key={`${match.home_team}-${match.away_team}-${match.game_week}`} // Ensure keys are unique and well-formed
                                            gameWeek={match.game_week}
                                            date={match.date}
                                            homeTeam={match.home_team}
                                            awayTeam={match.away_team}
                                            result={match.result}
                                            handleOpenMatchFactsModal={handleOpenMatchFactsModal}
                                            matchFactsPopulated={matchFacts.length > 0}
                                        />
                                    );
                                })}
                            </Box>
                        </Box>
					</Box>
				</Box>
				{
					<MatchModal
						isMatchFactsModalOpen={isMatchFactsModalOpen}
                        handleCloseMatchFactsModal={handleCloseMatchFactsModal}
                        isLoadingMatchFacts={isLoadingMatchFacts}
                        matchFacts={matchFacts}
						originX={originX}
                        originY={originY}
					/>
				}
			</Container>
		</Fragment>
	);
}
