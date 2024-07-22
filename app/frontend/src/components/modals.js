import React, { Fragment, useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import TabTableBySeasonTemplate from "./historicStats/TabTableBySeasonTemplate";
import { tabNames, tabColumns } from "./historicStats/statHeadings";
import { Button, CssBaseline, Divider, Grid } from "@mui/material";
import { AppBar } from "@mui/material";
import { Tabs } from "@mui/material";
import { Tab } from "@mui/material";
import { TabPanel, a11yProps } from "./tabs";
import { animated, useTransition, useSpring } from "@react-spring/web";
import PlayerProfileTab from "./historicStats/playerProfileTab";
import { ModalDataLoading } from "./loaders";
import { PredictionOutputCard, PredictionHistoryCard } from "./cards";
import Card from "@mui/material/Card";

export function MatchModal(props) {
	const {
		isMatchFactsModalOpen,
		handleCloseMatchFactsModal,
		originX,
		originY,
		isLoadingMatchFacts,
		matchFacts,
	} = props;
	const uniqueStats = [
		"vs",
		"goals",
		"shots",
		"shots_on_target",
		"corners",
		"fouls",
		"yellow_cards",
		"red_cards",
	];

	const modalSpring = useSpring({
		reset: isMatchFactsModalOpen,
		from: {
			opacity: 0,
			size: "0%",
			transform: "translate(-50%, -50%) scale(0)",
			top: originY,
			left: originX,
		},
		to: {
			transform: isMatchFactsModalOpen
				? "translate(-50%, -50%) scale(1)"
				: "translate(-50%, -50%) scale(0)",
			opacity: isMatchFactsModalOpen ? 1 : 0,
			size: isMatchFactsModalOpen ? "100%" : "0%",
			backgroundColor: isMatchFactsModalOpen ? "black" : "transparent",
			top: isMatchFactsModalOpen
				? document.documentElement.clientHeight / 2
				: originY,
			left: isMatchFactsModalOpen
				? document.documentElement.clientWidth / 2
				: originX,
		},
	});

	return (
		<Fragment>
			<Modal
				open={isMatchFactsModalOpen}
				onClose={handleCloseMatchFactsModal}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
				sx={{ border: "2px solid #000" }}
			>
				<animated.div
					style={{
						position: "absolute",
						top: "50%",
						left: "50%",
						width: 600,
						bgcolor: "background.paper",
						border: "2px solid #000",
						boxShadow: 24,
						p: 4,
						padding: 20,
						display: "flex",
						flexDirection: "row",
						justifyContent: "space-evenly",
						overflowX: "hidden",
						...modalSpring,
					}}
				>
					<Card sx={{ padding: 2 }} variant="outlined">
						{isLoadingMatchFacts ? (
							<Box
								sx={{
									display: "flex",
									flexDirection: "column",
									textAlign: "center",
									width: 200,
								}}
							>
								<ModalDataLoading />
							</Box>
						) : (
							<Box
								sx={{
									display: "flex",
									flexDirection: "row",
								}}
							>
								<Box
									sx={{
										display: "flex",
										flexDirection: "column",
										textAlign: "center",
										width: 200,
									}}
								>
									<Typography
										key={matchFacts.home_team}
										id="modal-modal-home-team"
										variant="body1"
										component="p"
										style={{ height: 20 }}
									>
										{matchFacts.home_team}
									</Typography>
									{uniqueStats.map((key) => {
										if (!key.includes("vs")) {
											return (
												<Typography
													key={"home_" + key}
													id={`modal-modal-${"home_" + key}`}
													variant="body1"
													component="p"
													style={{ height: 20 }}
												>
													{matchFacts["home_" + key]}
												</Typography>
											);
										}
										return null;
									})}
								</Box>
								<Divider orientation="horizontal" sx={{ height: 2 }} flexItem />
								<Box
									sx={{
										display: "flex",
										flexDirection: "column",
										textAlign: "center",
										width: 150,
									}}
								>
									{uniqueStats.map((key) => (
										<Typography
											key={`${key}-label`}
											id={`modal-modal-${key}-label`}
											variant="body1"
											component="p"
											style={{ height: 20 }}
										>
											{key}
										</Typography>
									))}
								</Box>
								<Box
									sx={{
										display: "flex",
										flexDirection: "column",
										textAlign: "center",
										width: 200,
									}}
								>
									<Typography
										key={matchFacts.away_team}
										id="modal-modal-away-team"
										variant="body1"
										component="p"
										style={{ height: 20 }}
									>
										{matchFacts.away_team}
									</Typography>
									{uniqueStats.map((key) => {
										if (!key.includes("vs")) {
											return (
												<Typography
													key={"away_" + key}
													id={`modal-modal-${"away_" + key}`}
													variant="body1"
													component="p"
													style={{ height: 20 }}
												>
													{matchFacts["away_" + key]}
												</Typography>
											);
										}
										return null;
									})}
								</Box>
							</Box>
						)}
					</Card>
				</animated.div>
			</Modal>
		</Fragment>
	);
}

export function PlayerStatsModal(props) {
	const {
		isOpen,
		historicStats,
		closePlayerStatsModal,
		originX,
		originY,
		playerProfile,
		isLoadingPlayerProfile,
		isLoadingHistoricStats,
	} = props;

	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		console.log("New value: ", newValue);
		console.log("Modal open?: ", isOpen);
		setValue(newValue);
	};

	const modalAnimation = useSpring({
		// reset: isOpen,
		from: {
			opacity: 0,
			transform: "translate(-50%, -50%) scale(0)",
			height: 0,
			width: 0,
			top: originY,
			left: originX,
		},
		to: {
			transform: isOpen
				? "translate(-50%, -50%) scale(1)"
				: "translate(-50%, -50%) scale(0)",
			opacity: isOpen ? 1 : 0,
			backgroundColor: isOpen ? "black" : "transparent",
			height: isOpen ? "max-content" : 0,
			width: isOpen ? 1250 : 0,
			top: isOpen ? document.documentElement.clientHeight / 2 : originY,
			left: isOpen ? document.documentElement.clientWidth / 2 : originX,
		},
	});

	const transitions = useTransition(value, {
		from: { opacity: 0, transform: "translate3d(100%,0,0)" },
		enter: { opacity: 1, transform: "translate3d(0%,0,0)" },
		leave: { opacity: 0, transform: "translate3d(100%,0,0)" },
		keys: value,
	});

	return (
		<Fragment>
			<CssBaseline />
			<Modal
				open={isOpen}
				onClose={closePlayerStatsModal}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
			>
				<animated.div
					style={{
						position: "absolute",
						height: "max-content",
						display: "flex",
						flexDirection: "row",
						justifyContent: "center",
						overflowX: "hidden",
						...modalAnimation,
					}}
				>
					<Box
						sx={{
							display: "flex",
							flexDirection: "column",
							textAlign: "center",
							width: "100%",
						}}
					>
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
									<Tab
										key={index}
										label={tab}
										sx={{
											whiteSpace: "nowrap",
											overflow: "hidden",
											textOverflow: "hidden",
										}}
										{...a11yProps(index)}
									/>
								))}
							</Tabs>
						</AppBar>
						<Card sx={{ margin: 2 }} variant="outlined">
							{isLoadingPlayerProfile || isLoadingHistoricStats ? (
								<ModalDataLoading />
							) : (
								<Grid
									item
									xs={12}
									sx={{
										maxHeight: 500,
										height: "min-content",
										overflowX: "auto",
										alignItems: "center",
									}}
								>
									{transitions((style, index) =>
										tabNames[index] !== "Profile" ? (
											<animated.div style={style}>
												<TabPanel value={value} index={index}>
													<TabTableBySeasonTemplate
														historicStats={historicStats}
														statHeadings={tabColumns[tabNames[index]]}
													/>
												</TabPanel>
											</animated.div>
										) : (
											<animated.div style={style}>
												<TabPanel value={value} index={index}>
													<PlayerProfileTab
														historicStats={historicStats}
														playerProfile={playerProfile}
													/>
												</TabPanel>
											</animated.div>
										)
									)}
								</Grid>
							)}
						</Card>
					</Box>
				</animated.div>
			</Modal>
		</Fragment>
	);
}

