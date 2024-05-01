import { Box, Tooltip } from "@mui/material";

export default function HistoricStatsTabTemplate(props) {
	const { historicStats, statHeadings, key } = props;

	return (
		<Box key={key} sx={{ display: 'flex', justifyContent: 'center', margin: 2 }}>
			<table style={{ borderCollapse: "collapse", textAlign: "center" }}>
				<thead>
					<tr style={{ border: `4px solid white` }}>
						{statHeadings.map((stat) => (
							<Tooltip title={stat.replace(/_per_90/g, "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())} placement="top">
								<th key={stat} style={{ border: `4px solid white`, padding: 5 }}>
									{stat.replace(/_per_90/g, "").split('_').map(word => word.charAt(0).toUpperCase()).join('')}
								</th>
							</Tooltip>
						))}
					</tr>
				</thead>
				<tbody>
					{historicStats.map((season) => (
						<tr key={season.season} style={{ border: `2px double white` }}>
							{statHeadings.map((stat) => (
								<td key={`${stat}-value`} style={{ border: `2px double white`, padding: 5 }}>
									{season[stat]}
								</td>
							))}
						</tr>
					))}
				</tbody>
			</table>
		</Box>
	);
}