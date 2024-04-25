import React, {useEffect, useState} from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Divider from '@mui/material/Divider';

export function MatchModal(props) {
	const { isMatchFactsModalOpen, handleCloseMatchFactsModal, matchFacts } = props;
	console.log(matchFacts)

	return (
		<Modal
			open={isMatchFactsModalOpen}
			onClose={handleCloseMatchFactsModal}
			aria-labelledby="modal-modal-title"
			aria-describedby="modal-modal-description"
		>
			<Box
				sx={{
					position: 'absolute',
					top: '50%',
					left: '50%',
					transform: 'translate(-50%, -50%)',
					width: 400,
					bgcolor: 'background.paper',
					border: '2px solid #000',
					boxShadow: 24,
					p: 4,
					display: "flex",
					flexDirection: "row",
					alignText: "center"
				}}
			>
				<Box sx={{ display: "flex", flexDirection: "column" }}>
					
					<Typography key={matchFacts.homeTeam} id={`modal-modal-home-team`} variant="body1" component="h4">
						{matchFacts.homeTeam}
					</Typography>
					{Object.keys(matchFacts).map((key) => {
						if (key.includes("home") && key !== "home_team" ) {
							return (
								<Typography key={key} id={`modal-modal-${key}`} variant="body2" component="p">
									{matchFacts[key]}
								</Typography>
							);
						}
						return null;
					})}
				</Box>
				<Divider orientation="vertical" sx={{ height: '100%' }} />
				<Box>
					{Object.keys(matchFacts).map((key) => {
						return (
							<Typography key={`${key}-label`} id={`modal-modal-${key}-label`} variant="body1" component="h3">
								{key}
							</Typography>
						);
					})}
				</Box>
				<Divider orientation="vertical" sx={{ height: '100%' }} />
				<Box sx={{display: "flex", flexDirection: "column"}}>
					<Typography key={matchFacts.awayTeam} id={`modal-modal-away-team`} variant="body1" component="h4">
						{matchFacts.awayTeam}
					</Typography>
					{Object.keys(matchFacts).map((key) => {
						if (key.includes("away") && key !== "away_team") {
							return (
								<Typography key={key} id={`modal-modal-${key}`} variant="body2" component="p">
									{matchFacts[key]}
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

export function AddResultModal() {}