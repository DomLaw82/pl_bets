import { Fragment, useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import { Divider } from "@mui/material";
import { TeamCards } from "../components/cards";
import { useQuery } from "react-query";
import { infinity } from "ldrs";
import { TeamModal } from "../components/modals";
import { PageLoading } from "../components/loaders";

export default function Teams(props) {

	const [teamId, setTeamId] = useState(null);
	const [isTeamModalOpen, setIsTeamModalOpen] = useState(false);

	const [originX, setOriginX] = useState(0);
	const [originY, setOriginY] = useState(0);

	const fetchTeams = async () => {
		const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/teams?active=true`);
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	};

	const {
        data: teams,
        isLoading,
        isError,
        error
    } = useQuery('teams', fetchTeams, {
        // Optional: Configure the query here, e.g., setting a refetch interval
        refetchInterval: 60000, // Refetch the data every 60 seconds
    });

	async function handleOpenTeamModal(event, team_id) {
		setOriginX(event.clientX);
		setOriginY(event.clientY);
		setTeamId(team_id);
		setIsTeamModalOpen(true);
		fetchTeamInformation(team_id);
	}

	async function fetchTeamInformation(teamId) {
		const teamInfo = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/teams/profile?team_id=${teamId}`
		)
			.then((response) => response.json())
			.catch((error) => console.log(error));

		const teamAllTimeStats = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/teams/all-time-stats?team_id=${teamId}`
		)
			.then((response) => response.json())
			.catch((error) => console.log(error));
		return [teamInfo, teamAllTimeStats];
	}
	const { data: teamTabData = [[], {}], isLoading: isLoadingTeamInfo } = useQuery(
		["teamInfo", teamId],
		() => fetchTeamInformation(teamId),
		{
			staleTime: infinity,
		}
	);
	

    if (isLoading) {
        return <PageLoading/>
    }

	return (
		<Fragment>
			<Container sx={{ maxHeight: "100vh", overflow: "auto" }}>
				<CssBaseline />
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Box sx={{ width: "100%" }} key={"active-team-container"}>
						<Divider sx={{ width: "100%", height: 2 }} />
						<Box
							id="active-teams"
							sx={{ width: "100%", height: "80vh", overflowY: "scroll" }}
							key={"active-teams"}
						>
							{teams.map((team) => {
								return (
									<TeamCards
										teamId={team.id}
										teamName={team.name}
										teamLogo={`/logos/${team.name}.png`}
										handleOpenTeamModal={handleOpenTeamModal}
										isOpen={isTeamModalOpen}
										key={team.id}
									/>
								);
							})}
						</Box>
					</Box>
					<Box>
						{<TeamModal
							teamInfo={teamTabData}
							isOpen={isTeamModalOpen}
							setIsOpen={setIsTeamModalOpen}
							originX={originX}
							originY={originY}
							isLoading={isLoadingTeamInfo}
						/>}
					</Box>
				</Box>
			</Container>
		</Fragment>
	);
}
