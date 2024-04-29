import React, { Fragment, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { UploadModal } from '../components/modals';
import { Container, CssBaseline, Grid } from '@mui/material';
import { Select } from '@mui/material';
import Divider from '@mui/material';
import { Input } from '@mui/material';

export default function Upload(props) {
	const [seasons, setSeasons] = props;
	const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
	const [selectedSeason, setSelectedSeason] = useState('2023-2024');

	const playerFileNames = ["defensive_action", "goalkeeping", "passing", "possession", "shooting", "standard"];

	async function getSeasons() {
		const response = await fetch('http://localhost:8080/matches/all-seasons',
			{
				headers: {
					'Access-Control-Allow-Origin': '*'
				}
			}
		);
		const seasons = await response.json();
		setSeasons(seasons);
		return seasons;
	}
	
	const handleFileUpload = (event) => {
		const file = event.target.files[0];
		// Process the file here
	};

	const handleDropdownChange = (event) => {
		const selectedOption = event.target.value;
		// Update the selected option here
	};

	const handleSave = () => {
		// Save the file here
	};
	
	return (
		<Fragment>
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
						<Box component="div" sx={{ mt: 3 }}>
							<Grid container spacing={2}>
								<Grid item xs={12}>
									<Input
										type="file"
										onChange={handleFileUpload}
									/>
								</Grid>
								<Grid item xs={12}>
									<Select
										value={selectedSeason}
										onChange={handleDropdownChange}
									>
										{
											seasons.map((season, index) => (
												<option key={index} value={season}>{season}</option>
											))
										}
									</Select>
								</Grid>
								<Grid item xs={12}>
									<Select
										onChange={handleDropdownChange}
									>
										{
											playerFileNames.map((fileName, index) => (
												<option key={index} value={fileName}>{fileName}</option>
											))
										}
									</Select>
								</Grid>
							</Grid>
						</Box>
					</Box>
				</Box>
			</Container>
			<UploadModal />
		</Fragment>
	);
}