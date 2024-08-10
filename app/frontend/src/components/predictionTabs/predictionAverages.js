import React, {Fragment} from 'react';
import { Divider, Typography } from '@mui/material';
import Box from '@mui/material/Box';

export function AverageStats(props) {
	const { homeTeamAverageStats, awayTeamAverageStats } = props;

	return (
		<Fragment>
			<Box key="last-five-average-stats" sx={{height:"43vh", display: "flex", flexDirection: "row", textAlign: "center", overflowY:"scroll"}}>
				<Box key={ "home-average-stats" }  sx={{ width: "100%" }}>
					{homeTeamAverageStats.map((obj, index) => {
						const awayObject = awayTeamAverageStats[index];
						const away_goals = awayObject.away_goals;
						const away_shots = awayObject.away_shots;
						const away_shots_on_target = awayObject.away_shots_on_target;
						const away_fouls = awayObject.away_fouls;
						const away_yellow_cards = awayObject.away_yellow_cards;
						const away_red_cards = awayObject.away_red_cards;
						return (
							<Box key={ "home-average-stats-container" } sx={{ width: "100%", display: "flex", flexDirection: "column", justifyContent: "space-evenly" }}>
								<Box sx={{ height: "43vh", width: "100%", display: "flex", flexDirection: "column", justifyContent: "space-evenly", textAlign: "center" }}>
									<Box key={"home_goals"}><Typography variant="body1" component="span" color={ away_goals < obj.home_goals ? "green" : "inherit"}>{obj.home_goals}</Typography></Box>
									<Box key={"home_shots"}><Typography variant="body1" component="span" color={ away_shots < obj.home_shots ? "green" : "inherit"}>{obj.home_shots}</Typography></Box>
									<Box key={"home_shots_on_target"}><Typography variant="body1" component="span" color={ away_shots_on_target < obj.home_shots_on_target ? "green" : "inherit"}>{obj.home_shots_on_target}</Typography></Box>
									<Box key={"home_fouls"}><Typography variant="body1" component="span" color={ away_fouls < obj.home_fouls ? "green" : "inherit"}>{obj.home_fouls}</Typography></Box>
									<Box key={"home_yellow_cards"}><Typography variant="body1" component="span" color={ away_yellow_cards < obj.home_yellow_cards ? "red" : "inherit"}>{obj.home_yellow_cards}</Typography></Box>
									<Box key={"home_red_cards"}><Typography variant="body1" component="span" color={ away_red_cards < obj.home_red_cards ? "red" : "inherit"}>{obj.home_red_cards}</Typography></Box>
								</Box>
							</Box>
						);
					})}
				</Box>
				<Divider orientation="vertical" flexItem />
				<Box sx={{ display: "flex", flexDirection: "column", justifyContent: "space-evenly", textAlign: "center", width: "100%" }}>
					<Box><Typography variant="body1" component="span">Goals</Typography></Box>
					<Box><Typography variant="body1" component="span">Shots</Typography></Box>
					<Box><Typography variant="body1" component="span">Shots on Target</Typography></Box>
					<Box><Typography variant="body1" component="span">Fouls</Typography></Box>
					<Box><Typography variant="body1" component="span">Yellow Cards</Typography></Box>
					<Box><Typography variant="body1" component="span">Red Cards</Typography></Box>
				</Box>
				<Divider orientation="vertical" flexItem />
				<Box key={ "away-average-stats" } sx={{ width: "100%" }}>
					{awayTeamAverageStats.map((obj, index) => {
						const homeObject = homeTeamAverageStats[index];
						const home_goals = homeObject.home_goals;
						const home_shots = homeObject.home_shots;
						const home_shots_on_target = homeObject.home_shots_on_target;
						const home_fouls = homeObject.home_fouls;
						const home_yellow_cards = homeObject.home_yellow_cards;
						const home_red_cards = homeObject.home_red_cards;
						return (
							<Box key={"away-average-stats"} sx={{ display: "flex", flexDirection: "row", justifyContent: "space-evenly", textAlign: "center" }}>
								<Box key={"away-average-stats-container"} sx={{ height: "43vh", width: "100%", display: "flex", flexDirection: "column", justifyContent: "space-evenly"}}>
									<Box key={"away_goals"}><Typography variant="body1" component="span" color={home_goals < obj.away_goals ? "green" : "inherit"}>{obj.away_goals}</Typography></Box>
									<Box key={"away_shots"}><Typography variant="body1" component="span" color={home_shots < obj.away_shots ? "green" : "inherit"}>{obj.away_shots}</Typography></Box>
									<Box key={"away_shots_on_target"}><Typography variant="body1" component="span" color={home_shots_on_target < obj.away_shots_on_target ? "green" : "inherit"}>{obj.away_shots_on_target}</Typography></Box>
									<Box key={"away_fouls"}><Typography variant="body1" component="span" color={home_fouls < obj.away_fouls ? "green" : "inherit"}>{obj.away_fouls}</Typography></Box>
									<Box key={"away_yellow_cards"}><Typography variant="body1" component="span" color={home_yellow_cards < obj.away_yellow_cards ? "red" : "inherit"}>{obj.away_yellow_cards}</Typography></Box>
									<Box key={"away_red_cards"}><Typography variant="body1" component="span" color={home_red_cards < obj.away_red_cards ? "red" : "inherit"}>{obj.away_red_cards}</Typography></Box>
								</Box>
							</Box>
						);
					})}
				</Box>
			</Box>
		</Fragment>
	)
}