import React, {Fragment} from 'react';
import { Divider } from '@mui/material';
import Box from '@mui/material/Box';
import { PredictionPlayerCards } from '../cards';

export function Squads(props) {
	const { homeTeamSquad, awayTeamSquad } = props;

	return (
		<Fragment>
			<Box key="squads" sx={{ textAlign: "center", display: "flex", flexDirection: "row", maxHeight:"43vh", overflowY:"scroll"}}>
				<Box key={"home-squads"} sx={{ width: "100%" }}>
					{homeTeamSquad && homeTeamSquad.map((player, index) => {
						return (
							<PredictionPlayerCards key={index} firstName={player.first_name} lastName={player.last_name} position={player.position} />
						)
					})}
				</Box>
				<Divider orientation="vertical" flexItem />
				<Box key={"away-squads"} sx={{ width: "100%" }}>
					{awayTeamSquad && awayTeamSquad.map((player, index) => {
						return (
							<PredictionPlayerCards key={index} firstName={player.first_name} lastName={player.last_name} position={player.position} />
						)
					})}
				</Box>
			</Box>
		</Fragment>
	)
}