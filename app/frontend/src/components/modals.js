import React, { Fragment, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import HistoricStatsTabTemplate from './historicStats/historicStatsTabTemplate';
import { tabNames, tabColumns } from './historicStats/statHeadings';
import { Grid } from '@mui/material';
import { AppBar } from '@mui/material';
import { Tabs } from '@mui/material';
import { Tab } from '@mui/material';
import { TabPanel, a11yProps } from './tabs';
import { animated, useTransition, useSpring } from '@react-spring/web';


export function MatchModal(props) {
	const { isMatchFactsModalOpen, handleCloseMatchFactsModal, matchFacts} = props;
	const uniqueStats = ["vs", "goals", "shots", "shots_on_target", "corners", "fouls", "yellow_cards", "red_cards"];

	const modalSpring = useSpring({
		from: {
			opacity: 0,
			size: '0%',
			transform: 'translate(-50%, -50%) scale(0.9)'
		},
        to: {
            transform: isMatchFactsModalOpen ? 'translate(-50%, -50%) scale(1)' : 'translate(-50%, -50%) scale(0.95)',
			opacity: isMatchFactsModalOpen ? 1 : 0,
			size: isMatchFactsModalOpen ? '100%' : '0%',
			backgroundColor: isMatchFactsModalOpen ? 'black' : 'transparent',
        },
	});

	return (
        <Fragment>
            <Modal
                open={isMatchFactsModalOpen}
                onClose={handleCloseMatchFactsModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
                sx={{ border: '2px solid #000' }}
            >
                <animated.div
                    style={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        width: 600,
                        bgcolor: 'background.paper',
                        border: '2px solid #000',
                        boxShadow: 24,
						p: 4,
						padding: 20,
                        display: "flex",
                        flexDirection: "row",
						justifyContent: "space-evenly",
						...modalSpring
                    }}
                >
                    {/* Content box for home team stats */}
                    <Box sx={{ display: "flex", flexDirection: "column", textAlign: "center", width: 200 }}>
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

                    {/* Center box for labels */}
                    <Box sx={{display: "flex", flexDirection: "column", textAlign: "center", width: 150 }}>
                        {uniqueStats.map((key) => (
                            <Typography key={`${key}-label`} id={`modal-modal-${key}-label`} variant="body1" component="p" style={{ height: 20 }}>
                                {key}
                            </Typography>
                        ))}
                    </Box>

                    {/* Content box for away team stats */}
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
                </animated.div>
            </Modal>
        </Fragment>
	);
}

export function PlayerStatsModal(props) {
	const { isOpen, historicStats, closePlayerStatsModal } = props;

	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		setValue(newValue);
	};

	const modalAnimation = useSpring({
		from: {
			opacity: 0,
			size: '0%',
			transform: 'translate(-50%, -50%) scale(0.95)',
			height: 0,
		},
		to: {
			transform: isOpen ? 'translate(-50%, -50%) scale(1)' : 'translate(-50%, -50%) scale(0.95)',
			opacity: isOpen ? 1 : 0,
			size: isOpen ? '100%' : '0%',
			backgroundColor: isOpen ? 'black' : 'transparent',
			height: isOpen ? "max-content" : 0,
		},
		config: { tension: 300, friction: 30 }
	});

	const transitions = useTransition(value, {
		from: { opacity: 0, transform: 'translate3d(100%,0,0)' },
		enter: { opacity: 1, transform: 'translate3d(0%,0,0)' },
		leave: { opacity: 0, transform: 'translate3d(-100%,0,0)' },
		keys: value
	});

	return (
		<Fragment>
			<Modal
				open={isOpen}
				onClose={closePlayerStatsModal}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
				sx={{
					border: '2px solid #000'
				}}
			>
				<animated.div
					style={{
						position: 'absolute',
						top: '50%',
						left: '50%',
						width: 1150,
						height: "max-content",
						maxWidth: 1200,
						display: "flex",
						flexDirection: "row",
						justifyContent: "center",
						...modalAnimation
					}}
				>
					<Box sx={{ display: "flex", flexDirection: "column", textAlign: "center", width: "100%" }}>
						<Typography variant="body1" component="div">
							{historicStats.first_name} {historicStats.last_name}
						</Typography>
						<Typography variant="body1" component="div">
							{historicStats.team}
						</Typography>
						<AppBar position="static">
							<Tabs
								value={value}
								onChange={handleChange}
								indicatorColor="secondary"
								textColor="inherit"
								variant="fullWidth"
								aria-label="full width tabs"
							>
								{tabNames.map((tab, index) => (
									<Tab key={index} label={tab} {...a11yProps(index)} />
								))}
							</Tabs>
						</AppBar>
						<Grid item xs={12} sx={{ maxHeight:500, height:"min-content", overflowX:"auto", alignItems: "center" }}>
							{transitions((style, index) => (
								<animated.div style={style}>
									<TabPanel value={value} index={index}>
										<HistoricStatsTabTemplate historicStats={historicStats} statHeadings={tabColumns[tabNames[index]]} />
									</TabPanel>
								</animated.div>
							))}
						</Grid>
					</Box>
				</animated.div>
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
		const file = event.target.files;
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