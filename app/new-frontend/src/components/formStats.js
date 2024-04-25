import React from 'react';
import Grid from '@mui/material/Grid';
import { Typography } from '@mui/material';
import Box from '@mui/material/Box';

export function FormStats(props) {

	const { homeTeamFormStats, awayTeamFormStats } = props;

	const homeTeamForm = homeTeamFormStats[0];
	const awayTeamForm = awayTeamFormStats[0];

	return (
		<Box id="form-stats">
			<Grid item xs={12}>
				<Grid item xs={12} sm={4}>
					{Object.entries(homeTeamForm).map(([key, value]) => {
						return (
							<Grid item xs={12} key={key}>
								<Typography variant="body1">
									{key}: {value}
								</Typography>
							</Grid>
						);
					})}
				</Grid>
				<Grid item xs={12} sm={4}>
					{awayTeamFormStats.map((stat) => {
						const keys = Object.keys(stat);
						return (
							<Grid item xs={12} key={stat}>
								<Typography variant="body1">
									{keys.map((key) => (
										<div key={key}>{key}</div>
									))}
								</Typography>
							</Grid>
						);
					})}
				</Grid>
				<Grid item xs={12} sm={4}>
					{Object.entries(awayTeamForm).map(([key, value]) => {
						return (
							<Grid item xs={12} key={key}>
								<Typography variant="body1">
									{key}: {value}
								</Typography>
							</Grid>
						);
					})}
				</Grid>
			</Grid>
		</Box>
	)
}