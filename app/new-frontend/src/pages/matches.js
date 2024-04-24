import { useEffect, useState } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Divider } from "@mui/material";
import { MatchCards } from "../components/cards";
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';

export default function Matches() {

    const [selectedSeason, setSelectedSeason] = useState('2023/2024');
    const [seasons, setSeasons] = useState([]);
    const [matches, setMatches] = useState([]);

    async function getMatches(season) {
        const response = await fetch(`http://localhost:8080/matches/season/${season}`);
        const matches = await response.json();
        return matches;
    }

    async function getSeasons() {
        const response = await fetch('http://localhost:8080/matches/all-seasons');
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
                const seasons = await getSeasons();
                setMatches(matches);
                setSeasons(seasons);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchData();
    }, [matches, selectedSeason]);

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
                  <Box>
                    <ButtonGroup size="large" aria-label="Large button group">
                          {
                                seasons.map((season) => {
                                    return (
                                        <Button key={season} onClick={() => setSelectedSeason(season)}>{season}</Button>
                                    )
                                })  
                          }
                    </ButtonGroup>
                  </Box>  
                <Box>
                    <Typography variant="h3">
                        Past Matches
                    </Typography>
                    <Box id="past-matches">
                        {
                            matches.map((match) => {
                                return MatchCards(match.game_week, match.date, match.home_team, match.away_team, match.result);
                            })
                        }
                    </Box>
                </Box>  
            </Box>
        </Box>
        </Container>  
  );
}