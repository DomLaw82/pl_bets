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

export default function Teams(props) {
	const { teams, setTeams } = props;
	const [teamId, setTeamId] = useState(null);

	const [isTeamModalOpen, setIsTeamModalOpen] = useState(false);

	const [originX, setOriginX] = useState(0);
	const [originY, setOriginY] = useState(0);

	useEffect(() => {
		fetch(`${process.env.REACT_APP_DATA_API_ROOT}/active-teams`)
			.then((response) => response.json())
			.then((data) => setTeams(data))
			.catch((error) => console.log(error));
	}, [setTeams]);

	async function handleOpenTeamModal(event, team_id) {
		setOriginX(event.clientX);
		setOriginY(event.clientY);
		setTeamId(team_id);
		setIsTeamModalOpen(true);
		fetchTeamInformation(team_id);
	}

	async function fetchTeamInformation(teamId) {
		const teamInfo = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/teams/profile/${teamId}`
		)
			.then((response) => response.json())
			.catch((error) => console.log(error));

		const teamAllTimeStats = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/teams/all-time-stats/${teamId}`
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

	return (
		<Fragment>
			<Container sx={{ maxHeight: "80vh", overflow: "auto" }}>
				<CssBaseline />
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Typography
						variant="h1"
						sx={{
							display: "flex",
							flexDirection: { xs: "column", md: "row" },
							alignSelf: "center",
							textAlign: "center",
							fontSize: "clamp(3.5rem, 10vw, 4rem)",
						}}
					>
						Teams
					</Typography>
					<Divider sx={{ width: "100%", height: 2 }} />
					<Box sx={{ width: "100%" }}>
						<Divider sx={{ width: "100%", height: 2 }} />
						<Box
							id="active-teams"
							sx={{ width: "100%", height: "65vh", overflowY: "scroll" }}
						>
							{teams.map((team) => {
								return (
									<TeamCards
										teamId={team.id}
										teamName={team.name}
										teamLogo={`/logos/${team.name}.png`}
										handleOpenTeamModal={handleOpenTeamModal}
										isOpen={isTeamModalOpen}
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