export function RefreshModal(props) {
	const { settingOptions, isOpen, setIsOpen, originX, originY } = props;

	const [apiRoute, setApiRoute] = useState("");

	useEffect(() => {
		if (apiRoute !== "") {
			if (["game", "squads", "schedule"].includes(apiRoute)) {
				fetch(`${settingOptions[apiRoute]}`)
					.then((response) => response.json())
					.then((data) => {
						alert(data);
					})
					.catch((error) => {
						alert(error);
					});
			} else if (["rebuild", "retuneAndRebuild"].includes(apiRoute)) {
				fetch(`${settingOptions[apiRoute]}`)
					.then((response) => response.json())
					.then((data) => {
						alert(data);
					})
					.catch((error) => {
						alert(error);
					});
			}
		}
	}, [settingOptions, apiRoute]);

	const modalAnimation = useSpring({
		// reset: isOpen,
		from: {
			opacity: 0,
			transform: "translate(-50%, -50%) scale(0)",
			height: 0,
			width: 0,
			top: originY,
			left: originX,
		},
		to: {
			transform: isOpen
				? "translate(-50%, -50%) scale(1)"
				: "translate(-50%, -50%) scale(0)",
			opacity: isOpen ? 1 : 0,
			backgroundColor: isOpen ? "black" : "transparent",
			height: isOpen ? "max-content" : 0,
			width: isOpen ? 1150 : 0,
			top: isOpen ? document.documentElement.clientHeight / 2 : originY,
			left: isOpen ? document.documentElement.clientWidth / 2 : originX,
		},
	});

	const handleCloseModal = () => {
		setIsOpen(false);
	};

	return (
		<Fragment>
			<Modal
				open={isOpen}
				onClose={handleCloseModal}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
			>
				<animated.div
					style={{
						position: "absolute",
						height: "max-content",
						display: "flex",
						flexDirection: "row",
						justifyContent: "center",
						textAlign: "center",
						overflowX: "hidden",
						...modalAnimation,
					}}
				>
					<Box
						sx={{
							display: "flex",
							flexDirection: "column",
							textAlign: "center",
							width: "100%",
							padding: 2,
						}}
					>
						<Typography id="modal-modal-title" variant="h3" component="h2">
							{"OPTIONS"}
						</Typography>
						<Box
							sx={{
								display: "flex",
								flexDirection: "column",
								justifyContent: "center",
								textAlign: "center",
							}}
						>
							{Object.entries(settingOptions).map(([key, value]) => (
								<Box
									key={key}
									sx={{
										display: "flex",
										flexDirection: "row",
										justifyContent: "center",
										textAlign: "center",
										margin: 2,
									}}
								>
									<Typography
										key={key}
										id={`modal-modal-${key}`}
										variant="h5"
										component="p"
										sx={{ margin: 2 }}
									>
										{key.toUpperCase()}
									</Typography>
									<Button
										key={`button-${key}`}
										onClick={() => setApiRoute(key)}
										variant="contained"
										color="primary"
										sx={{ margin: 2 }}
									>
										{"Refresh"}
									</Button>
								</Box>
							))}
						</Box>
					</Box>
				</animated.div>
			</Modal>
		</Fragment>
	);
}

