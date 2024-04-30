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
	const [historicStats, setHistoricStats] = useState([{}]);
	const [minutesPlayed, setMinutesPlayed] = useState([{}]);
	const [isPlayerStatsModalOpen, setIsPlayerStatsModalOpen] = useState(false);
	const [modalPlayerId, setModalPlayerId] = useState(0);
	
	useEffect(() => {
        fetch(`http://localhost:8080/players/historic-stats/${modalPlayerId}`)
        .then(response => response.json())
			.then(data => {
				setHistoricStats(data)
				console.log("Historic Stats: ")
				console.log(data)
			})
        .catch(error => console.log(error));
	}, [setHistoricStats, modalPlayerId]);
	
	useEffect((player_id) => {
		fetch(`http://localhost:8080/players/recent-minutes/${modalPlayerId}`)
		.then(response => response.json())
			.then(data => {
				setMinutesPlayed(data)
				console.log("Minutes Played: ")
				console.log(data)
			})
		.catch(error => console.log(error));
	}, [setMinutesPlayed, modalPlayerId]);

    function showPlayerModal(playerId) {
		setIsPlayerStatsModalOpen(true);
		setModalPlayerId(playerId);
    }

	useEffect(() => {
		fetch('http://localhost:8080/all-active-players')
			.then(response => response.json())
			.then(data => {
				setPlayers(data)
				console.log(data)
			})
			.catch(error => console.log(error));
	}, [setPlayers]);

	return (
		<Fragment>
			<Container component="main">
				<CssBaseline />
				<Box
					sx={{
						marginTop: 8,
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
						Players
					</Typography>
					<Divider sx={{ width: '100%', height: 2 }} />
					<Box sx={{ width: '100%', height: 2 }}>
						<Divider sx={{ width: '100%', height: 2 }} />
						<Box id="active-teams">
							{
								players.map((player) => {
									return (
										<PlayerCards
											key={player.id}
											playerId={player.id}
											firstName={player.first_name}
											lastName={player.last_name}
											birthDate={player.birth_date}
											position={player.position}
											teamName={player.team_name}
											badge={`/logos/${player.team_name}.png`}
											showPlayerModal={showPlayerModal}
										/>
									);
								})
							}
						</Box>
					</Box>
				</Box>
				<PlayerStatsModal
					isOpen={isPlayerStatsModalOpen}
					setIsOpen={setIsPlayerStatsModalOpen}
					historicStats={historicStats}
					minutesPlayed={minutesPlayed}
				/>
			</Container>
		</Fragment>
	);
}