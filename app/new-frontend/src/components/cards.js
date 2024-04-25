import React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';


export function TeamCards(team) {
	return (
		<Card></Card>
	)
}

export function PlayerCards(player) {
	return (
		<Card></Card>
	)
}

export function MatchCards(props) {
    const { gameWeek, date, homeTeam, awayTeam, result, handleOpenMatchFactsModal } = props;
    
    return (
        <Card sx={{ margin: 2 }}>
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
                            {date}
                        </Typography>
                        <Typography variant="body2">
                            {gameWeek}
                        </Typography>
                    </Box>
                    <Box sx={{ alignContent: "center" }}>
                        <Typography variant="h5">
                            {result}
                        </Typography>
                    </Box>
                </Box>
            </CardContent>
            <CardActions sx={{ justifyContent: "center" }}>
                <Button size="small" onClick={() => handleOpenMatchFactsModal(date, homeTeam, awayTeam)}>View Match Facts</Button>
                <Button size="small">Add Result</Button>
            </CardActions>
        </Card>
    );
}
