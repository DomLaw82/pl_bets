import React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import Divider from '@mui/material/Divider';


export function PlayerCards(props) {

    const { id, firstName, lastName, birthDate, position } = props;

	return (
        <Card sx={{ margin: 2 }} variant="outlined">
            <CardContent>
                <Box sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'space-evenly',
                    alignItems: "center"
                }}>
                    <Box sx={{alignItems: "center", textAlign: "center", width: "33%"}}>
                        <Typography variant="h5" component="div">
                            {firstName} {lastName}
                        </Typography>
                    </Box>
                    <Box sx={{alignItems: "center", textAlign: "center", width: "33%"}}>
                        <Typography variant="body1">
                            DOB: {birthDate}
                        </Typography>
                    </Box>
                    <Box sx={{alignItems: "center", textAlign: "center", width: "33%"}}>
                        <Typography variant="body1">
                            Position: {position}
                        </Typography>
                    </Box>
                </Box>
            </CardContent>
        </Card>
	)
}

export function MatchCards(props) {
    const { gameWeek, date, homeTeam, awayTeam, result, handleOpenMatchFactsModal } = props;
    
    return (
        <Card sx={{ margin: 2 }} variant="outlined">
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
            <CardActions sx={{ justifyContent: "center" }}>
                <Button size="small" onClick={() => handleOpenMatchFactsModal(date, homeTeam, awayTeam)}>View Match Facts</Button>
            </CardActions>
        </Card>
    );
}

export function TeamCards(props) {
    const { teamName, teamLogo } = props;

    return (
        <Card sx={{ margin: 2, minWidth: "70%" }} variant="outlined">
            <CardContent>
                <Box sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'space-between',
                    alignItems: "center"
                }}>
                    <Box sx={{alignItems: "center"}}>
                        <Typography variant="h4" component="div">
                            {teamName}
                        </Typography>
                    </Box>
                    <Box sx={{ alignContent: "center" }}>
                        <img src={teamLogo} alt={teamName} />
                    </Box>
                </Box>
            </CardContent>
        </Card>
    );
}
