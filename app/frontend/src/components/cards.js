import React, { Fragment } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActionArea from '@mui/material/CardActionArea';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import Divider from '@mui/material/Divider';


const predictionResultColumns = ["goals","shots","shots_on_target","corners","fouls","yellow_cards","red_cards"]

export function PlayerCards(props) {

    const { firstName, lastName, birthDate, position, teamName, badge } = props;

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
                                <Typography variant="h5" component="div">
                                    {firstName} {lastName}
                                </Typography>
                            </Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "30%"}}>
                                <Typography variant="body1">
                                    DOB: {birthDate}
                                </Typography>
                            </Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "30%"}}>
                                <Typography variant="body1">
                                    Position: {position}
                                </Typography>
                            </Box>
                            <Box sx={{ alignItems: "center", height: 60}}>
                                <img src={badge} alt={teamName} height="60" />
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
    const { gameWeek, date, homeTeam, awayTeam, result, handleOpenMatchFactsModal } = props;
    
    return (
        <Fragment>
            <Card sx={{ margin: 2 }} variant="outlined">
            <CardActionArea  onClick={() => handleOpenMatchFactsModal(date, homeTeam, awayTeam)}>
                    <CardContent>
                        <Box sx={{
                            display: 'flex',
                            flexDirection: 'row',
                            justifyContent: 'space-between'
                        }}>
                            <Box>
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
                            <Box sx={{ alignContent: "center" }}>
                                <Typography variant="h5">
                                    {result}
                                </Typography>
                            </Box>
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
            <Card sx={{ margin: 2 }} variant="outlined">
                <CardContent sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-evenly',
                    alignItems: "center"
                }}>
                    <Box sx={{alignItems: "center", width: "100%"}}>
                        {/* <Typography variant="h4" component="div">
                            Prediction Output
                        </Typography> */}
                        <Box sx={{display:"flex", flexDirection:"row"}}>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "32.5%"}}>
                                <Typography variant="h4" component="div">
                                    {homeTeam}
                                </Typography>
                            </Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "17.5%"}}></Box>
                            <Box sx={{alignItems: "center", textAlign: "center"}}>
                                <Divider orientation="vertical" flexItem />
                            </Box>
                            <Divider orientation="vertical" flexItem />
                            <Box sx={{alignItems: "center", textAlign: "center", width: "17.5%"}}></Box>
                            <Box sx={{alignItems: "center", textAlign: "center", width: "32.5%"}}>
                                <Typography variant="h4" component="div">
                                    {awayTeam}
                                </Typography>
                            </Box>
                        </Box>

                        {predictionOutput && predictionResultColumns.map((column, index) => {
                            return (
                                <Box sx={{ display: "flex", flexDirection: "row" }}>
                                    <Box sx={{ alignItems: "center", textAlign: "center", width: "32.5%" }}>
                                        <Typography variant="body1" component="div">
                                            {predictionOutput[`home_${column}`]}
                                        </Typography>
                                    </Box>
                                    <Divider orientation="vertical" flexItem />
                                    <Box sx={{ alignItems: "center", textAlign: "center", width: "35%" }}>
                                        <Typography variant="h6" component="div">
                                            {`${column}`.toUpperCase()}
                                        </Typography>
                                    </Box>
                                    <Divider orientation="vertical" flexItem />
                                    <Box sx={{ alignItems: "center", textAlign: "center", width: "32.5%" }}>
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