import React, { useEffect, useState } from 'react';
import { useQuery } from 'react-query';
import { Drawer, List, ListItem, ListItemText, Checkbox, FormGroup, FormControlLabel, IconButton, Box } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu'; // For the toggle button
import ArrowCircleLeftIcon from '@mui/icons-material/ArrowCircleLeft';
import ArrowCircleRightIcon from '@mui/icons-material/ArrowCircleRight';
import { MenuItem, Select } from '@mui/material';
import { TextField } from '@mui/material';
import { infinity } from 'ldrs';

export const ColumnsSidebar = (props) => {

	const { selectedEntity, checked, setChecked } = props;

    const [columns, setColumns] = useState([]);
	const [searchTerm, setSearchTerm] = useState('');
	const [filteredColumns, setFilteredColumns] = useState([]);
	const [open, setOpen] = useState(false); // State to handle sidebar open/close
	const [stats, setStats] = useState([]);

	useEffect(() => {
		if (selectedEntity !== "") {
			fetch(`${process.env.REACT_APP_DATA_API_ROOT}/vis/${selectedEntity === "player" ? "player-columns" : (selectedEntity === "team" ? "team-columns" : "")}`)
				.then(response => response.json())
				.then(data => {
					if (!Array.isArray(data)) {
						throw new Error(`${data}`);
					}
					setColumns(data);
					const initialCheckState = {};
					data.forEach(column => {
						initialCheckState[column] = false;
					});
					setChecked(initialCheckState);
				})
				.catch(error => console.error('Error fetching player columns:', error))
		};
	}, [selectedEntity]);

	useEffect(() => {
        if (searchTerm) {
            const filtered = columns.filter(entity =>
                entity.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setFilteredColumns(filtered);
        } else {
            setFilteredColumns(columns);
        }
    }, [searchTerm, columns]);

    const handleToggle = (value) => {
        setChecked(prev => ({ ...prev, [value]: !prev[value] }));
    };

    const toggleDrawer = () => {
        setOpen(!open);
    };

	return (
		<Box
			sx={{
				width: open ? 280 : 68, // Adjust width based on state, 48px enough to show icon only
				height: open ? 480 : 68, // Hide sidebar when closed
				overflowX: 'scroll', // Hide content when drawer is closed
				overflowY: 'scroll', // Hide content when drawer is closed
				transition: 'all 0.3s ease-in-out',
				border: '1px solid white',
				paddingLeft: open ? 1 : 0,
				paddingRight: open ? 1 : 0,
				bgcolor: 'background.paper',
			}}
		>
			<Box
				sx={{
					display: 'flex',
					flexDirection: 'row',
					width: '100%', // Fixed width for the button
					justifyContent: 'flex-end', // Center the icon button
					transition: 'all 0.3s ease-in-out',
					position: 'sticky', // Changed from absolute to fixed for viewport-based positioning
					top: "0",
					bgcolor: 'background.paper',
					borderBottom: '1px solid white',
					zIndex: 1,
					padding: 1,
					alignItems: 'center',
				}}
			>
				<Box sx={{flexGrow:1, alignItems:"center", justifyContent: "center", alignContent: "center"}}>
					{columns && open && <TextField
						label="Search"
						variant="outlined"
						fullWidth
						onChange={(event) => setSearchTerm(event.target.value)}
					/>}
				</Box>
				<Box>
					<IconButton
						onClick={toggleDrawer}
						sx={{
							justifyContent: 'center',
						}}
					>
						{open ? <ArrowCircleLeftIcon fontSize='large' /> : <ArrowCircleRightIcon fontSize='large' />}
					</IconButton>
				</Box>
			</Box>
			<List>
				{filteredColumns.map((column, index) => (
					<ListItem key={index} disablePadding>
						<FormGroup>
							<FormControlLabel
								control={
									<Checkbox
										checked={checked[column]}
										onChange={() => handleToggle(column)}
										name={column}
									/>
								}
								label={<ListItemText primary={column.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())} />}
							/>
						</FormGroup>
					</ListItem>
				))}
			</List>
		</Box>
	);
};


