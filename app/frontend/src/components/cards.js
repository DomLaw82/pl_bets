import React, { Fragment, useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActionArea from '@mui/material/CardActionArea';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import Divider from '@mui/material/Divider';

const predictionResultColumns = ["goals", "shots", "shots_on_target", "corners", "fouls", "yellow_cards", "red_cards"]

export function PlayerCards(props) {
    const { playerId, firstName, lastName, birthDate, position, teamName, badge, setModalPlayer } = props;

    const handleCardClick = (event, playerId) => {
        setModalPlayer(event, playerId);
      };
    
    return (
        <Fragment>
            <Card sx={{ margin: 2 }} variant="outlined">
                <CardActionArea onClick={ (event) => handleCardClick(event, playerId) }>
                    <CardContent>
                        <Box sx={{
                            display: 'flex',
                            flexDirection: 'row',
                            justifyContent: 'space-evenly',
                            alignItems: "center"
                        }}>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "30%"}}>
                                <Typography className={"player-name"} variant="h5" component="div">
                                    {firstName} {lastName}
                                </Typography>
                            </Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "30%"}}>
                                <Typography className={"player-dob"} variant="body1">
                                    DOB: {birthDate}
                                </Typography>
                            </Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "30%"}}>
                                <Typography className={"player-position"} variant="body1">
                                    Position: {position}
                                </Typography>
                            </Box>
                            <Box sx={{ alignItems: "center", height: 60}}>
                                <img className={"player-team"} src={badge} alt={teamName} height="60" />
                            </Box>
                        </Box>
                    </CardContent>
                </CardActionArea>
            </Card>
        </Fragment>
	)
}

export function PredictionPlayerCards(props) {

    const { firstName, lastName, position } = props;

    return (
        <Fragment>
            <Card sx={{ margin: 2 }} variant="outlined">
                <CardActionArea>
                    <CardContent>
                        <Box sx={{
                            display: 'flex',
                            flexDirection: 'row',
                            justifyContent: 'space-evenly',
                            alignItems: "center"
                        }}>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "30%"}}>
                                <Typography variant="body5" component="div">
                                    {firstName} {lastName}
                                </Typography>
                            </Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "30%"}}>
                                <Typography variant="body5">
                                    Position: {position}
                                </Typography>
                            </Box>
                        </Box>
                    </CardContent>
                </CardActionArea>
            </Card>
        </Fragment>
	)
}

export function MatchCards(props) {
    const { gameWeek, date, homeTeam, awayTeam, result, handleOpenMatchFactsModal, homeWinProb, awayWinProb, drawProb, prediction, futureMatch } = props;
    
    return (
        <Fragment>
            <Card sx={{ margin: 2 }} variant="outlined">
                <CardActionArea onClick={(event) => {
                    if (!futureMatch) {
                        handleOpenMatchFactsModal(event, date, homeTeam, awayTeam)
                    }
                }
                }>
                    <CardContent>
                        <Box sx={{
                            display: 'flex',
                            flexDirection: 'row',
                            justifyContent: 'space-between'
                        }}>
                            <Box sx={{width:"70%"}}>
                                <Typography variant="h5" component="div">
                                    {homeTeam} vs {awayTeam}
                                </Typography>
                                <Typography variant="body2">
                                    Date: {date}
                                </Typography>
                                <Typography variant="body2">
                                    Game Week: {gameWeek}
                                </Typography>
                            </Box>
                            {
                                homeWinProb && awayWinProb && drawProb &&
                                <Box sx={{width:"20%", alignItems: "center"}}>
                                    <Typography variant="body2" color={homeWinProb > drawProb && homeWinProb > awayWinProb ? "green" : "white"}>
                                        Home: {(homeWinProb*100).toPrecision(3)}%
                                    </Typography>
                                    <Typography variant="body2" color={awayWinProb > drawProb && awayWinProb > homeWinProb ? "green" : "white"}>
                                        Away: {(awayWinProb*100).toPrecision(3)}%
                                    </Typography>
                                    <Typography variant="body2" color={drawProb > awayWinProb && drawProb > homeWinProb ? "green" : "white"}>
                                        Draw: {(drawProb*100).toPrecision(3)}%
                                    </Typography>
                                </Box>
                            }
                            {
                                !homeWinProb && !awayWinProb && !drawProb &&
                                <Box sx={{ alignContent: "center", width:"10%" }}>
                                    <Typography variant="h5">
                                        {result}
                                    </Typography>
                                </Box>
                            }
                            {
                                result === "-" && homeWinProb && awayWinProb && drawProb &&
                                <Box sx={{ alignContent: "center", width:"10%" }}>
                                    <Typography variant="h3">
                                        {prediction}
                                    </Typography>
                                </Box>
                            }
                        </Box>
                    </CardContent>
                    <Divider sx={{ width: '100%', height: 2 }} />
                </CardActionArea>
            </Card>
        </Fragment>
    );
}

export function TeamCards(props) {
    const { teamName, teamLogo } = props;

    return (
        <Fragment>
            <Card sx={{ margin: 2}} variant="outlined">
                <CardActionArea>
                    <CardContent>
                        <Box sx={{
                            display: 'flex',
                            flexDirection: 'row',
                            justifyContent: 'space-evenly',
                            alignItems: "center"
                        }}>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "60%"}}>
                                <Typography variant="h4" component="div">
                                    {teamName}
                                </Typography>
                            </Box>
                            <Box sx={{ alignContent: "center", textAlign: "center", width: "40%"}}>
                                <img src={teamLogo} alt={teamName} height={50} />
                            </Box>
                        </Box>
                    </CardContent>
                </CardActionArea>
            </Card>
        </Fragment>
    );
}