export function PredictionOutputModal(props) {
	const {
		homeTeam,
		awayTeam,
		predictionOutput,
		isOpen,
		setIsOpen,
		originX,
		originY,
	} = props;

	const modalAnimation = useSpring({
		from: {
			opacity: 0,
			transform: "translate(-50%, -50%) scale(0)",
			height: 0,
			width: 0,
			top: originY,
			left: originX,
		},
		to: {
			transform: isOpen
				? "translate(-50%, -50%) scale(1)"
				: "translate(-50%, -50%) scale(0)",
			opacity: isOpen ? 1 : 0,
			backgroundColor: isOpen ? "black" : "transparent",
			height: isOpen ? "max-content" : 0,
			width: isOpen ? 1150 : 0,
			top: isOpen ? document.documentElement.clientHeight / 2 : originY,
			left: isOpen ? document.documentElement.clientWidth / 2 : originX,
		},
	});

	const handleCloseModal = () => {
		setIsOpen(false);
	};

	return (
		<Fragment>
			<Modal
				open={isOpen}
				onClose={handleCloseModal}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
			>
				<animated.div
					style={{
						position: "absolute",
						height: "max-content",
						width: "100%",
						display: "flex",
						flexDirection: "row",
						justifyContent: "center",
						textAlign: "center",
						...modalAnimation,
					}}
				>
					{predictionOutput ? (
						<PredictionOutputCard
							homeTeam={homeTeam}
							awayTeam={awayTeam}
							predictionOutput={predictionOutput}
						/>
					) : (
						<ModalDataLoading />
					)}
				</animated.div>
			</Modal>
		</Fragment>
	);
}

