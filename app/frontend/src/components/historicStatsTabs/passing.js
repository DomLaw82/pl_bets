

export default function Passing(props) {
	const { historicStats } = props;
	
	const passing = [
		"season",
		"progressive_passes_per_90",
		"progressive_passes_received_per_90",	
		"total_passing_distance_per_90",
		"total_progressive_passing_distance_per_90",
		"short_passes_completed_per_90",
		"short_passes_attempted_per_90",
		"medium_passes_completed_per_90",
		"medium_passes_attempted_per_90",
		"long_passes_completed_per_90",
		"long_passes_attempted_per_90",
		"expected_assists_per_90",
		"assists_minus_expected_assisted_goals_per_90",
		"key_passes_per_90",
		"passes_into_final_third_per_90",
		"passes_into_penalty_area_per_90",
		"crosses_into_penalty_area_per_90"
	];

	return (
		<table>
			<thead>
				<tr>

					{passing.map((stat) => (
						<th key={stat}>{stat}</th>
					))}
				</tr>
			</thead>
			<tbody>
				{historicStats.map((season) => (
					<tr key={season.season}>
						{passing.map((stat) => (
							<td key={`${stat}-value`}>{season[stat]}</td>
						))}
					</tr>
				))}
			</tbody>
		</table>
	);
}