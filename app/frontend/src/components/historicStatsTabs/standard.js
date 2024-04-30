

export default function Standard(props) {
	const { historicStats } = props;
	
	const standard = [
		"season",
		"goals_per_90",
		"assists_per_90",
		"direct_goal_contributions_per_90",
		"non_penalty_goals_per_90",
		"penalties_scored_per_90",
		"penalties_attempted_per_90",
		"yellow_cards_per_90",
		"red_cards_per_90",
		"expected_goals_per_90",
		"non_penalty_expected_goals_per_90",
		"expected_assisted_goals_per_90",
		"non_penalty_expected_goals_plus_expected_assisted_goals_per_90",
		"progressive_carries_per_90"
	];


	return (
		<table>
			<thead>
				<tr>

					{standard.map((stat) => (
						<th key={stat}>{stat}</th>
					))}
				</tr>
			</thead>
			<tbody>
				{historicStats.map((season) => (
					<tr key={season.season}>
						{standard.map((stat) => (
							<td key={`${stat}-value`}>{season[stat]}</td>
						))}
					</tr>
				))}
			</tbody>
		</table>
	);
}