export function PredictionHistoryModal(props) {
	const { isOpen, setIsOpen, originX, originY, history } = props;

	const modalAnimation = useSpring({
		from: {
			opacity: 0,
			transform: "translate(-50%, -50%) scale(0)",
			height: 0,
			width: 0,
			top: originY,
			left: originX,
		},
		to: {
			transform: isOpen
				? "translate(-50%, -50%) scale(1)"
				: "translate(-50%, -50%) scale(0)",
			opacity: isOpen ? 1 : 0,
			backgroundColor: isOpen ? "black" : "transparent",
			height: isOpen ? "max-content" : 0,
			width: isOpen ? 1150 : 0,
			top: isOpen ? document.documentElement.clientHeight / 2 : originY,
			left: isOpen ? document.documentElement.clientWidth / 2 : originX,
		},
	});

	const handleCloseModal = () => {
		setIsOpen(false);
	};

	return (
		<Fragment>
			<Modal
				open={isOpen}
				onClose={handleCloseModal}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
			>
				<animated.div
					style={{
						position: "absolute",
						height: "max-content",
						width: "100%",
						display: "flex",
						flexDirection: "row",
						justifyContent: "center",
						textAlign: "center",
						overflowX: "hidden",
						...modalAnimation,
					}}
				>
					<Box
						sx={{
							display: "flex",
							flexDirection: "column",
							textAlign: "center",
							width: "100%",
							padding: 2,
						}}
					>
						<Box
							sx={{
								display: "flex",
								flexDirection: "column",
								justifyContent: "center",
								textAlign: "center",
							}}
						>
							{history.map((prediction, index) => (
								<Box
									key={`${index}-${prediction.home_team}-${prediction.away_team}`}
									sx={{
										display: "flex",
										flexDirection: "row",
										justifyContent: "center",
										textAlign: "center",
										margin: 0.5,
									}}
								>
									<PredictionHistoryCard
										homeTeam={prediction.home_team}
										awayTeam={prediction.away_team}
										data={prediction}
									/>
								</Box>
							))}
						</Box>
					</Box>
				</animated.div>
			</Modal>
		</Fragment>
	);
}

