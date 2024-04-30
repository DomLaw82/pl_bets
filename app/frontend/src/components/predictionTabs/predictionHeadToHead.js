import React, {Fragment} from 'react';
import { Typography } from '@mui/material';
import Box from '@mui/material/Box';

export function HeadToHead(props) {
	const { headToHeadStats } = props;

	return (
		<Fragment>
			<Box component="div" id="form-stats" sx={{ display: "flex", flexDirection: "column", justifyContent: "space-evenly", textAlign: "center" }}>
				{headToHeadStats.map((obj, index) => {
					return (
						<Box component="div" key={`awayForm-${index}`}>
							<Box component="div" key={`awayFormTeams-${index}`} sx={{ display:"flex", flexDirection: "row", justifyContent: "space-evenly", alignItems:"center" }}>
								<Box component="div" sx={{ width: "45%", alignItems:"center" }} >
									<Typography variant="body1" component="span" color={obj.home_goals > obj.away_goals ? "green" : obj.home_goals === obj.away_goals ? "orange" :"inherit"}>
										{obj.home_team}
									</Typography>
								</Box>
								<Box component="div" sx={{ width: "10%", alignItems:"center" }} >
									<Typography variant="body1" component="span">
										{obj.home_goals} v {obj.away_goals}
									</Typography>
								</Box>
								<Box component="div" sx={{ width: "45%", alignItems:"center" }} >
									<Typography variant="body1" component="span" color={obj.home_goals < obj.away_goals ? "green" : obj.home_goals === obj.away_goals ? "orange" :"inherit"}>
										{obj.away_team}
									</Typography>
								</Box>
							</Box>
						</Box>
					);
				})}
			</Box>
		</Fragment>
	)
}