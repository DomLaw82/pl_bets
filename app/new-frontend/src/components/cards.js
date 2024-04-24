import React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

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

export function MatchCards(gameWeek, date, homeTeam, awayTeam, result) {
	return (
		<Card>
			<CardContent>
				<Typography variant="h5" component="div">
					{gameWeek}
				</Typography>
				<Typography variant="body2">
					{date}
				</Typography>
				<Typography variant="body2">
					{homeTeam} vs {awayTeam}
				</Typography>
				<Typography variant="body2">
					{result}
				</Typography>
			</CardContent>
			<CardActions>
				<Button size="small">Learn More</Button>
				<Button size="small">Add Result</Button>
				{/* Learn more shows all stats for the game in a modal/popup */}
			</CardActions>
		</Card>
	)
}