export const EntitySidebar = (props) => {
	const { selectedEntity, checked, setChecked } = props;
	const [filteredEntities, setFilteredEntities] = useState([]);
	const [open, setOpen] = useState(false); // State to handle sidebar open/close
	const [searchTerm, setSearchTerm] = useState('');

	const fetchEntities = async (entityType) => {
        const response = await fetch(`${process.env.REACT_APP_DATA_API_ROOT}/${entityType}s`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    };

    const { data: entities = [], isLoading, isError, error } = useQuery(
        ['entities', selectedEntity], // The first parameter is a unique key for the query
        () => fetchEntities(selectedEntity), // The query function that fetches the data
        {
            enabled: !!selectedEntity, // Only run the query if `selectedEntity` is truthy
            staleTime: infinity, // Adjust based on desired freshness (example: 5 minutes)
            cacheTime: infinity, // How long to keep unused data in cache (example: 15 minutes)
            onError: (err) => console.error(`Error fetching ${selectedEntity} columns:`, err),
            // Optionally, specify initial data or placeholders
            // initialData: [],
            // placeholderData: [],
        }
    );

    // Setup initial check state once data is loaded
    useEffect(() => {
        if (entities) {
            const initialCheckState = {};
            entities.forEach(column => {
                initialCheckState[column.id] = false;
            });
            setChecked(initialCheckState);
        }
    }, [entities]);

	useEffect(() => {
        if (searchTerm) {
            const filtered = entities.filter(entity =>
                `${entity.first_name} ${entity.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setFilteredEntities(filtered);
        } else {
            setFilteredEntities(entities);
        }
    }, [searchTerm, entities]);

	const handleToggle = (value) => {
		setChecked(prev => ({ ...prev, [value]: !prev[value] }));
	};

	const toggleDrawer = () => {
		setOpen(!open);
	};

	return (
		<Box
			sx={{
				width: open ? 280 : 68, // Adjust width based on state, 48px enough to show icon only
				height: open ? 480 : 68, // Hide sidebar when closed
				overflowX: 'scroll', // Hide content when drawer is closed
				overflowY: 'scroll',
				transition: 'all 0.3s ease-in-out',
				border: '1px solid white',
				paddingLeft: open ? 1 : 0,
				paddingRight: open ? 1 : 0,
				bgcolor: 'background.paper',
			}}
		>
			<Box sx={{
				display: 'flex',
				flexDirection: 'row',
				width: '100%', // Fixed width for the button
				justifyContent: 'flex-start', // Center the icon button
				transition: 'all 0.3s ease-in-out',
				position: 'sticky', // Changed from absolute to fixed for viewport-based positioning
				top: "0",
				bgcolor: 'background.paper',
				borderBottom: '1px solid white',
				zIndex: 1,
				padding: 1,
				alignItems: 'center',
			}}>
				<IconButton
					onClick={toggleDrawer}
					sx={{
						 // Fixed width for the button
						justifyContent: 'center', // Center the icon button
					}}
				>
					{open ? <ArrowCircleRightIcon fontSize='large' /> : <ArrowCircleLeftIcon fontSize='large' /> }
				</IconButton>
				<Box sx={{flexGrow:1, alignItems:"center", justifyContent: "center", alignContent: "center"}}
				>
					{entities && open && <TextField
						label="Search"
						variant="outlined"
						fullWidth
						onChange={(event) => setSearchTerm(event.target.value)}
					/>}
				</Box>
			</Box>
			<List>
				{entities && filteredEntities.map((entity, index) => (
					<ListItem key={index} disablePadding>
						<FormGroup>
							<FormControlLabel
								control={
									<Checkbox
										checked={checked[entity.id]}
										onChange={() => handleToggle(entity.id)}
										name={entity.id}
									/>
								}
								label={<ListItemText primary={selectedEntity === "team" ? entity.name : `${entity.first_name} ${entity.last_name}`} />}
							/>
						</FormGroup>
					</ListItem>
				))}
			</List>
		</Box>
	);
};