import React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { Box } from '@mui/material';
import Divider from '@mui/material/Divider';


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