export function TeamModal(props) {
	const { isOpen, teamInfo, setIsOpen, originX, originY, isLoading } = props;

	const [value, setValue] = useState(0);

	const transitions = useTransition(value, {
		from: { opacity: 0, transform: "translate3d(100%,0,0)" },
		enter: { opacity: 1, transform: "translate3d(0%,0,0)" },
		leave: { opacity: 0, transform: "translate3d(100%,0,0)" },
		keys: value,
	});

	const modalAnimation = useSpring({
		from: {
			opacity: 0,
			transform: "translate(-50%, -50%) scale(0)",
			height: 0,
			width: 0,
			top: originY,
			left: originX,
		},
		to: {
			transform: isOpen
				? "translate(-50%, -50%) scale(1)"
				: "translate(-50%, -50%) scale(0)",
			opacity: isOpen ? 1 : 0,
			backgroundColor: isOpen ? "black" : "transparent",
			height: isOpen ? "max-content" : 0,
			width: isOpen ? 1150 : 0,
			top: isOpen ? document.documentElement.clientHeight / 2 : originY,
			left: isOpen ? document.documentElement.clientWidth / 2 : originX,
		},
	});

	const handleChange = (event, newValue) => {
		console.log("New value: ", newValue);
		console.log("Modal open?: ", isOpen);
		setValue(newValue);
	};

	const handleCloseModal = () => {
		setIsOpen(false);
	};

	const tabNames = [
		"Performance",
		"Appearances",
		"Goals",
		"Assists",
		"Goalkeeping",
		"Defending",
		"Discipline",
		"Errors",
	];
	const tabColumns = {
		Performance: [
			"season",
			"matches_played",
			"total_points",
			"wins",
			"draws",
			"losses",
			"goals_for",
			"goals_against",
			"goal_difference",
		],
		Appearances: ["appearances", "minutes"],
		Goals: [
			"goals",
			"goals_per_ninety",
			"expected_goals",
			"expected_goals_per_ninety",
		],
		Assists: [
			"assists",
			"assists_per_ninety",
			"expected_assists",
			"expected_assists_per_ninety",
		],
		Goalkeeping: ["saves", "clean_sheets"],
		Defending: ["tackles", "interceptions", "clearances"],
		Discipline: ["yellow_cards", "red_cards"],
		Errors: ["errors_leading_to_shot", "dispossessed", "miscontrols"],
	};
	const teamLeaguePerformance = teamInfo ? teamInfo[0] : null;
	const teamAllTimeStats = teamInfo ? teamInfo[1] : null;

	function toTitleCase(stat) {
		return stat
			.replace(/_/g, " ")
			.split(' ')
			.map(word => word !== "per" ? word.charAt(0).toUpperCase() + word.slice(1).toLowerCase() : word)
			.join(' ')
			.replace("Ninety", "90") 
			.replace("per", "/") 
			.replace("Expected", "Exp.");
	}

	return (
		<Fragment>
			<Modal
				open={isOpen}
				onClose={handleCloseModal}
				aria-labelledby="modal-modal-title"
				aria-describedby="modal-modal-description"
			>
				<animated.div
					style={{
						position: "absolute",
						height: "max-content",
						width: "100%",
						display: "flex",
						flexDirection: "row",
						justifyContent: "center",
						textAlign: "center",
						overflowX: "hidden",
						...modalAnimation,
					}}
				>
					<Box
						sx={{
							display: "flex",
							flexDirection: "column",
							textAlign: "center",
							width: "100%",
							padding: 2,
						}}
					>
						<Box
							sx={{
								display: "flex",
								flexDirection: "column",
								justifyContent: "center",
								textAlign: "center",
							}}
						>
							{teamInfo && !isLoading ? (
								<Box>
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
												<Tab
													key={index}
													label={tab}
													sx={{
														whiteSpace: "nowrap",
														overflow: "hidden",
														textOverflow: "hidden",
													}}
													{...a11yProps(index)}
												/>
											))}
										</Tabs>
									</AppBar>
									{transitions((style, index) =>
										tabNames[index] === "Performance" ? (
											<animated.div style={style}>
												<TabPanel value={value} index={index}>
													<TabTableBySeasonTemplate
														historicStats={teamLeaguePerformance}
														statHeadings={tabColumns[tabNames[index]]}
													/>
												</TabPanel>
											</animated.div>
										) : (
											<animated.div style={style}>
												<TabPanel value={value} index={index}>
													<Box
														sx={{
															display: "flex",
															flexDirection: "row",
															width: "100%",
															justifyContent: "space-evenly",
															overflowX: "scroll",
														}}
													>
														{tabColumns[tabNames[index]].map((stat) => (
															<Box
																sx={{
																	display: "flex",
																	flexDirection: "column",
																	textAlign: "center",
																}}
															>
																<Typography variant="h5">
																	Top 5: {toTitleCase(stat)}
																</Typography>
																<Box
																	sx={{ display: "flex", flexDirection: "row" }}
																>
																	<Box>
																		<TabTableBySeasonTemplate
																			historicStats={
																				teamAllTimeStats[
																					tabNames[index].toLowerCase()
																				][stat]
																			}
																			statHeadings={["full_name", stat]}
																		/>
																	</Box>
																</Box>
															</Box>
														))}
													</Box>
												</TabPanel>
											</animated.div>
										)
									)}
								</Box>
							) : (
								<ModalDataLoading />
							)}
						</Box>
					</Box>
				</animated.div>
			</Modal>
		</Fragment>
	);
}
