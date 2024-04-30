import React, { Fragment, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Passing from './historicStatsTabs/passing';
import Possession from './historicStatsTabs/possession';
import DefensiveActions from './historicStatsTabs/defensiveActions';
import Goalkeeping from './historicStatsTabs/goalkeeping';
import Standard from './historicStatsTabs/standard';
import Shooting from './historicStatsTabs/shooting';
import { Grid } from '@mui/material';
import { AppBar } from '@mui/material';
import { Tabs } from '@mui/material';
import { Tab } from '@mui/material';
import { TabPanel, a11yProps } from './tabs';



export function MatchModal(props) {
	const { isMatchFactsModalOpen, handleCloseMatchFactsModal, matchFacts} = props;
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

export function PlayerStatsModal(props) {
	const { isOpen, setIsOpen, historicStats, minutesPlayed } = props;

	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		setValue(newValue);
	};

	const tabs = ["Passing", "Shooting", "Defensive Actions", "Goalkeeping", "Possession", "Standard"];

	const shooting = [
		"shots_per_90",
		"shots_on_target_per_90",
		"goals_per_shot_per_90",
		"goals_per_shot_on_target_per_90",
		"average_shot_distance_per_90",
		"shots_from_free_kicks_per_90",
		"penalties_made_per_90",
		"non_penalty_expected_goals_per_shot_per_90",
		"goals_minus_expected_goals_per_90",
		"non_penalty_goals_minus_non_penalty_expected_goals_per_90",
	];



	return (
		<Fragment>
			<Modal
				open={isOpen}
				onClose={() => setIsOpen(!isOpen)}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
				sx={{ border: '2px solid #000' }}
			>
				<Box
					sx={{
						position: 'absolute',
						top: '50%',
						left: '50%',
						transform: 'translate(-50%, -50%)',
						width: "min-content",
						maxWidth: 1000,
						overflow: "hidden",
						bgcolor: 'background.paper',
						border: '2px solid #000',
						boxShadow: 24,
						p: 4,
						display: "flex",
						flexDirection: "row",
						justifyContent: "space-evenly",
					}}
				>
					<Box sx={{ display: "flex", flexDirection: "column", textAlign: "center", width: "100%" }}>
						<Box sx={{width:"100%"}}>
							<Box sx={{ width: "80%", display:"flex", flexDirection:"row" }}>
								<Typography variant="body1" component="div">
									{historicStats.first_name} {historicStats.last_name}
								</Typography>
							</Box>
							<Box sx={{width:"20%"}}>
								<Typography variant="body1" component="div">
									{historicStats.team}
								</Typography>
							</Box>
						</Box>
						<Box sx={{ width: "80%", display:"flex", flexDirection:"row" }}>
							<Box sx={{ width: "33%" }}>
								<Typography variant="body1" component="div">
									Most Recent Season: {minutesPlayed.season}
								</Typography>
							</Box>
							<Box sx={{width:"33%"}}>
								<Typography variant="body1" component="div">
									Minutes: {minutesPlayed.minutes}
								</Typography>
							</Box>
							<Box sx={{width:"33%"}}>
								<Typography variant="body1" component="div">
									90 mins: {minutesPlayed.ninetys}
								</Typography>
							</Box>
						</Box>
						<Grid item xs={12} sx={{ maxHeight:300, height:"min-content", overflowX:"auto", alignItems: "center" }} >
							<AppBar position="static">
								<Tabs
									value={value}
									onChange={handleChange}
									indicatorColor="secondary"
									textColor="inherit"
									variant="fullWidth"
									aria-label="full width tabs"
								>
									{tabs.map((tab, index) => (
										<Tab key={index} label={tab} {...a11yProps(index)} />
									))}
								</Tabs>
							</AppBar>
							<Box sx={{ height: '100%', overflowY: 'auto', alignItems: "center" }}>
								<TabPanel key="averageAtLocationStats" value={value} index={1} dir={"right"}>
									<Standard historicStats={historicStats} />
								</TabPanel>
								<TabPanel key="averageAtLocationStats" value={value} index={1} dir={"right"}>
									<Shooting historicStats={historicStats} />
								</TabPanel>
								<TabPanel key="formStats" value={value} index={0} dir={"right"}>
									<Passing historicStats={historicStats} />
								</TabPanel>
								<TabPanel key="averageAtLocationStats" value={value} index={1} dir={"right"}>
									<Possession historicStats={historicStats} />
								</TabPanel>
								<TabPanel key="averageAtLocationStats" value={value} index={1} dir={"right"}>
									<DefensiveActions historicStats={historicStats} />
								</TabPanel>
								<TabPanel key="averageAtLocationStats" value={value} index={1} dir={"right"}>
									<Goalkeeping historicStats={historicStats} />
								</TabPanel>
							</Box>
						</Grid>
					</Box>
				</Box>
			</Modal>
		</Fragment>
	)
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
			{/* <Modal
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
			</Modal> */}
		</Fragment>
	);
}