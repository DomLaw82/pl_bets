import Typography from '@mui/material/Typography';
import { Fragment } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Stack from '@mui/material/Stack';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';

export default function Home() {
	return (
		<Fragment>
			<Container component="main">
				<CssBaseline />
				<Box
					id="hero"
					sx={(theme) => ({
						width: '100%',
					})}
				>
					<Container
						sx={{
							display: 'flex',
							flexDirection: 'column',
							alignItems: 'center',
							pt: { xs: 14, sm: 20 },
							pb: { xs: 8, sm: 12 },
						}}
					>
						<Stack spacing={2} useFlexGap sx={{ width: { xs: '100%', sm: '70%' } }}>
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
								Welcome to&nbsp;
								<Typography
									component="span"
									variant="h1"
									sx={{
										fontSize: 'clamp(3rem, 10vw, 4rem)',
										color: "inherit",
										fontWeight: 700,
									}}
								>
									PL Bets
								</Typography>
							</Typography>
							<Divider sx={{ width: '100%', height: 2}} />
							<Typography
								variant="h2"
								sx={{
									fontSize: 'clamp(1.5rem, 5vw, 2rem)',
									color: "inherit",
									fontWeight: 700,
									textAlign: 'center',
								}}
							>
								Your Premier League Prediction Platform
							</Typography>
							{/* <Divider sx={{ width: '100%', height: 2}} /> */}
							<Typography
								variant="h5"
								sx={{
									fontSize: 'clamp(.25rem, 2vw, 1rem)',
									color: "text.secondary",
									fontWeight: 700,
									textAlign: 'center',
								}}
							>
								PL Bets is a web application that allows users to view the Premier League teams, players, schedule, get a rundown on all the stats since 2017, and run our model which predicts the outcome of games coming in the Premier League. Everything you need, at you fingertips!
							</Typography>
							<Typography
								variant="h5"
								sx={{
									fontSize: 'clamp(.25rem, 2vw, 1rem)',
									color: "text.secondary",
									fontWeight: 700,
									textAlign: 'center',
								}}
							>
								Give it a go
							</Typography>
						</Stack>
					</Container>
				</Box>
			</Container>
		</Fragment>
	);
}