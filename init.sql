CREATE DATABASE pl_stats;

CREATE TABLE country (
	id VARCHAR(5) PRIMARY KEY,
	name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE competition (
	id VARCHAR(4) PRIMARY KEY,
	country_id VARCHAR(5) REFERENCES country(id) NOT NULL,
	name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE player (
	id VARCHAR(7) PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	birth_date DATE NOT NULL,
	role VARCHAR NOT NULL
);

CREATE TABLE TEAM (
	id VARCHAR(5) PRIMARY KEY,
	name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE schedule (
	competition_id VARCHAR(4) REFERENCES competition(id),
	home_team_id VARCHAR(5) REFERENCES team(id),
	away_team_id VARCHAR(5) REFERENCES team(id),
	ko_date DATE NOT NULL,
	ko_time TIME NOT NULL
);

CREATE TABLE player_team (
	player_id VARCHAR(5) REFERENCES team(id),
	team_id VARCHAR(5) REFERENCES team(id),
	season VARCHAR(7) NOT NULL
);

CREATE TABLE competition_team (
	competition_id VARCHAR(4) REFERENCES competition(id),
	team_id VARCHAR(5) REFERENCES team(id),
	season VARCHAR(7) NOT NULL
);

CREATE TABLE match (
	id VARCHAR(8) PRIMARY KEY,
	season VARCHAR(7) NOT NULL,
	competition_id VARCHAR(4) NOT NULL,
	home_team_id VARCHAR(5) REFERENCES team(id) NOT NULL,
	away_team_id VARCHAR(5) REFERENCES team(id) NOT NULL,
	home_goals INTEGER NOT NULL,
	away_goals INTEGER NOT NULL,
	home_shots INTEGER NOT NULL,
	home_shots_on_target INTEGER NOT NULL,
	away_shots INTEGER NOT NULL,
	away_shots_on_target INTEGER NOT NULL,
	home_corners INTEGER NOT NULL,
	away_corners INTEGER NOT NULL,
	home_fouls INTEGER NOT NULL,
	home_yellow_cards INTEGER NOT NULL,
	home_red_cards INTEGER NOT NULL,
	home_corners INTEGER NOT NULL,
	away_fouls INTEGER NOT NULL,
	away_yellow_cards INTEGER NOT NULL,
	away_red_cards INTEGER NOT NULL,
	away_corners INTEGER NOT NULL
);

CREATE TABLE historic_player_per_ninety (
	player_id VARCHAR(7) REFERENCES player(id) PRIMARY KEY,
	minutes_played NUMERIC NOT NULL,
	goals NUMERIC NOT NULL,
	x_goals NUMERIC NOT NULL,
	assists NUMERIC NOT NULL,
	x_assists NUMERIC NOT NULL,
	shots NUMERIC NOT NULL,
	shots_on_target NUMERIC NOT NULL,
	passes_attempted NUMERIC NOT NULL,
	passes_completed NUMERIC NOT NULL,
	progressive_passes_completed NUMERIC NOT NULL,
	take_ons_attempted NUMERIC NOT NULL,
	take_ons_completed NUMERIC NOT NULL,
	touches_def_third NUMERIC NOT NULL,
	touches_middle_third NUMERIC NOT NULL,
	touches_att_third NUMERIC NOT NULL,
	carries NUMERIC NOT NULL,
	total_carrying_distance NUMERIC NOT NULL,
	tackles NUMERIC NOT NULL,
	blocks NUMERIC NOT NULL,
	interceptions NUMERIC NOT NULL,
	clearances NUMERIC NOT NULL,
	fouls NUMERIC NOT NULL,
	yellow_cards NUMERIC NOT NULL,
	red_cards NUMERIC NOT NULL
);

CREATE TABLE player_form (
	player_id VARCHAR(7) REFERENCES player(id) PRIMARY KEY,
	minutes_played NUMERIC NOT NULL,
	goals NUMERIC NOT NULL,
	x_goals NUMERIC NOT NULL,
	assists NUMERIC NOT NULL,
	x_assists NUMERIC NOT NULL,
	shots NUMERIC NOT NULL,
	shots_on_target NUMERIC NOT NULL,
	passes_attempted NUMERIC NOT NULL,
	passes_completed NUMERIC NOT NULL,
	progressive_passes_completed NUMERIC NOT NULL,
	take_ons_attempted NUMERIC NOT NULL,
	take_ons_completed NUMERIC NOT NULL,
	touches_def_third NUMERIC NOT NULL,
	touches_middle_third NUMERIC NOT NULL,
	touches_att_third NUMERIC NOT NULL,
	carries NUMERIC NOT NULL,
	total_carrying_distance NUMERIC NOT NULL,
	tackles NUMERIC NOT NULL,
	blocks NUMERIC NOT NULL,
	interceptions NUMERIC NOT NULL,
	clearances NUMERIC NOT NULL,
	fouls NUMERIC NOT NULL,
	yellow_cards NUMERIC NOT NULL,
	red_cards NUMERIC NOT NULL
);

