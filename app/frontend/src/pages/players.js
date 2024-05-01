import { useEffect, useState, Fragment } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Divider } from "@mui/material";
import { PlayerCards } from "../components/cards";
import { PlayerStatsModal } from "../components/modals";

export default function Players() {
    const [players, setPlayers] = useState([]);
    const [historicStats, setHistoricStats] = useState([]);
    const [minutesPlayed, setMinutesPlayed] = useState([]);
    const [isPlayerStatsModalOpen, setIsPlayerStatsModalOpen] = useState(false);
    const [modalPlayerId, setModalPlayerId] = useState("");

    // Function to fetch player stats
    const fetchPlayerData = async (playerId) => {
        try {
            const statsResponse = await fetch(`http://localhost:8080/players/historic-stats/${playerId}`);
            const statsData = await statsResponse.json();
            const minutesResponse = await fetch(`http://localhost:8080/players/recent-minutes/${playerId}`);
            const minutesData = await minutesResponse.json();

            setHistoricStats(statsData);
            setMinutesPlayed(minutesData[0]);

            if (statsData.length > 0 && minutesData.length > 0) {
                setIsPlayerStatsModalOpen(true);
            }
        } catch (error) {
            console.error("Error fetching player data:", error);
        }
    };

    // Effect for fetching all active players
    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                const response = await fetch('http://localhost:8080/all-active-players');
                const data = await response.json();
                setPlayers(data);
            } catch (error) {
                console.error("Error fetching players:", error);
            }
        };
        fetchPlayers();
    }, []);

    // Effect for handling modal data fetching
    useEffect(() => {
        if (modalPlayerId) {
            fetchPlayerData(modalPlayerId);
        }
	}, [modalPlayerId]);
	
	const closePlayerStatsModal = () => {
		setIsPlayerStatsModalOpen(false);
		setModalPlayerId("");
	}

    return (
        <Fragment>
            <Container component="main">
                <CssBaseline />
                <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Typography variant="h1" sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, alignSelf: 'center', textAlign: 'center', fontSize: 'clamp(3.5rem, 10vw, 4rem)' }}>
                        Players
                    </Typography>
                    <Divider sx={{ width: '100%', height: 2 }} />
                    <Box sx={{ width: '100%' }}>
                        <Divider sx={{ width: '100%', height: 2 }} />
                        <Box id="active-teams">
                            {players.map((player) => (
                                <PlayerCards
                                    key={player.id}
									playerId={player.id}
									firstName={player.first_name}
									lastName={player.last_name}
									birthDate={player.birth_date}
									position={player.position}
									teamName={player.team_name}
									badge={`/logos/${player.team_name}.png`}
									setModalPlayerId={setModalPlayerId}
                                />
                            ))}
                        </Box>
                    </Box>
                </Box>
                <PlayerStatsModal
                    isOpen={isPlayerStatsModalOpen}
                    setIsOpen={setIsPlayerStatsModalOpen}
                    historicStats={historicStats}
					minutesPlayed={minutesPlayed}
					closePlayerStatsModal={closePlayerStatsModal}
                />
            </Container>
        </Fragment>
    );
}
