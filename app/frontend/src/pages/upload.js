import React, { Fragment, useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Container, CssBaseline, FormControl, Grid, MenuItem } from '@mui/material';
import { Select, Divider, Button, Input } from '@mui/material';

export default function Upload() {
	const [ seasons, setSeasons ] = useState([]);
	const [selectedSeason, setSelectedSeason] = useState('2023-2024');
	const [selectedFolder, setSelectedFolder] = useState('historic_player_stats');
	
	const [selectedFiles, setSelectedFiles] = useState([]);
	const [selectedFileNames, setSelectedFileNames] = useState([]);

	const addFiles = (fileName, file) => {
		setSelectedFiles(prevSelectedFiles => [...prevSelectedFiles, file]);
		setSelectedFileNames(prevSelectedFileNames => [...prevSelectedFileNames, fileName]);
	}
	const removeFiles = (fileName, file) => {
		setSelectedFiles(prevSelectedFiles => prevSelectedFiles.filter(f => f !== file));
		setSelectedFileNames(prevSelectedFileNames => prevSelectedFileNames.filter(name => name !== fileName));
	}

	console.log(selectedFiles);	
	console.log(selectedFileNames);

	const historicPlayerStatsFileNames = ["defensive_action", "goalkeeping", "passing", "possession", "shooting", "standard"];

	useEffect(() => {
		const getSeasons = async () => {
			const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/seasons`,
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
		const formData = new FormData();
		selectedFiles.forEach((file, index) => {
			formData.append('files', file);
			formData.append('names', selectedFileNames[index]);
		});

		formData.append('folder', selectedFolder);
		formData.append('season', selectedSeason);
		
		const response = await fetch(`${process.env.REACT_APP_INGESTION_API_ROOT}/upload/upload-file`, {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();
		console.log(result);
        alert('Files uploaded successfully');

		for (let [key, value] of formData.entries()) {
			console.log(key, value);
		}
	};

	const handleSeasonDropdownChange = (event) => {
		const selectedOption = event.target.value;
		setSelectedSeason(selectedOption)
	};
	
	return (
		<Fragment>
			<Container sx={{maxHeight: "80vh", overflow: "auto"}}>
				<CssBaseline />
				<Box
					sx={{
						marginTop: 2,
						display: 'flex',
						flexDirection: 'column',
						alignItems: 'center',
						height: '100%'
					}}
				>
					<Box sx={{ width: '100%'}}>
						<Divider sx={{ height: 2 }} />
						<Box component="div" sx={{ mt: 3 }}>
							<Grid container spacing={2} >
								<Grid item xs={12} sm={12} sx={{display: "flex", flexDirection:"row", margin: 2}}>
									<Grid item xs={12} sm={12}>
										<FormControl key={"file-upload-season"} required fullWidth>
											<Select
												id="season-dropdown"
												value={selectedSeason}
												onChange={handleSeasonDropdownChange}
												sx={{ width: '100%' }}
												placeholder='Select Season *'
												label="Select Season *"
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
								<Grid item xs={12} sm={12} sx={{textAlign:"center", justifyContent: "center"}}>
									{
										historicPlayerStatsFileNames.map((fileName, index) => (
											<Box key={`file-upload-${fileName}-${index}`} sx={{ width: '100%', display: "flex", flexDirection: "row"}}>
												<FormControl key={`file-upload-${fileName}-title`} required fullWidth>
													<Grid item xs={12} sm={6} sx={{textAlign:"center", margin: 2}}>
														<Typography variant="h4" sx={{ textTransform: 'capitalize' }}>
															{fileName.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
														</Typography>
													</Grid>
												</FormControl>
												<FormControl key={`file-upload-${fileName}-input`} required fullWidth>
													<Grid item xs={12} sm={6} sx={{textAlign:"center", margin: 2}}>
														<Input
															id={`${fileName}`}
															type="file"
															accept=".csv"
															required
															name={`${fileName}`}
															onChange={(event) => {
																if (event.target.files.length > 0 && event.target.files.length < 2) {
																	addFiles(fileName, event.target.files[0]);
																} else {
																	removeFiles(fileName, event.target.files[0]);
																}
															}}
														/>
													</Grid>
												</FormControl>
											</Box>
										))
									}
								</Grid>
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
		</Fragment>
	);
}