import React from 'react';
import { Typography } from '@mui/material';
import Box from '@mui/material/Box';

export function FormStats(props) {

	const { homeTeamFormStats, awayTeamFormStats } = props;

	console.log(homeTeamFormStats);
	console.log(awayTeamFormStats);

	return (
		<Box id="form-stats" sx={{display: "flex", flexDirection: "row", justifyContent: "space-evenly", textAlign: "center"}}>
			<Box sx={{width: "100%"}}>
				{homeTeamFormStats.map((obj, index) => {
					return (
						<Box key="homeForm">
							<Box key={`homeFormTeams-${index}`} sx={{ display:"flex", flexDirection: "row", justifyContent: "space-evenly", alignItems:"center" }}>
								<Box sx={{ width: "45%", alignItems:"center" }} >
									<Typography variant="body1" component="span" color={obj.ishome ? "secondary" : "inherit"}>
										{obj.home_team}
									</Typography>
								</Box>
								<Box sx={{ width: "10%", alignItems:"center" }} >
									<Typography variant="body1" component="span">
										{obj.home_goals} v {obj.away_goals}
									</Typography>
								</Box>
								<Box sx={{ width: "45%", alignItems:"center" }} >
									<Typography variant="body1" component="span" color={!obj.ishome ? "secondary" : "inherit"}>
										{obj.away_team}
									</Typography>
								</Box>
							</Box>
						</Box>
					);
				})}
			</Box>
			<Box sx={{width: "100%"}}>
				{awayTeamFormStats.map((obj, index) => {
					return (
						<Box key="awayForm">
							<Box key={`awayFormTeams-${index}`} sx={{ display:"flex", flexDirection: "row", justifyContent: "space-evenly", alignItems:"center" }}>
								<Box sx={{ width: "45%", alignItems:"center" }} >
									<Typography variant="body1" component="span" color={obj.ishome ? "secondary" : "inherit"}>
										{obj.home_team}
									</Typography>
								</Box>
								<Box sx={{ width: "10%", alignItems:"center" }} >
									<Typography variant="body1" component="span">
										{obj.home_goals} v {obj.away_goals}
									</Typography>
								</Box>
								<Box sx={{ width: "45%", alignItems:"center" }} >
									<Typography variant="body1" component="span" color={!obj.ishome ? "secondary" : "inherit"}>
										{obj.away_team}
									</Typography>
								</Box>
							</Box>
						</Box>
					);
				})}
			</Box>
		</Box>
	)
}