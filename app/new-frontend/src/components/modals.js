import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';

export function MatchModal(props) {
	const { isMatchFactsModalOpen, handleCloseMatchFactsModal, matchFacts } = props;
	const uniqueStats = ["vs", "goals", "shots", "shots_on_target", "corners", "fouls", "yellow_cards", "red_cards"];

	return (
		<Modal
			open={isMatchFactsModalOpen}
			onClose={handleCloseMatchFactsModal}
			aria-labelledby="modal-modal-title"
			aria-describedby="modal-modal-description"
			sx={{border: '2px solid #000'}}
		>
			<Box
				sx={{
					position: 'absolute',
					top: '50%',
					left: '50%',
					transform: 'translate(-50%, -50%)',
					width: 600,
					bgcolor: 'background.paper',
					border: '2px solid #000',
					boxShadow: 24,
					p: 4,
					display: "flex",
					flexDirection: "row",
					justifyContent: "space-evenly",
				}}
			>
				<Box sx={{ display: "flex", flexDirection: "column", textAlign: "center", width: 200  }}>
					
					<Typography key={matchFacts.home_team} id="modal-modal-home-team" variant="body1" component="p" style={{ height: 20 }}>
						{matchFacts.home_team}
					</Typography>
					{uniqueStats.map((key) => {
						if (!key.includes("vs")) {
							return (
								<Typography key={"home_"+key} id={`modal-modal-${"home_"+key}`} variant="body1" component="p" style={{ height: 20 }}>
									{matchFacts["home_"+key]}
								</Typography>
							);
						}
						return null;
					})}
				</Box>
				<Box sx={{display: "flex", flexDirection: "column", textAlign: "center", width: 150 }}>
					{	
						uniqueStats.map((key) => {
						return (
							<Typography key={`${key}-label`} id={`modal-modal-${key}-label`} variant="body1" component="p" style={{ height: 20 }}>
								{key}
							</Typography>
						);
					})}
				</Box>
				<Box sx={{ display: "flex", flexDirection: "column", textAlign: "center", width: 200 }}>
					<Typography key={matchFacts.away_team} id="modal-modal-away-team" variant="body1" component="p" style={{ height: 20 }}>
						{matchFacts.away_team}
					</Typography>
					{uniqueStats.map((key) => {
						if (!key.includes("vs")) {
							return (
								<Typography key={"away_"+key} id={`modal-modal-${"away_"+key}`} variant="body1" component="p" style={{ height: 20}}>
									{matchFacts["away_"+key]}
								</Typography>
							);
						}
						return null;
					})}
				</Box>
			</Box>
		</Modal>
	);
}