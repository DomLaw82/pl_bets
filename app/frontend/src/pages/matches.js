import { useEffect, useState, useCallback, Fragment } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Divider } from "@mui/material";
import { MatchCards } from "../components/cards";
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import { MatchModal } from '../components/modals';

export default function Matches(props) {
    const [seasons, setSeasons] = useState([]);
    const [selectedSeason, setSelectedSeason] = useState('2023-2024');
    const [matches, setMatches] = useState([]);
    const [matchFacts, setMatchFacts] = useState([]);
    const [originX, setOriginX] = useState(0);
    const [originY, setOriginY] = useState(0);

    const [isMatchFactsModalOpen, setIsMatchFactsModalOpen] = useState(false);
    
    async function getMatchFacts(date, homeTeamName, awayTeamName) {
        const formattedDate = date.split(' ')[0].replace(/\//g, '-');
        const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/matches/match-facts?date=${formattedDate}&home_team=${homeTeamName.replace(/&/g, "%26")}&away_team=${awayTeamName.replace(/&/g, "%26")}`, {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        });
        const matchFacts = await response.json();
        return matchFacts[0];
    }
    
    const handleOpenMatchFactsModal = useCallback(async (event, date, homeTeamName, awayTeamName) => {
        setOriginX(event.clientX);
        setOriginY(event.clientY);
        const facts = await getMatchFacts(date, homeTeamName, awayTeamName);
        setIsMatchFactsModalOpen(true);
        setMatchFacts(facts)
    }, [setIsMatchFactsModalOpen, setMatchFacts]);

    const handleCloseMatchFactsModal = useCallback(() => {
        setIsMatchFactsModalOpen(false);
    }, []);

    async function getMatches(season) {
        const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/matches/season/${season}`, {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        });
        const matches = await response.json();
        return matches;
    }

    async function getSeasons() {
        const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/matches/all-seasons`,
            {
                headers: {
                    'Access-Control-Allow-Origin': '*'
                }
            }
        );
        const seasons = await response.json();
        return seasons;
    }

    useEffect(() => {
        const fetchData = async () => {
            try {
                const matches = await getMatches(selectedSeason);
                setMatches(matches);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchData();
    }, [selectedSeason]);

    useEffect(() => {
        const fetchSeasons = async () => {
            try {
                const seasons = await getSeasons();
                setSeasons(seasons);
            } catch (error) {
                console.error('Error fetching seasons:', error);
            }
        };
    
        fetchSeasons();
    }, [setSeasons]);

    return (
        <Fragment>
            <Container component="main">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
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
                        Matches
                    </Typography>
                    <Divider sx={{ width: '100%', height: 2 }} />
                    <Box>
                        <Container sx={{marginTop: 2, marginBottom: 2}}>
                            <ButtonGroup size="large" aria-label="Large button group">
                                {
                                        seasons.map((season) => {
                                            return (
                                                <Button key={season} onClick={() => setSelectedSeason(season)}>{season}</Button>
                                            )
                                        })  
                                }
                            </ButtonGroup>
                        </Container>
                        <Divider sx={{ width: '100%', height: 2 }} />
                        <Divider sx={{ width: '100%', height: 2 }} />
                        <Box id="past-matches">
                            {
                                matches.map((match) => {
                                    return (
                                        <MatchCards
                                            key={`${match.home_team}-${match.away_team}-${match.game_week}`} // Ensure keys are unique and well-formed
                                            gameWeek={match.game_week}
                                            date={match.date}
                                            homeTeam={match.home_team}
                                            awayTeam={match.away_team}
                                            result={match.result}
                                            handleOpenMatchFactsModal={handleOpenMatchFactsModal}
                                        />
                                    );
                                })
                            }
                        </Box>
                    </Box>
                </Box>
                {<MatchModal isMatchFactsModalOpen={isMatchFactsModalOpen} handleCloseMatchFactsModal={handleCloseMatchFactsModal} matchFacts={matchFacts} originX={originX} originY={originY} />}
            </Container>
        </Fragment>
  );    
}