import React, {Fragment} from 'react';
import { Divider, Typography } from '@mui/material';
import Box from '@mui/material/Box';

export function FormStats(props) {

	const { homeTeamFormStats, awayTeamFormStats } = props;

	return (
		<Fragment>
			<Box component="div" id="form-stats" sx={{height:"43vh", display: "flex", flexDirection: "row", justifyContent: "space-evenly", textAlign: "center", overflow: "hidden"}}>
				<Box component="div" sx={{width: "100%", display: "flex", flexDirection: "column", justifyContent: "space-evenly"}}>
					{homeTeamFormStats.map((obj, index) => {
						return (
							<Box component="div" key={`homeForm-${index}`}>
								<Box component="div" key={`homeFormTeams-${index}`} sx={{ display:"flex", flexDirection: "row", justifyContent: "space-evenly", alignItems:"center" }}>
									<Box component="div" sx={{ width: "45%", alignItems:"center" }} >
										<Typography variant="body1" component="span" color={obj.ishome ? "secondary" : "inherit"}>
											{obj.home_team}
										</Typography>
									</Box>
									<Box component="div" sx={{ width: "10%", alignItems:"center" }} >
										<Typography variant="body1" component="span">
											{obj.home_goals} v {obj.away_goals}
										</Typography>
									</Box>
									<Box component="div" sx={{ width: "45%", alignItems:"center" }} >
										<Typography variant="body1" component="span" color={!obj.ishome ? "secondary" : "inherit"}>
											{obj.away_team}
										</Typography>
									</Box>
								</Box>
							</Box>
						);
					})}
				</Box>
				<Divider orientation="vertical" flexItem sx={{flexGrow: 1}} />
				<Box component="div" sx={{width: "100%", display: "flex", flexDirection: "column", justifyContent: "space-evenly"}}>
					{awayTeamFormStats.map((obj, index) => {
						return (
							<Box component="div" key={`awayForm-${index}`}>
								<Box component="div" key={`awayFormTeams-${index}`} sx={{ display:"flex", flexDirection: "row", justifyContent: "space-evenly", alignItems:"center" }}>
									<Box component="div" sx={{ width: "45%", alignItems:"center" }} >
										<Typography variant="body1" component="span" color={obj.ishome ? "secondary" : "inherit"}>
											{obj.home_team}
										</Typography>
									</Box>
									<Box component="div" sx={{ width: "10%", alignItems:"center" }} >
										<Typography variant="body1" component="span">
											{obj.home_goals} v {obj.away_goals}
										</Typography>
									</Box>
									<Box component="div" sx={{ width: "45%", alignItems:"center" }} >
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
		</Fragment>
	)
}