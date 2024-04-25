import { useEffect, useState } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Divider } from "@mui/material";
import { TeamCards } from "../components/cards";

export default function Teams() {
	const [teams, setTeams] = useState([]);

	useEffect(() => {
		fetch('http://localhost:8080/active-teams')
			.then(response => response.json())
			.then(data => setTeams(data))
			.catch(error => console.log(error));
	}, []);


    return (
		<Container component="main">
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
					Teams
				</Typography>
				<Divider sx={{ width: '100%', height: 2 }} />
				<Box sx={{ width: '100%', height: 2 }}>
					<Divider sx={{ width: '100%', height: 2 }} />
					<Box id="active-teams">
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
	);
}