import { useEffect, useState } from "react";
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import { Divider } from "@mui/material";


export default function Prediction() {
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
					Prediction
				</Typography>
				<Divider sx={{ width: '100%', height: 2 }} />
				<Box sx={{ width: '100%', height: 2 }}>
					<Divider sx={{ width: '100%', height: 2 }} />
					
				</Box>
			</Box>
		</Container>
	);
}