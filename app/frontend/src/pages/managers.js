import React, { useMemo } from "react";
import { useQuery } from "react-query";
import { Fragment, useState } from "react";
import {
	Container,
	CssBaseline,
	Box,
	Divider,
	Typography,
} from "@mui/material";
import { TextField, Select, MenuItem } from "@mui/material";
import { PageLoading } from "../components/loaders";
import Button from "@mui/material/Button";
import { ManagerCard } from "../components/cards";

export default function Managers() {
	const [searchTerm, setSearchTerm] = useState("");
	const [category, setCategory] = useState("manager-name");
	const [managerStartIndex, setManagerStartIndex] = useState(0);
	const [managerEndIndex, setManagerEndIndex] = useState(20);
	const [isCurrent, setIsCurrent] = useState("all");

	const handlePreviousPage = () => {
		if (managerStartIndex > 0) {
			setManagerStartIndex(managerStartIndex - 20);
			setManagerEndIndex(managerEndIndex - 20);
		}
	};

	const handleNextPage = () => {
		if (managerEndIndex < managers.length) {
			setManagerStartIndex(managerStartIndex + 20);
			setManagerEndIndex(managerEndIndex + 20);
		}
	};

	const fetchManagers = async () => {
		const response = await fetch(
			`${process.env.REACT_APP_DATA_API_ROOT}/all-managers`
		);
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	};
	const {
		isLoading: isLoadingManagers,
		error: managersError,
		data: managers = [],
	} = useQuery("managers", fetchManagers, { staleTime: Infinity });

	const handleCategoryChange = (event) => {
		setCategory(event.target.value);
	};
	const handleActiveChange = (event) => {
		setIsCurrent(event.target.value);
	};

	const handleTextSearch = (event) => {
		setSearchTerm(event.target.value);
	};

	const managerStatsSegment = useMemo(() => {
		return managers ? managers.slice(managerStartIndex, managerEndIndex) : [];
	}, [managers, managerStartIndex, managerEndIndex]);

	const filteredManagers = useMemo(() => {
		return managers.filter((manager) => {
			const fullName =
				`${manager.first_name} ${manager.last_name}`.toLowerCase();
			const teamName = manager.team_name.toLowerCase();
			const searchLower = searchTerm.toLowerCase();
			const isCurrentJob = manager.current_job;

			// Filter on category
			let categoryMatch = true; // Default to true to handle no category filter
			if (category === "manager-name") {
				categoryMatch = fullName.includes(searchLower);
			} else if (category === "team-name") {
				categoryMatch = teamName.includes(searchLower);
			}

			// Filter on isCurrent
			let isCurrentMatch = true; // Default to true to handle "all"
			if (isCurrent === "true") {
				isCurrentMatch = isCurrentJob;
			} else if (isCurrent === "false") {
				isCurrentMatch = !isCurrentJob;
			}

			// Combine conditions: both must be true to include the manager
			return categoryMatch && isCurrentMatch;
		});
	}, [managers, searchTerm, category, isCurrent]);

	return (
		<Fragment>
			<Container component="main">
				<CssBaseline />
				<Box
					sx={{
						display: "flex",
						flexDirection: "column",
						alignItems: "center",
					}}
				>
					<Box sx={{ width: "100%", overflow: "hidden", overflowY: "scroll" }}>
						<Divider sx={{ width: "100%", height: 2 }} />
						<Container
							sx={{
								marginTop: 2,
								marginBottom: 2,
								width: "100%",
								display: "flex",
								justifyContent: "center",
							}}
						>
							<Box
								sx={{
									width: "20%",
									display: "flex",
									justifyContent: "center",
								}}
							>
								<Select
									id="category-select"
									variant="outlined"
									value={category}
									onChange={handleCategoryChange}
									sx={{ width: "100%", marginLeft: 2 }}
									labelId="category-select-label"
									label="Filter by"
								>
									<MenuItem value="manager-name">Name</MenuItem>
									<MenuItem value="team-name">Team</MenuItem>
								</Select>
							</Box>
							<Box
								sx={{
									width: "80%",
									display: "flex",
									justifyContent: "center",
								}}
							>
								<TextField
									id="search-text"
									label="Search"
									variant="outlined"
									sx={{ width: "90%" }}
									onChange={handleTextSearch}
								/>
								<Select
									sx={{ textAlign: "center", width: "15%" }}
									label={"Status"}
									labelId="is-active"
									id="is-active"
									onChange={handleActiveChange}
									value={isCurrent}
								>
									<MenuItem value="all">All</MenuItem>
									<MenuItem value="true">Current</MenuItem>
									<MenuItem value="false">Former</MenuItem>
								</Select>
							</Box>
						</Container>
						<Divider sx={{ width: "100%", height: 2 }} />
						<Divider sx={{ width: "100%", height: 2 }} />
					</Box>
					<Box
						id="managers"
						sx={{
							width: "100%",
							overflowY: "scroll",
							height: "61vh",
							alignItems: "center",
						}}
					>
						{searchTerm === "" && isCurrent === "all" ? (
							managerStatsSegment.map((manager) => (
								<ManagerCard
									key={manager.id}
									managerName={`${manager.first_name} ${manager.last_name}`}
									managerId={manager.id}
									teamName={manager.team_name}
									currentJob={manager.current_job}
									startDate={manager.start_date}
									endDate={manager.end_date}
									teamId={manager.team_id}
								/>
							))
						) : isCurrent !== "all" && filteredManagers.length > 0 ? (
							filteredManagers.map((manager) => (
								<ManagerCard
									key={manager.id}
									managerName={`${manager.first_name} ${manager.last_name}`}
									managerId={manager.id}
									teamName={manager.team_name}
									currentJob={manager.current_job}
									startDate={manager.start_date}
									endDate={manager.end_date}
									teamId={manager.team_id}
								/>
							))
						) : searchTerm !== "" && filteredManagers.length > 0 ? (
							filteredManagers.map((manager) => (
								<ManagerCard
									key={manager.id}
									managerName={`${manager.first_name} ${manager.last_name}`}
									managerId={manager.id}
									teamName={manager.team_name}
									currentJob={manager.current_job}
									startDate={manager.start_date}
									endDate={manager.end_date}
									teamId={manager.team_id}
								/>
							))
						) : searchTerm !== "" &&
						  filteredManagers.length === 0 &&
						  !isLoadingManagers ? (
							<Typography
								variant="h3"
								sx={{
									width: "100%",
									textAlign: "center",
									height: "100%",
									alignItems: "center",
									alignContent: "center",
								}}
							>
								No managers found
							</Typography>
						) : (
							<PageLoading />
						)}
						{
							managersError && (
								<Typography
									variant="h3"
									sx={{
										width: "100%",
										textAlign: "center",
										height: "100%",
										alignItems: "center",
										alignContent: "center",
									}}
								>
									{managersError.message}
								</Typography>
							)
						}
					</Box>
					<Box sx={{ width: "100%" }}>
						<Divider sx={{ width: "100%" }} />
						<Box sx={{ display: "flex", justifyContent: "center", margin: 2 }}>
							{managerStartIndex > 0 && !searchTerm ? (
								<Button variant="outlined" onClick={handlePreviousPage}>
									Previous
								</Button>
							) : (
								""
							)}
							{managerEndIndex < managers.length &&
							!searchTerm &&
							isCurrent === "all" ? (
								<Button variant="outlined" onClick={handleNextPage}>
									Next
								</Button>
							) : (
								""
							)}
						</Box>
					</Box>
				</Box>
			</Container>
		</Fragment>
	);
}
