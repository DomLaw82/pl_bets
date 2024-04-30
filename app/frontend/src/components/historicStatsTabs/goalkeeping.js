

export default function Goalkeeping(props) {
	const { historicStats } = props;
	
	const goalkeeping = [
		"season",
		"goals_against_per_90",
		"shots_on_target_against_per_90",
		"saves_per_90",
		"clean_sheets_per_90",
		"penalties_faced_per_90",
		"penalties_allowed_per_90",
		"penalties_saved_per_90",
		"penalties_missed_per_90"
	];

	return (
		<table>
			<thead>
				<tr>

					{goalkeeping.map((stat) => (
						<th key={stat}>{stat}</th>
					))}
				</tr>
			</thead>
			<tbody>
				{historicStats.map((season) => (
					<tr key={season.season}>
						{goalkeeping.map((stat) => (
							<td key={`${stat}-value`}>{season[stat]}</td>
						))}
					</tr>
				))}
			</tbody>
		</table>
	);
}