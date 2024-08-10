import React from "react";
import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import { Typography } from "@mui/material";

export default function PlayerProfileTab(props) {
	const { playerProfile, historicStats } = props;

	return (
		<Box
			sx={{
				display: "flex",
				flexDirection: "row",
				justifyContent: "center",
				margin: 2,
				width: "100%",
			}}
		>
			<Box
				sx={{
					display: "flex",
					flexDirection: "column",
					width: "50%",
					alignItems: "center",
				}}
				key={"Information"}
			>
				{playerProfile.map((player) => (
					<Box
						sx={{
							display: "flex",
							flexDirection: "row",
							justifyContent: "center",
							margin: 2,
							width: "100%",
							height: "100%",
						}}
						key={`${player.id}-info`}
					>
						<Box
							sx={{
								display: "flex",
								flexDirection: "column",
								alignItems: "flex-start",
								justifyContent: "space-around",
								height: "100%",
								padding: 2,
							}}
							key={`${player.id}-headers`}
						>
							<Box>
								<Typography variant="h5">{"Full Name:"}</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{"DOB:"}</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{"Nationality:"}</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{"Position:"}</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{"Current Team:"}</Typography>
							</Box>
						</Box>
						<Box
							sx={{
								display: "flex",
								flexDirection: "column",
								alignItems: "flex-start",
								justifyContent: "space-around",
								height: "100%",
								padding: 2,
							}}
							key={player.id}
						>
							<Box>
								<Typography variant="h5">
									{player.first_name} {player.last_name}
								</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{player.birth_date}</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{player.nationality}</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{player.position}</Typography>
							</Box>
							<Box>
								<Typography variant="h5">{player.team}</Typography>
							</Box>
						</Box>
					</Box>
				))}
			</Box>

			<Box
				key={"playing-time"}
				sx={{
					display: "flex",
					justifyContent: "center",
					textAlign: "center",
					alignItems: "center",
					margin: 2,
					width: "50%",
				}}
			>
				<table style={{ borderCollapse: "collapse", textAlign: "center" }}>
					<thead>
						<tr style={{ border: `4px solid white` }} key={"profile-table-head"}>
							<th style={{ border: `4px solid white`, padding: 5 }}>
								<Tooltip title="Season"><>S</></Tooltip>
							</th>
							<th style={{ border: `4px solid white`, padding: 5 }}>
								<Tooltip title="Team"><>T</></Tooltip>
							</th>
							<th style={{ border: `4px solid white`, padding: 5 }}>
								<Tooltip title="Played"><>P</></Tooltip>
							</th>
							<th style={{ border: `4px solid white`, padding: 5 }}>
								<Tooltip title="Starts"><>S</></Tooltip>
							</th>
							<th style={{ border: `4px solid white`, padding: 5 }}>
								<Tooltip title="Minutes"><>M</></Tooltip>
							</th>
						</tr>
					</thead>
					<tbody>
						{historicStats.map((player) => (
							<tr style={{ border: `2px double white` }} key={`${player.season} ${player.team}`}>
								<td style={{ border: `2px double white`, padding: 5 }}>
									{player.season}
								</td>
								<td style={{ border: `2px double white`, padding: 5 }}>
									{player.team}
								</td>
								<td style={{ border: `2px double white`, padding: 5 }}>
									{player.matches_played}
								</td>
								<td style={{ border: `2px double white`, padding: 5 }}>
									{player.starts}
								</td>
								<td style={{ border: `2px double white`, padding: 5 }}>
									{player.minutes}
								</td>
							</tr>
						))}
					</tbody>
				</table>
			</Box>
		</Box>
	);
}
