CREATE DATABASE pl_stats;

\c pl_stats;

CREATE TABLE country (
	id VARCHAR(7) PRIMARY KEY,
	name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE competition (
	id VARCHAR(7) PRIMARY KEY,
	country_id VARCHAR(7) REFERENCES country(id) NOT NULL,
	name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE player (
	id VARCHAR(7) PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	birth_date DATE NOT NULL,
	position VARCHAR NOT NULL
);

CREATE TABLE team (
	id VARCHAR(7) PRIMARY KEY,
	name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE referee (
	id VARCHAR(7) PRIMARY KEY,
	name VARCHAR NOT NULL
);

CREATE TABLE schedule (
	match_number INT NOT NULL,
	round_number INT NOT NULL,
	date DATETIME NOT NULL,
	location VARCHAR NOT NULL,
	home_team_id VARCHAR(7) REFERENCES team(id),
	away_team_id VARCHAR(7) REFERENCES team(id),
	competition_id VARCHAR(7) REFERENCES competition(id),
	result VARCHAR
);

CREATE TABLE player_team (
	player_id VARCHAR(7) REFERENCES team(id),
	team_id VARCHAR(7) REFERENCES team(id),
	season VARCHAR(7) NOT NULL
);

CREATE TABLE match (
	id VARCHAR(7) PRIMARY KEY,
	season VARCHAR(7) NOT NULL,
	competition_id VARCHAR(7) NOT NULL,
	home_team_id VARCHAR(7) REFERENCES team(id) NOT NULL,
	away_team_id VARCHAR(7) REFERENCES team(id) NOT NULL,
	referee_id VARCHAR(7) REFERENCES referee(id) NOT NULL,
	home_goals INTEGER NOT NULL,
	away_goals INTEGER NOT NULL,
	home_shots INTEGER NOT NULL,
	away_shots INTEGER NOT NULL,
	home_shots_on_target INTEGER NOT NULL,
	away_shots_on_target INTEGER NOT NULL,
	home_corners INTEGER NOT NULL,
	away_corners INTEGER NOT NULL,
	home_fouls INTEGER NOT NULL,
	away_fouls INTEGER NOT NULL,
	home_yellow_cards INTEGER NOT NULL,
	away_yellow_cards INTEGER NOT NULL,
	home_red_cards INTEGER NOT NULL,
	away_red_cards INTEGER NOT NULL
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

ALTER TABLE team
ADD CONSTRAINT team_id_format_check
CHECK (id ~ '^t-\d{5}$');

ALTER TABLE match
ADD CONSTRAINT match_id_format_check
CHECK (id ~ '^m-\d{5}$');

ALTER TABLE player
ADD CONSTRAINT player_id_format_check
CHECK (id ~ '^p-\d{5}$');

ALTER TABLE country
ADD CONSTRAINT country_id_format_check
CHECK (id ~ '^c-\d{5}$');

ALTER TABLE competition
ADD CONSTRAINT competition_id_format_check
CHECK (id ~ '^x-\d{5}$');

ALTER TABLE referee
ADD CONSTRAINT referee_id_format_check
CHECK (id ~ '^r-\d{5}$');

CREATE SEQUENCE team_id_seq START 1;
CREATE SEQUENCE player_id_seq START 1;
CREATE SEQUENCE match_id_seq START 1;
CREATE SEQUENCE country_id_seq START 1;
CREATE SEQUENCE competition_id_seq START 1;
CREATE SEQUENCE referee_id_seq START 1;

CREATE OR REPLACE FUNCTION validate_id()
RETURNS TRIGGER AS $$
BEGIN

    CASE
        WHEN TG_TABLE_NAME = 'team' THEN
            NEW.id = 't-' || LPAD(nextval('team_id_seq')::TEXT, 7, '0');
        WHEN TG_TABLE_NAME = 'country' THEN
            NEW.id = 'c-' || LPAD(nextval('country_id_seq')::TEXT, 7, '0');
        WHEN TG_TABLE_NAME = 'competition' THEN
            NEW.id = 'x-' || LPAD(nextval('competition_id_seq')::TEXT, 7, '0');
        WHEN TG_TABLE_NAME = 'match' THEN
            NEW.id = 'm-' || LPAD(nextval('match_id_seq')::TEXT, 7, '0');
        WHEN TG_TABLE_NAME = 'referee' THEN
            NEW.id = 'r-' || LPAD(nextval('referee_id_seq')::TEXT, 7, '0');
        WHEN TG_TABLE_NAME = 'player' THEN
            NEW.id = 'p-' || LPAD(nextval('player_id_seq')::TEXT, 7, '0');
    END CASE;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER before_insert_or_update_team
BEFORE INSERT OR UPDATE ON team
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_country
BEFORE INSERT OR UPDATE ON country
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_competition
BEFORE INSERT OR UPDATE ON competition
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_match
BEFORE INSERT OR UPDATE ON match
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_referee
BEFORE INSERT OR UPDATE ON referee
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_player
BEFORE INSERT OR UPDATE ON player
FOR EACH ROW EXECUTE FUNCTION validate_id();