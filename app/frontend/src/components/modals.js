import React, { Fragment, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { CssBaseline } from '@mui/material';
import { Select } from '@mui/material';
import { Input } from '@mui/material';
import { Grid } from '@mui/material';
import { Divider } from '@mui/material';


export function MatchModal(props) {
	const { isMatchFactsModalOpen, handleCloseMatchFactsModal, matchFacts } = props;
	const uniqueStats = ["vs", "goals", "shots", "shots_on_target", "corners", "fouls", "yellow_cards", "red_cards"];

	return (
		<Fragment>
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
		</Fragment>
	);
}

export function UploadModal(props) {

	const { seasons, setSeasons } = props;
	const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
	const [selectedSeason, setSelectedSeason] = useState('2023-2024');

	const playerFileNames = ["defensive_action", "goalkeeping", "passing", "possession", "shooting", "standard"];

	async function getSeasons() {
        const response = await fetch('http://localhost:8080/matches/all-seasons',
            {
                headers: {
                    'Access-Control-Allow-Origin': '*'
                }
            }
        );
		const seasons = await response.json();
		setSeasons(seasons);
        return seasons;
	}
	
	const handleFileUpload = (event) => {
		const file = event.target.files[0];
		// Process the file here
	};

	const handleDropdownChange = (event) => {
		const selectedOption = event.target.value;
		// Update the selected option here
	};

	const handleSave = () => {
		// Save the file here
	};
	
	return (
		<Fragment>
			<Modal
				open={isUploadModalOpen}
				onClose={() => setIsUploadModalOpen(!isUploadModalOpen)}
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
							Upload Data
						</Typography>
						<Divider sx={{ width: '100%', height: 2 }} />
						<Box sx={{ width: '100%', height: 2 }}>
							<Divider sx={{ width: '100%', height: 2 }} />
							<Box component="div" sx={{ mt: 3 }}>
								<Grid container spacing={2}>
									<Grid item xs={12}>
										<Input
											type="file"
											onChange={handleFileUpload}
										/>
									</Grid>
									<Grid item xs={12}>
										<Select
											value={selectedSeason}
											onChange={handleDropdownChange}
										>
											{
												seasons.map((season, index) => (
													<option key={index} value={season}>{season}</option>
												))
											}
										</Select>
									</Grid>
									<Grid item xs={12}>
										<Select
											onChange={handleDropdownChange}
										>
											{
												playerFileNames.map((fileName, index) => (
													<option key={index} value={fileName}>{fileName}</option>
												))
											}
										</Select>
									</Grid>
								</Grid>
							</Box>
						</Box>
					</Box>
				</Box>
			</Modal>
		</Fragment>
	);
}