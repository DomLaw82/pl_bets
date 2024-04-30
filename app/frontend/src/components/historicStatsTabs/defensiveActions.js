

export default function DefensiveActions(props) {
	const { historicStats } = props;
	
	const defensiveActions = [
		"season",
		"tackles_per_90",
		"tackles_won_per_90",
		"defensive_third_tackles_per_90",
		"middle_third_tackles_per_90",
		"attacking_third_tackles_per_90",
		"dribblers_tackled_per_90",
		"dribbler_tackles_attempted_per_90",
		"shots_blocked_per_90",
		"passes_blocked_per_90",
		"interceptions_per_90",
		"clearances_per_90",
		"errors_leading_to_shot_per_90"
	]


	return (
		<table>
			<thead>
				<tr>
					{defensiveActions.map((stat) => (
						<th key={stat}>{stat}</th>
					))}
				</tr>
			</thead>
			<tbody>
				{historicStats.map((season) => (
					<tr key={season.season}>
						{defensiveActions.map((stat) => (
							<td key={`${stat}-value`}>{season[stat]}</td>
						))}
					</tr>
				))}
			</tbody>
		</table>
	);
}