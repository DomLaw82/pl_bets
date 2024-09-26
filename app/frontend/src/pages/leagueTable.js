import React, { useState } from "react";
import { useQuery } from "react-query";
import { Fragment } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Divider from "@mui/material/Divider";
import { PageLoading } from "../components/loaders";
import {
	Table,
	TableBody,
	TableHead,
	Typography,
	TableCell,
	TableRow,
} from "@mui/material";
import { SeasonLeagueSelector } from "../components/seasonLeagueSelector";

export function LeagueTable() {
	const [selectedSeason, setSelectedSeason] = useState("2024-2025");
	const [selectedCompetition, setSelectedCompetition] = useState("x-00005");

	const fetchLeagueTable = async () => {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/league-table?season=${selectedSeason}&competition=${selectedCompetition}`,
		);
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	};
	const {
		isLoading: isLoadingLeagueTable,
		// error: managersError,
		data: leagueTable = [],
	} = useQuery(
		["leagueTable", selectedSeason, selectedCompetition],
		() => fetchLeagueTable(),
		{ staleTime: Infinity }
	);

	return (
		<Fragment>
			<Container component="main">
				<CssBaseline />
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Box sx={{ width: "100%", overflow: "hidden", overflowY: "scroll" }}>
						<SeasonLeagueSelector setSelectedCompetition={setSelectedCompetition} setSelectedSeason={setSelectedSeason}  selectedCompetition={selectedCompetition} selectedSeason={selectedSeason} />
						<Divider sx={{ width: "100%", height: 2 }} />
						<Divider sx={{ width: "100%", height: 2 }} />
						{!isLoadingLeagueTable ? (
							<Box sx={{ width: "100%", overflowY: "scroll", height: "70vh" }}>
								<Divider sx={{ width: "100%", height: 2 }} />
								{leagueTable.length > 0 ? (
									<Box key="league-table-container" id="league-table-container">
										<Table key={"league-table"}>
											<TableHead key={"league-table-header"}>
												<TableRow
													key={"league-table-header-row"}
													sx={{
														position: "sticky",
														top: "0",
														bgcolor: "background.paper",
														zIndex: 1,
														borderBottom: "2px solid white",
													}}
												>
													<TableCell key={"position"}>Position</TableCell>
													<TableCell key={"team"}>Team</TableCell>
													<TableCell key={"played"}>Played</TableCell>
													<TableCell key={"wins"}>Wins</TableCell>
													<TableCell key={"draws"}>Draws</TableCell>
													<TableCell key={"losses"}>Losses</TableCell>
													<TableCell key={"goals-for"}>GF</TableCell>
													<TableCell key={"goals-against"}>GA</TableCell>
													<TableCell key={"goal-difference"}>GD</TableCell>
													<TableCell key={"points"}>Points</TableCell>
												</TableRow>
											</TableHead>
											<TableBody>
												{leagueTable.map((row) => (
													<TableRow key={row.id}>
														<TableCell key={`${row.id}-position`}>
															{row.position}
														</TableCell>
														<TableCell key={`${row.id}-name`}>
															{row.name}
														</TableCell>
														<TableCell key={`${row.id}-matches_played`}>
															{row.matches_played}
														</TableCell>
														<TableCell key={`${row.id}-wins`}>
															{row.wins}
														</TableCell>
														<TableCell key={`${row.id}-draws`}>
															{row.draws}
														</TableCell>
														<TableCell key={`${row.id}-losses`}>
															{row.losses}
														</TableCell>
														<TableCell key={`${row.id}-goals_for`}>
															{row.goals_for}
														</TableCell>
														<TableCell key={`${row.id}-goals_against`}>
															{row.goals_against}
														</TableCell>
														<TableCell key={`${row.id}-goal_difference`}>
															{row.goal_difference}
														</TableCell>
														<TableCell key={`${row.id}-total_points`}>
															{row.total_points}
														</TableCell>
													</TableRow>
												))}
											</TableBody>
										</Table>
									</Box>
								) : (
									<Typography
										variant="h3"
										sx={{
											width: "100%",
											textAlign: "center",
											height: "100%",
											alignItems: "center",
											alignContent: "center",
										}}
									>
										No table available for this season
									</Typography>
								)}
							</Box>
						) : (
							<PageLoading />
						)}
					</Box>
				</Box>
			</Container>
		</Fragment>
	);
}
