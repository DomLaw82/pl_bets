import { useState, Fragment, useMemo } from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import Typography from "@mui/material/Typography";
import { Divider, Select } from "@mui/material";
import { PlayerCards } from "../components/cards";
import { PlayerStatsModal } from "../components/modals";
import Button from "@mui/material/Button";
import { useQuery } from "react-query";
import { QueryClientProvider } from "react-query";
import { PageLoading } from "../components/loaders";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";

export default function Players(props) {
    const [isPlayerStatsModalOpen, setIsPlayerStatsModalOpen] = useState(false);
    const [modalPlayerId, setModalPlayerId] = useState("");
    const [modalOriginX, setModalOriginX] = useState(0);
    const [modalOriginY, setModalOriginY] = useState(0);
    const [playerStartIndex, setPlayerStartIndex] = useState(0);
    const [playerEndIndex, setPlayerEndIndex] = useState(20);

    const [searchTerm, setSearchTerm] = useState('');
    const [category, setCategory] = useState('player-name');

    const { queryClient } = props;

    const fetchPlayers = async () => {
        const response = await fetch(
            `${process.env.REACT_APP_DATA_API_ROOT}/all-active-players`
        );
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    };

    const {
        isLoading: isLoadingPlayers,
        // error: playersError,
        data: players = [],
    } = useQuery(
        "players",
        fetchPlayers,
        { staleTime: Infinity }
    );

    const handlePreviousPage = () => {
        if (playerStartIndex > 0) {
            setPlayerStartIndex(playerStartIndex - 20);
            setPlayerEndIndex(playerEndIndex - 20);
        }
    };

    const handleNextPage = () => {
        if (playerEndIndex < players.length) {
            setPlayerStartIndex(playerStartIndex + 20);
            setPlayerEndIndex(playerEndIndex + 20);
        }
    };

    // Function to fetch player stats
    const fetchPlayerData = async (playerId) => {
        const response = await fetch(
            `${process.env.REACT_APP_DATA_API_ROOT}/players/historic-stats/${playerId}`
        );
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    };
    
    const fetchPlayerProfile = async (playerId) => {
        const response = await fetch(
            `${process.env.REACT_APP_DATA_API_ROOT}/players/player-profile/${playerId}`
        );
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    }

    const {
        data: historicStats = {},
        isLoading: isLoadingHistoricStats,
        // error: historicStatsError,
    } = useQuery(
        ["playerHistoricStats", modalPlayerId],
        () => fetchPlayerData(modalPlayerId),
        {
            enabled: !!modalPlayerId && modalOriginX !== 0 && modalOriginY !== 0,
            onSuccess: (data) => {
                if (data.length > 0) {
                    setIsPlayerStatsModalOpen(true);
                }
            },
        }
    );

    const {
        data: playerProfile = [],
        isLoading: isLoadingPlayerProfile,
        // error: playerProfileError,
    } = useQuery(
        ["playerProfile", modalPlayerId],
        () => fetchPlayerProfile(modalPlayerId),
        {
            enabled: !!modalPlayerId && modalOriginX !== 0 && modalOriginY !== 0,
            onSuccess: (data) => {
                if (data.length > 0) {
                    setIsPlayerStatsModalOpen(true);
                }
            }
        }
    );

    const closePlayerStatsModal = () => {
        setIsPlayerStatsModalOpen(false);
        setModalPlayerId("");
    };

    const setModalPlayer = (event, playerId) => {
        setModalOriginX(event.clientX);
        setModalOriginY(event.clientY);
        setModalPlayerId(playerId);
    };

    const playerStatsSegment = useMemo(() => {
        return players ? players.slice(playerStartIndex, playerEndIndex) : [];
    }, [players, playerStartIndex, playerEndIndex]);
    
    
    const handleCategoryChange = (event) => {
        setCategory(event.target.value);
    };

    const handleTextSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    const filteredPlayers = useMemo(() => {
        return players.filter(player => {
            const fullName = `${player.first_name} ${player.last_name}`;
            if (category === "player-name") {
                return (
                    player.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    player.last_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
                    fullName.toLowerCase().includes(searchTerm.toLowerCase()
                );
            } else if (category === "position") {
                return player.position.toLowerCase().includes(searchTerm.toLowerCase());
            } else if (category === "team-name") {
                return player.team_name.toLowerCase().includes(searchTerm.toLowerCase());
            }
            return false;
        });
    }, [players, searchTerm, category]);

    if (isLoadingPlayers)
        return (
            <PageLoading />
        );
    // if (playersError) console.alert(playersError);
    // if (historicStatsError) console.alert(historicStatsError);
    // if (playerProfileError) console.alert(playerProfileError);

    return (
        <QueryClientProvider client={queryClient}>
            <Fragment>
                <Container
                    component="main"
                >
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
                            <Container sx={{ marginTop: 2, marginBottom: 2, width: "100%", display: "flex", justifyContent: "center" }}>
                                <Box sx={{ width: "80%", display: "flex", justifyContent: "center" }}>
                                    <TextField id="search-text" label="Search" variant="outlined" sx={{ width: "90%" }} onChange={handleTextSearch} />
                                </Box>
                                <Box sx={{ width: "20%", display: "flex", justifyContent: "center" }}>
                                    <Select
                                        id="category-select"
                                        label="Categories"
                                        variant="outlined"
                                        value={category}
                                        onChange={handleCategoryChange}
                                        sx={{ width: "100%", marginLeft: 2 }}
                                    >
                                        <MenuItem value="player-name">Player Name</MenuItem>
                                        <MenuItem value="position">Position</MenuItem>
                                        <MenuItem value="team-name">Team Name</MenuItem>
                                    </Select>
                                </Box>
                            </Container>
                            <Divider sx={{ width: "100%", height: 2 }} />
                            <Divider sx={{ width: "100%", height: 2 }} />
                            <Box id="active-teams" sx={{ width: "100%", overflowY: "scroll", maxHeight: "51vh" }} >
                                {
                                    searchTerm !== "" ?
                                    filteredPlayers.map((player) => (
                                        <PlayerCards
                                            key={player.id}
                                            playerId={player.id}
                                            firstName={player.first_name}
                                            lastName={player.last_name}
                                            birthDate={player.birth_date}
                                            position={player.position}
                                            teamName={player.team_name}
                                            badge={`/logos/${player.team_name}.png`}
                                            setModalPlayer={setModalPlayer}
                                        />
                                    )) : 
                                    playerStatsSegment.map((player) => (
                                        <PlayerCards
                                            key={player.id}
                                            playerId={player.id}
                                            firstName={player.first_name}
                                            lastName={player.last_name}
                                            birthDate={player.birth_date}
                                            position={player.position}
                                            teamName={player.team_name}
                                            badge={`/logos/${player.team_name}.png`}
                                            setModalPlayer={setModalPlayer}
                                        />
                                    ))
                                }
                            </Box>
                            <Box sx={{ width: "100%" }}>
                                <Divider sx={{ width: "100%" }} />
                                <Box
                                    sx={{ display: "flex", justifyContent: "center", margin: 2 }}
                                >   
                                    {
                                        playerStartIndex > 0 && !searchTerm ?
                                            <Button variant="outlined" onClick={handlePreviousPage}>
                                                Previous
                                            </Button> :
                                            ""
                                    }
                                    {
                                        playerEndIndex < players.length && !searchTerm ?
                                            <Button variant="outlined" onClick={handleNextPage}>
                                                Next
                                            </Button> :
                                            ""
                                    }
                                </Box>
                            </Box>
                        </Box>
                    </Box>
                    <PlayerStatsModal
                        isOpen={isPlayerStatsModalOpen}
                        setIsOpen={setIsPlayerStatsModalOpen}
                        historicStats={historicStats}
                        closePlayerStatsModal={closePlayerStatsModal}
                        originX={modalOriginX}
                        originY={modalOriginY}
                        playerProfile={playerProfile}
                        isLoadingPlayerProfile={isLoadingPlayerProfile}
                        isLoadingHistoricStats={isLoadingHistoricStats}
                    />
                </Container>
            </Fragment>
        </QueryClientProvider>
    );
}
