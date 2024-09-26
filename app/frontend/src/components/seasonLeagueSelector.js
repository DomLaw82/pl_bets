import React from "react";
import { Button, ButtonGroup, Container, Select, MenuItem } from "@mui/material";
import { useQuery } from "react-query";
import { PageLoading } from "./loaders";

export function LeagueSelector(props) {
	const { setSelectedCompetition, selectedCompetition } = props;
	
	async function getCompetitions() {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/leagues`,
			{
				headers: {
					"Access-Control-Allow-Origin": "*",
				},
			}
		);
		const competitions = await response.json();
		return competitions;
	}
	const {
		data: competitions = [],
		isLoading: isLoadingCompetitions,
		// error: errorCompetitions,
	} = useQuery("competitions", getCompetitions, { staleTime: Infinity });
	
	const handleCompetitionChange = (event) => {
		setSelectedCompetition(event.target.value);
	};
	
	if (isLoadingCompetitions) {
		return <PageLoading />;
	}
	
	return (		
		<Select onChange={handleCompetitionChange} value={selectedCompetition}>
			{competitions.map(({ id, country_id, name }) => (
				<MenuItem key={id} value={id}>
					{name}
				</MenuItem>
			))}
		</Select>
	)
}

export function SeasonSelector(props) {
	const { setSelectedSeason, selectedSeason } = props;
	
	async function getSeasons() {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/seasons`,
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
		<ButtonGroup size="large" aria-label="Large button group">
			{seasons.map((season) => {
				return (
					<Button
						key={season}
						onClick={() => setSelectedSeason(season)}
						variant={selectedSeason === season ? "contained" : "outlined"}
					>
						{season}
					</Button>
				);
			})}
		</ButtonGroup>
	)
}

export function SeasonLeagueSelector(props) {
	const { setSelectedSeason, setSelectedCompetition, selectedSeason, selectedCompetition } = props;

	return (		
		<Container sx={{ display: "flex", marginTop: .5, marginBottom: 1, textAlign: "center", justifyContent: "space-between" }}>
			<SeasonSelector setSelectedSeason={setSelectedSeason} selectedSeason={selectedSeason} />
			<LeagueSelector setSelectedCompetition={setSelectedCompetition} selectedCompetition={selectedCompetition} />
		</Container>
	)
}