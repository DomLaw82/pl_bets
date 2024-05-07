import React, { Fragment, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { UploadModal } from '../components/modals';
import { Container, CssBaseline, FormControl, Grid, MenuItem } from '@mui/material';
import { Select, Divider, Button, Input } from '@mui/material';

export default function Upload() {
	const [ seasons, setSeasons ] = useState([]);
	const [selectedSeason, setSelectedSeason] = useState('');
	const [selectedFile, setSelectedFile] = useState('');
	const [selectedFolder, setSelectedFolder] = useState('');

	const fileFolders = ["game_data", "historic_player_stats", "schedule_data", "squad_data"]
	const fileNames = {
		"": [],
		"historic_player_stats": ["defensive_action", "goalkeeping", "passing", "possession", "shooting", "standard", "random"],
		"game_data": [""],
		"schedule_data": [""],
		"squad_data": [""]
	};

	useEffect(() => {
		const getSeasons = async () => {
			const response = await fetch('http://localhost:8080/matches/all-seasons',
				{
					headers: {
						'Access-Control-Allow-Origin': '*'
					}
				}
			);
			const seasons = await response.json();
			setSeasons(seasons);
		}
		getSeasons();
	}, []);

	const handleFileUpload = async (event) => {
		const file = document.getElementById("file-upload-file").files[0];

		const requestBody = {
			file: file,
			folder: selectedFolder,
			name: selectedFile,
			season: selectedSeason
		};

		fetch(`http://localhost:8009/upload/upload-file`, {
			method: 'POST',
			body: requestBody
		});
		console.log(requestBody);
	};

	const handleSeasonDropdownChange = (event) => {
		const selectedOption = event.target.value;
		setSelectedSeason(selectedOption)
	};
	const handleFileDropdownChange = (event) => {
		const selectedOption = event.target.value;
		setSelectedFile(selectedOption);
	};
	const handleFolderDropdownChange = (event) => {
		const selectedOption = event.target.value;
		setSelectedFolder(selectedOption);
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
						Upload
					</Typography>
					<Divider sx={{ width: '100%', height: 2 }} />
					<Box sx={{ width: '100%', height: 2 }}>
						<Divider sx={{ height: 2 }} />
						<Box component="div" sx={{ mt: 3 }}>
							<Grid container spacing={2} >
								<Grid item xs={12} sm={12} sx={{display: "flex", flexDirection:"row", margin: 2}}>
									<Grid item xs={12} sm={4}>
										<FormControl key={"file-upload-folder"} required fullWidth>
											<Select
												id="folder-dropdown"
												value={selectedFolder}
												onChange={handleFolderDropdownChange}
												sx={{ width: '100%' }}
												label="File Folder *"
												required
											>	
												{
													fileFolders.map((folder, index) => (
														<MenuItem key={`${folder}-${index}`} value={folder}>{folder.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</MenuItem>
													))
												}
											</Select>
										</FormControl>
									</Grid>
									<Grid item xs={12} sm={4}>
										<FormControl key={"file-upload-name"} required fullWidth>
											<Select
												id="file-dropdown"
												value={selectedFile}
												onChange={handleFileDropdownChange}
												sx={{ width: '100%' }}
												label="File Name *"
												required
											>
												{ selectedFolder &&
													fileNames[selectedFolder].map((fileName, index) => (
														<MenuItem key={`${fileName}-${index}`} value={fileName}>{fileName.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</MenuItem>
													))
												}
											</Select>
										</FormControl>
									</Grid>
									<Grid item xs={12} sm={4}>
										<FormControl key={"file-upload-season"} required fullWidth>
											<Select
												id="season-dropdown"
												value={selectedSeason}
												onChange={handleSeasonDropdownChange}
												sx={{ width: '100%' }}
												label="Season *"
												required
											>	
												{
													seasons.map((season, index) => (
														<MenuItem key={`${season}-${index}`} value={season}>{season}</MenuItem>
													))
												}
											</Select>
										</FormControl>
									</Grid>
								</Grid>
								<FormControl key={"file-upload-file"} required fullWidth>
									<Grid item xs={12} sm={12} sx={{textAlign:"center", margin: 2}}>
										<Input
											id='file-upload-file'
											type="file"
											accept=".csv"
											required
										/>
									</Grid>
								</FormControl>
								<Grid item xs={12} sm={12} sx={{textAlign:"center", margin: 2}}>
									<Button
										type="submit"
										onClick={handleFileUpload}
										variant="outlined"
									>
										Upload File
									</Button>
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