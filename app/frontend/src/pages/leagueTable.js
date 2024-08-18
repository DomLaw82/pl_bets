import React, { useState } from "react";
import { useQuery } from "react-query";
import { Fragment } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Button from "@mui/material/Button";
import ButtonGroup from "@mui/material/ButtonGroup";
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

export function LeagueTable() {
	const [selectedSeason, setSelectedSeason] = useState("2021-22");

	const fetchLeagueTable = async () => {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/league-table/${selectedSeason}`
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
	} = useQuery("leagueTable", fetchLeagueTable, { staleTime: Infinity });

	async function getSeasons() {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/matches/all-seasons`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);
		const seasons = await response.json();
		return seasons;
	}
	const {
		data: seasons = [],
		isLoading: isLoadingSeasons,
		// error: errorSeasons,
	} = useQuery("seasons", getSeasons, { staleTime: Infinity });

	if (isLoadingSeasons) {
		return <PageLoading />;
	}

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
						<Container
							sx={{ marginTop: 2, marginBottom: 2, textAlign: "center" }}
						>
							<ButtonGroup size="large" aria-label="Large button group">
								{seasons.map((season) => {
									return (
										<Button
											key={season}
											onClick={() => setSelectedSeason(season)}
											variant={
												selectedSeason === season ? "contained" : "outlined"
											}
										>
											{season}
										</Button>
									);
								})}
							</ButtonGroup>
						</Container>
						<Divider sx={{ width: "100%", height: 2 }} />
						<Divider sx={{ width: "100%", height: 2 }} />
						{!isLoadingLeagueTable ? (
							<Box
								sx={{ width: "100%", overflowY: "scroll", maxHeight: "70vh" }}
							>
								<Divider sx={{ width: "100%", height: 2 }} />
								{leagueTable.length > 0 ? (
									<Box id="league-table">
										<Table>
											<TableHead>
												<TableRow>
													<TableCell>Position</TableCell>
													<TableCell>Team</TableCell>
													<TableCell>Played</TableCell>
													<TableCell>Wins</TableCell>
													<TableCell>Draws</TableCell>
													<TableCell>Losses</TableCell>
													<TableCell>GF</TableCell>
													<TableCell>GA</TableCell>
													<TableCell>GD</TableCell>
													<TableCell>Points</TableCell>
												</TableRow>
											</TableHead>
											{leagueTable.map((row) => (
												<TableBody>
													<TableRow key={row.id}>
														<TableCell>{row.position}</TableCell>
														<TableCell>{row.name}</TableCell>
														<TableCell>{row.matches_played}</TableCell>
														<TableCell>{row.wins}</TableCell>
														<TableCell>{row.draws}</TableCell>
														<TableCell>{row.losses}</TableCell>
														<TableCell>{row.goals_for}</TableCell>
														<TableCell>{row.goals_against}</TableCell>
														<TableCell>{row.goal_difference}</TableCell>
														<TableCell>{row.total_points}</TableCell>
													</TableRow>
												</TableBody>
											))}
										</Table>
									</Box>
								) : (
									<Typography variant="h3">
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
