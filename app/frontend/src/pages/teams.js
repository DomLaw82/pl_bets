import { Fragment, useEffect } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Divider } from "@mui/material";
import { TeamCards } from "../components/cards";
import { useQuery } from "react-query";

export default function Teams(props) {
	const {teams, setTeams} = props;

	useEffect(() => {
		fetch(`${process.env.REACT_APP_DATA_API_ROOT}/active-teams`)
			.then(response => response.json())
			.then(data => setTeams(data))
			.catch(error => console.log(error));
	}, [setTeams]);

	// async function fetchTeamInformation(team_id) {
	// 	const teamInfo = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/teams/profile/${team_id}`)
	// 		.then(response => response.json())
	// 		.catch(error => console.log(error));
	// 	const teamAllTimeStats = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/teams/all-time-stats/${team_id}`)
	// 		.then(response => response.json())
	// 		.catch(error => console.log(error));
	// 	return teamInfo;
	// }
	// const {
	// 	data: teamInfo,
	// 	isLoading: teamInfoIsLoading,

	// } = useQuery(['teamInfo', team_id], () => fetchTeamInformation(team_id), {
	// 	enabled: !!team_id,
	// });

	return (
		<Fragment>
			<Container sx={{maxHeight: "80vh", overflow: "auto"}}>
				<CssBaseline />
				<Box
					sx={{
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
						Teams
					</Typography>
					<Divider sx={{ width: '100%', height: 2 }} />
					<Box sx={{ width: '100%'}}>
						<Divider sx={{ width: '100%', height: 2 }} />
						<Box id="active-teams" sx={{ width: "100%",height: "65vh", overflowY: "scroll"}}>
							{
								teams.map((team) => {
									return (
										<TeamCards
											key={team.id}
											teamName={team.name}
											teamLogo={`/logos/${team.name}.png`}
										/>
									);
								})
							}
						</Box>
					</Box>
				</Box>
			</Container>
		</Fragment>
	);
}