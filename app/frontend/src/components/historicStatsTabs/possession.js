

export default function Possession(props) {
	const { historicStats } = props;
	
	const possession = [
		"season",
		"touches_per_90",
		"touches_in_defensive_penalty_area_per_90",
		"touches_in_defensive_third_per_90",
		"touches_in_middle_third_per_90",
		"touches_in_attacking_third_per_90",
		"touches_in_attacking_penalty_area_per_90",
		"live_ball_touches_per_90",
		"take_ons_attempted_per_90",
		"take_ons_succeeded_per_90",
		"times_tackled_during_take_on_per_90",
		"carries_per_90",
		"total_carrying_distance_per_90",
		"progressive_carrying_distance_per_90",
		"carries_into_final_third_per_90",
		"carries_into_penalty_area_per_90",
		"miscontrols_per_90",
		"dispossessed_per_90",
		"passes_received_per_90",
	]


	return (
		<table>
			<thead>
				<tr>

					{possession.map((stat) => (
						<th key={stat}>{stat}</th>
					))}
				</tr>
			</thead>
			<tbody>
				{historicStats.map((season) => (
					<tr key={season.season}>
						{possession.map((stat) => (
							<td key={`${stat}-value`}>{season[stat]}</td>
						))}
					</tr>
				))}
			</tbody>
		</table>
	);
}