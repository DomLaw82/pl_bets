import { Fragment, useState, useEffect } from "react";
import { useQuery } from "react-query";
import { Box, Typography} from "@mui/material";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import { ColumnsSidebar, EntitySidebar } from "../components/visSideBar";
import { MenuItem, Select } from "@mui/material";
import { LineChart} from "@mui/x-charts";
import { PageLoading } from "../components/loaders";
import { AppBar, Tab, Tabs } from "@mui/material";
import { TabPanel, a11yProps } from "../components/tabs";
import { animated, useTransition} from "@react-spring/web";

export default function Visualisations() {
	const [selectedEntity, setSelectedEntity] = useState("");
	const [stats, setStats] = useState({});
	const [selectedStats, setSelectedStats] = useState([]);
	const [entities, setEntities] = useState([]);
	const [xAxis, setXAxis] = useState("season");
	const [xValues, setXValues] = useState([]);
	const [yValues, setYValues] = useState([]);
	const [value, setValue] = useState(0);

	const handleChange = (event, newValue) => {
		setValue(newValue);
	};

	// fix max depth reached error
	// stat per graph, can show comparison between multiple players, teams, mini app bar to cycle through stats
	// 		x axis can be season, gameweek
	// 		y axis can be any stat
	// 		speed up page processing
	// resort lists on sidebar when entity is selected, i.e. all selected entities are at the top

	const { data: data_series = [[], {}] } = useQuery(
		["columns", stats, entities],
		async () => {
			const checked_stats = Object.keys(stats).filter(
				(key) => stats[key] === true
			);
			console.log(checked_stats);
			const checked_entities = Object.keys(entities)
				.filter((key) => entities[key] === true)
				.map((key) => `'${key}'`);
			console.log(checked_entities);

			const response = await fetch(
				`http://localhost:8080/visualisation?table_name=${selectedEntity}&stats=${checked_stats.join(
					","
				)}&entities=${checked_entities.join(",")}&per_ninety=0&x_axis=${xAxis}`
			);
			if (!response.ok) {
				return [[], []];
			}

			const data = await response.json();
			setXValues(data[0]);
			setYValues(data[1]);
			return data;
		},
		{
			enabled:
				selectedEntity !== "" &&
				Object.keys(stats).filter((key) => stats[key] === true).length > 0 &&
				Object.keys(entities)
					.filter((key) => entities[key] === true)
					.map((key) => `'${key}'`).length > 0,
			staleTime: Infinity,
		}
	);

	useEffect(() => {
		setSelectedStats(Object.keys(stats).filter((key) => stats[key] === true));
	}, [stats]);

	const transitions = useTransition(value, {
		from: { opacity: 0, transform: "translate3d(100%,0,0)" },
		enter: { opacity: 1, transform: "translate3d(0%,0,0)" },
		leave: { opacity: 0, transform: "translate3d(100%,0,0)" },
		keys: value,
	});

	return (
		<Fragment>
			<Container>
				<CssBaseline />
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Box sx={{ width: "20%", justifyContent: "center" }}>
						<Select
							value={selectedEntity}
							onChange={(event) => setSelectedEntity(event.target.value)}
							sx={{ width: "100%" }}
							id="entity-select"
						>
							<MenuItem value="" key={"empty-entity"}></MenuItem>
							<MenuItem value="player" key={"player-entity"}>
								Player
							</MenuItem>
							<MenuItem value="team" key={"team-entity"}>
								Team
							</MenuItem>
						</Select>
					</Box>
					<AppBar position="static">
						<Tabs
							value={value}
							onChange={handleChange}
							indicatorColor="secondary"
							textColor="inherit"
							variant="fullWidth"
							aria-label="full width tabs"
						>
							{selectedStats.map((tab, index) => (
								<Tab
									key={index}
									label={tab}
									sx={{
										whiteSpace: "nowrap",
										overflow: "hidden",
										textOverflow: "hidden",
									}}
									{...a11yProps(index)}
								/>
							))}
						</Tabs>
					</AppBar>
					{selectedEntity && stats && entities ? (
						<Box
							sx={{
								maxHeight: "65vh",
								width: "100%",
								display: "flex",
								justifyContent: "space-between",
								overflowY: "scroll",
								paddingTop: 1,
							}}
						>
							<ColumnsSidebar
								selectedEntity={selectedEntity}
								checked={stats}
								setChecked={setStats}
							/>
							<Box
								sx={{
									display: "flex",
									flexDirection: "column",
									overflowX: "hidden",
									justifyContent: "center",
									alignItems: "center", // Center content horizontally in the flex container
									position: "fixed", // Changed from absolute to fixed for viewport-based positioning
									top: "65%", // Position at 50% from the top of the viewport
									left: "50%", // Position at 50% from the left of the viewport
									transform: "translate(-50%, -50%)", // Adjust position to center the element exactly
									width: 1000, // Specific width for the chart
									height: 500, // Specific height for the chart
									zIndex: -10, // Ensure the chart is above other elements
								}}
							>
								{selectedStats.length > 0 &&
									xValues && Object.keys(yValues).length > 0 &&
									selectedStats.map((stat, index) => (
										<animated.div style={transitions}>
											<TabPanel value={value} index={index} key={index}>
												<LineChart
													width={1000}
													height={500}
													loading={xValues.length === 0}
													xAxis={[{ data: xValues, scaleType: "band" }]}
													series={yValues[stat].map((data) => ({
														...data,
														curve: "linear",
														valueFormatter: (value) =>
															value == null ? "?" : value.toString(),
													}))}
													yAxis={[{ min: 0, scaleType: "linear" }]}
												/>
											</TabPanel>
										</animated.div>
									))
								}
							</Box>
							<EntitySidebar
								selectedEntity={selectedEntity}
								checked={entities}
								setChecked={setEntities}
							/>
						</Box>
					) : (
						<Box>
							<Typography variant="h3" sx={{ marginTop: "10%" }}>
								Select an entity type to graph
							</Typography>
							<PageLoading />
						</Box>
					)}
				</Box>
			</Container>
		</Fragment>
	);
}
