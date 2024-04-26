import React, {Fragment} from 'react';
import { Divider, Typography } from '@mui/material';
import Box from '@mui/material/Box';
import { PlayerCards } from './cards';

export function Squads(props) {
	const { homeTeamSquad, awayTeamSquad } = props;

	return (
		<Fragment>
			<Box key="squads" sx={{ textAlign: "center", display: "flex", flexDirection: "row" }}>
				<Box key={"home-squads"} sx={{ width: "100%" }}>
				</Box>
				<Divider orientation="vertical" flexItem />
				<Box key={"away-squads"} sx={{ width: "100%" }}>
				</Box>
			</Box>
		</Fragment>
	)
}