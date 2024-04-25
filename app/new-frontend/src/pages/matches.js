import { useEffect, useState, useCallback } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Divider } from "@mui/material";
import { MatchCards } from "../components/cards";
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import { MatchModal } from '../components/modals';

export default function Matches() {

    const [selectedSeason, setSelectedSeason] = useState('2023-2024');
    const [seasons, setSeasons] = useState([]);
    const [matches, setMatches] = useState([]);
    const [matchFacts, setMatchFacts] = useState([]);

    const [isMatchFactsModalOpen, setIsMatchFactsModalOpen] = useState(false);
    
    async function getMatchFacts(date, homeTeamName, awayTeamName) {
        const response = await fetch(`http://localhost:8080/matches/match-facts/?date=${date}&home_team=${homeTeamName}&away_team=${awayTeamName}`, {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        });
        const matchFacts = await response.json();
        console.log(matchFacts);
        return matchFacts;
    }
    
    const handleOpenMatchFactsModal = useCallback(async (date, homeTeamName, awayTeamName) => {
        const facts = await getMatchFacts(date, homeTeamName, awayTeamName);
        setIsMatchFactsModalOpen(true);
        setMatchFacts(facts)
    }, [setIsMatchFactsModalOpen, setMatchFacts]);
    
    const handleCloseMatchFactsModal = useCallback(() => {
        setIsMatchFactsModalOpen(false);
    }, []);

    async function getMatches(season) {
        const response = await fetch(`http://localhost:8080/matches/season/${season}`, {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        });
        const matches = await response.json();
        return matches;
    }

    async function getSeasons() {
        const response = await fetch('http://localhost:8080/matches/all-seasons',
            {
                headers: {
                    'Access-Control-Allow-Origin': '*'
                }
            }
        );
        const seasons = await response.json();
        return seasons;
    }

    function addResult(gameWeekValue, date, homeTeamName, awayTeamName, competitionIdValue) {
        const homeTeam = document.getElementById('add-result-home-team')
        const awayTeam = document.getElementById('add-result-away-team')
        const matchDate = document.getElementById('add-result-match-date')
        const gameWeek = document.getElementById('add-result-game-week')
        const competitionId = document.getElementById('add-result-competition-id')
        const resultPopup = document.getElementById('add-result-popup')
        const popUpBackground = document.getElementById('pop-up-background')
    
        let onlyDate = date.split(' ')[0]+"T"+date.split(' ')[1];
    
        homeTeam.value = homeTeamName;
        awayTeam.value = awayTeamName;
        matchDate.value = onlyDate;
        gameWeek.value = gameWeekValue;
        competitionId.value = competitionIdValue;
    
        popUpBackground.style.display = 'block';
        resultPopup.style.display = 'block';
    
        document.addEventListener('click', function(event) {
            if (event.target.id === 'pop-up-background') {
                resultPopup.style.display = 'none';
                popUpBackground.style.display = 'none';
            }
        });
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
    }, []);

  return (
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
                    <Box sx={{textAlign: 'center',}}>  
                        <Typography variant="h5">
                            Past Matches
                        </Typography>
                    </Box>
                    <Divider sx={{ width: '100%', height: 2 }} />
                    <Box>
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
            </Box>
          {<MatchModal isMatchFactsModalOpen={isMatchFactsModalOpen} handleCloseMatchFactsModal={handleCloseMatchFactsModal} matchFacts={matchFacts}/>}
        </Container>
  );
}