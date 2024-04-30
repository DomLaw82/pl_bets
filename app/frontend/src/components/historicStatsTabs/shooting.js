

export default function Shooting(props) {
	const { historicStats } = props;
	
	const shooting = [
		"shots_per_90",
		"shots_on_target_per_90",
		"goals_per_shot_per_90",
		"goals_per_shot_on_target_per_90",
		"average_shot_distance_per_90",
		"shots_from_free_kicks_per_90",
		"penalties_made_per_90",
		"non_penalty_expected_goals_per_shot_per_90",
		"goals_minus_expected_goals_per_90",
		"non_penalty_goals_minus_non_penalty_expected_goals_per_90",
	];

	return (
		<table>
			<thead>
				<tr>

					{shooting.map((stat) => (
						<th key={stat}>{stat}</th>
					))}
				</tr>
			</thead>
			<tbody>
				{historicStats.map((season) => (
					<tr key={season.season}>
						{shooting.map((stat) => (
							<td key={`${stat}-value`}>{season[stat]}</td>
						))}
					</tr>
				))}
			</tbody>
		</table>
	);
}