export function PredictionOutputCard(props) {
    const { homeTeam, awayTeam, predictionOutput } = props;

    return (
        <Fragment>
            <Card sx={{ margin: 2, width: "100%" }} variant="outlined">
                <CardContent sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-evenly',
                    alignItems: "center",
                }}>
                    <Box sx={{alignItems: "center", width: "100%"}}>
                        {/* <Typography variant="h4" component="div">
                            Prediction Output
                        </Typography> */}
                        <Box key={"header"} sx={{display:"flex", flexDirection:"row", margin: 2}}>
                            <Box key={"home-header"} sx={{alignItems: "center", textAlign: "center", width: "32.5%"}}>
                                <Typography variant="h4" component="div">
                                    {homeTeam}
                                </Typography>
                            </Box>
                            <Box sx={{width: "35%", alignItems: "center", textAlign: "center"}}>
                                <Typography variant="h5" component="div">
                                        <span> vs </span>
                                </Typography>
                            </Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "32.5%"}}>
                                <Typography variant="h4" component="div">
                                    {awayTeam}
                                </Typography>
                            </Box>
                        </Box>

                        {predictionOutput && predictionResultColumns.map((column, index) => {
                            return (
                                <Box key={`data-${index}`} sx={{ display: "flex", flexDirection: "row" }}>
                                    <Box key={`home_${column}`} sx={{ alignItems: "center", textAlign: "center", width: "32.5%" }}>
                                        <Typography variant="body1" component="div">
                                            {predictionOutput[`home_${column}`]}
                                        </Typography>
                                    </Box>
                                    <Divider orientation="vertical" flexItem />
                                    <Box key={`title_${column}`} sx={{ alignItems: "center", textAlign: "center", width: "35%" }}>
                                        <Typography variant="h6" component="div">
                                            {`${column}`.replace(/_/g, " ").replace(/\w\S*/g, text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase())}
                                        </Typography>
                                    </Box>
                                    <Divider orientation="vertical" flexItem />
                                    <Box key={`away_${column}`} sx={{ alignItems: "center", textAlign: "center", width: "32.5%" }}>
                                        <Typography variant="body1" component="div">
                                            {predictionOutput[`away_${column}`]}
                                        </Typography>
                                    </Box>
                                </Box>
                            )
                        })}
                    </Box>
                </CardContent>
            </Card>
        </Fragment>
    )
}

export function PredictionHistoryCard(props) {
    const { homeTeam, awayTeam, data } = props;
    const [viewPrediction, setViewPrediction] = useState(false);
    const [displaySettings, setDisplaySettings] = useState("none");

    useEffect(() => {
        if (viewPrediction) {
            setDisplaySettings("flex");
        } else {
            setDisplaySettings("none");
        }
    }, [viewPrediction])

    return (
        <Fragment>
            <Card key={`${homeTeam}-${awayTeam}`} sx={{ margin: .5, width: "100%" }} variant="outlined">
            <CardActionArea  onClick={(event) => setViewPrediction(!viewPrediction)}>
                    <CardContent sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'space-evenly',
                        alignItems: "center"
                    }}>
                        <Box sx={{alignItems: "center", width: "100%"}}>
                            <Box sx={{display:"flex", flexDirection:"row", justifyContent: "space-evenly", textAlign: "center"}}>
                                <Typography variant="h5" component="div" sx={{width: "32.5%" }}>
                                    {homeTeam}
                                </Typography>
                                <Typography variant="h5" component="div" sx={{width: "35%" }}>
                                    <span> vs </span>
                                </Typography>
                                <Typography variant="h5" component="div" sx={{width: "32.5%" }}>
                                    {awayTeam}
                                </Typography>
                            </Box>
                            {
                                viewPrediction && <Divider sx={{ width: '100%', height: 2 }} />
                            }
                            <Box sx={{display:displaySettings, flexDirection:"column", justifyContent: "space-evenly", textAlign: "center"}}>
                                {
                                    viewPrediction && predictionResultColumns.map((column, index) => {
                                        return (
                                            <Box key={column} sx={{ display: "flex", flexDirection: "row" }}>
                                                <Box sx={{ alignItems: "center", textAlign: "center", width: "32.5%" }}>
                                                    <Typography variant="body1" component="div">
                                                        {data[`home_${column}`]}
                                                    </Typography>
                                                </Box>
                                                <Divider orientation="vertical" flexItem />
                                                <Box sx={{ alignItems: "center", textAlign: "center", width: "35%" }}>
                                                    <Typography variant="h6" component="div">
                                                        {`${column}`.replace(/_/g, " ").replace(/\w\S*/g, text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase())}
                                                    </Typography>
                                                </Box>
                                                <Divider orientation="vertical" flexItem />
                                                <Box sx={{ alignItems: "center", textAlign: "center", width: "32.5%" }}>
                                                    <Typography variant="body1" component="div">
                                                        {data[`away_${column}`]}
                                                    </Typography>
                                                </Box>
                                            </Box>
                                        )
                                    })}
                            </Box>
                        </Box>
                    </CardContent>
                </CardActionArea>
            </Card>
        </Fragment>
    );
}
                       