-- CREATE DATABASE pl_stats;

\c pl_stats;

CREATE TABLE country (
	id VARCHAR(7) PRIMARY KEY,
	name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE competition (
	id VARCHAR(7) PRIMARY KEY,
	country_id VARCHAR(7) REFERENCES country(id) NOT NULL,
	name VARCHAR UNIQUE NOT NULL,
	type VARCHAR NOT NULL
);

CREATE TABLE player (
	id VARCHAR(7) PRIMARY KEY,
	first_name VARCHAR,
	last_name VARCHAR,
	birth_year VARCHAR NOT NULL,
	position VARCHAR,
	nationality VARCHAR,
	fbref_match_logs_href VARCHAR,
	fbref_id VARCHAR DEFAULT NULL
);

CREATE TABLE team (
	id VARCHAR(7) PRIMARY KEY,
	name VARCHAR UNIQUE NOT NULL,
	country_id VARCHAR(7) REFERENCES country(id) NOT NULL
);

CREATE TABLE referee (
	id VARCHAR(7) PRIMARY KEY,
	name VARCHAR NOT NULL
);

CREATE TABLE schedule (
	season VARCHAR(9) NOT NULL,
	round_number INT NOT NULL,
	date VARCHAR(16) NOT NULL,
	home_team_id VARCHAR(7) REFERENCES team(id),
	away_team_id VARCHAR(7) REFERENCES team(id),
	home_elo FLOAT,
	away_elo FLOAT,
	competition_id VARCHAR(7) REFERENCES competition(id),
	result VARCHAR,
	PRIMARY KEY (season, competition_id, round_number, home_team_id, away_team_id)
);

CREATE TABLE player_team (
	player_id VARCHAR(7) REFERENCES player(id),
	team_id VARCHAR(7) REFERENCES team(id),
	season VARCHAR(9) NOT NULL,
	number_team_in_season INT DEFAULT 1,
	PRIMARY KEY (player_id, team_id, season)
);

CREATE TABLE match (
	id VARCHAR(7) PRIMARY KEY,
	season VARCHAR(9) NOT NULL,
	date VARCHAR(16) NOT NULL,
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
	away_red_cards INTEGER NOT NULL,
	home_odds FLOAT NOT NULL,
	draw_odds FLOAT NOT NULL,
	away_odds FLOAT NOT NULL,
	closing_home_odds FLOAT NOT NULL,
	closing_draw_odds FLOAT NOT NULL,
	closing_away_odds FLOAT NOT NULL
);

CREATE TABLE match_logs (
	player_id VARCHAR(7) REFERENCES player(id),
	fbref_id VARCHAR NOT NULL,
	competition_id VARCHAR(7) REFERENCES competition(id) NOT NULL,
	match_id VARCHAR(7) REFERENCES match(id),
	season VARCHAR NOT NULL,
	date VARCHAR NOT NULL,
	location VARCHAR NOT NULL,
	team_id VARCHAR(7) REFERENCES team(id) NOT NULL,
	opponent_id VARCHAR(7) REFERENCES team(id) NOT NULL,
	position VARCHAR,
	started VARCHAR NOT NULL,
	minutes INTEGER NOT NULL,
	goals INTEGER NOT NULL,
	assists INTEGER NOT NULL,
	pens_made INTEGER NOT NULL,
	pens_att INTEGER NOT NULL,
	shots INTEGER NOT NULL,
	shots_on_target INTEGER NOT NULL,
	cards_yellow INTEGER NOT NULL,
	cards_red INTEGER NOT NULL,
	blocks INTEGER NOT NULL,
	xg FLOAT NOT NULL,
	npxg FLOAT NOT NULL,
	passes_total_distance INTEGER NOT NULL,
	passes_progressive_distance INTEGER NOT NULL,
	passes_completed_short INTEGER NOT NULL,
	passes_short INTEGER NOT NULL,
	passes_completed_medium INTEGER NOT NULL,
	passes_medium INTEGER NOT NULL,
	passes_completed_long INTEGER NOT NULL,
	passes_long INTEGER NOT NULL,
	xg_assist FLOAT NOT NULL,
	pass_xa FLOAT NOT NULL,
	assisted_shots INTEGER NOT NULL,
	passes_into_final_third INTEGER NOT NULL,
	passes_into_penalty_area INTEGER NOT NULL,
	crosses_into_penalty_area INTEGER NOT NULL,
	progressive_passes INTEGER NOT NULL,
	tackles INTEGER NOT NULL,
	tackles_won INTEGER NOT NULL,
	tackles_def_3rd INTEGER NOT NULL,
	tackles_mid_3rd INTEGER NOT NULL,
	tackles_att_3rd INTEGER NOT NULL,
	challenge_tackles INTEGER NOT NULL,
	challenges INTEGER NOT NULL,
	blocked_shots INTEGER NOT NULL,
	blocked_passes INTEGER NOT NULL,
	interceptions INTEGER NOT NULL,
	clearances INTEGER NOT NULL,
	errors INTEGER NOT NULL,
	touches INTEGER NOT NULL,
	touches_def_pen_area INTEGER NOT NULL,
	touches_def_3rd INTEGER NOT NULL,
	touches_mid_3rd INTEGER NOT NULL,
	touches_att_3rd INTEGER NOT NULL,
	touches_att_pen_area INTEGER NOT NULL,
	touches_live_ball INTEGER NOT NULL,
	take_ons INTEGER NOT NULL,
	take_ons_won INTEGER NOT NULL,
	take_ons_tackled INTEGER NOT NULL,
	carries INTEGER NOT NULL,
	carries_distance INTEGER NOT NULL,
	carries_progressive_distance INTEGER NOT NULL,
	progressive_carries INTEGER NOT NULL,
	carries_into_final_third INTEGER NOT NULL,
	carries_into_penalty_area INTEGER NOT NULL,
	miscontrols INTEGER NOT NULL,
	dispossessed INTEGER NOT NULL,
	passes_received INTEGER NOT NULL,
	progressive_passes_received INTEGER NOT NULL,
	sca INTEGER NOT NULL,
	sca_passes_live INTEGER NOT NULL,
	sca_passes_dead INTEGER NOT NULL,
	sca_take_ons INTEGER NOT NULL,
	sca_shots INTEGER NOT NULL,
	sca_fouled INTEGER NOT NULL,
	sca_defense INTEGER NOT NULL,
	gca INTEGER NOT NULL,
	gca_passes_live INTEGER NOT NULL,
	gca_passes_dead INTEGER NOT NULL,
	gca_take_ons INTEGER NOT NULL,
	gca_shots INTEGER NOT NULL,
	gca_fouled INTEGER NOT NULL,
	gca_defense INTEGER NOT NULL,
	gk_shots_on_target_against INTEGER NOT NULL,
	gk_goals_against INTEGER NOT NULL,
	gk_saves INTEGER NOT NULL,
	gk_clean_sheets INTEGER NOT NULL,
	gk_psxg INTEGER NOT NULL,
	gk_pens_att INTEGER NOT NULL,
	gk_pens_allowed INTEGER NOT NULL,
	gk_pens_saved INTEGER NOT NULL,
	gk_pens_missed INTEGER NOT NULL,
	gk_passed_completed_launched INTEGER NOT NULL,
	gk_passes_launched INTEGER NOT NULL,
	gk_passes INTEGER NOT NULL,
	gk_passes_throws INTEGER NOT NULL,
	gk_passes_length_avg FLOAT NOT NULL,
	gk_goal_kicks INTEGER NOT NULL,
	gk_goal_kicks_length_avg FLOAT NOT NULL,
	PRIMARY KEY (player_id, match_id)
);

CREATE TABLE historic_player_per_ninety (
	player_id VARCHAR(7) REFERENCES player(id),
	team_id VARCHAR(7) REFERENCES team(id),
	nationality VARCHAR NOT NULL,
	matches_played INT NOT NULL,
	minutes_played FLOAT NOT NULL,
	ninetys FLOAT NOT NULL,
	starts INT NOT NULL,
	goals FLOAT NOT NULL,
	assists FLOAT NOT NULL,
	direct_goal_contributions FLOAT NOT NULL,
	non_penalty_goals FLOAT NOT NULL,
	penalties_scored FLOAT NOT NULL,
	penalties_attempted FLOAT NOT NULL,
	yellow_cards FLOAT NOT NULL,
	red_cards FLOAT NOT NULL,
	expected_goals FLOAT NOT NULL,
	non_penalty_expected_goals FLOAT NOT NULL,
	expected_assisted_goals FLOAT NOT NULL,
	non_penalty_expected_goals_plus_expected_assisted_goals FLOAT NOT NULL,
	progressive_carries FLOAT NOT NULL,
	progressive_passes FLOAT NOT NULL,
	progressive_passes_received FLOAT NOT NULL,
	total_passing_distance FLOAT NOT NULL,
	total_progressive_passing_distance FLOAT NOT NULL,
	short_passes_completed FLOAT NOT NULL,
	short_passes_attempted FLOAT NOT NULL,
	medium_passes_completed FLOAT NOT NULL,
	medium_passes_attempted FLOAT NOT NULL,
	long_passes_completed FLOAT NOT NULL,
	long_passes_attempted FLOAT NOT NULL,
	expected_assists FLOAT NOT NULL,
	assists_minus_expected_assisted_goals FLOAT NOT NULL,
	key_passes FLOAT NOT NULL,
	passes_into_final_third FLOAT NOT NULL,
	passes_into_penalty_area FLOAT NOT NULL,
	crosses_into_penalty_area FLOAT NOT NULL,
	shots FLOAT NOT NULL,
	shots_on_target FLOAT NOT NULL,
	goals_per_shot FLOAT NOT NULL,
	goals_per_shot_on_target FLOAT NOT NULL,
	average_shot_distance FLOAT NOT NULL,
	shots_from_free_kicks FLOAT NOT NULL,
	penalties_made FLOAT NOT NULL,
	non_penalty_expected_goals_per_shot FLOAT NOT NULL,
	goals_minus_expected_goals FLOAT NOT NULL,
	non_penalty_goals_minus_non_penalty_expected_goals FLOAT NOT NULL,
	touches FLOAT NOT NULL,
	touches_in_defensive_penalty_area FLOAT NOT NULL,
	touches_in_defensive_third FLOAT NOT NULL,
	touches_in_middle_third FLOAT NOT NULL,
	touches_in_attacking_third FLOAT NOT NULL,
	touches_in_attacking_penalty_area FLOAT NOT NULL,
	live_ball_touches FLOAT NOT NULL,
	take_ons_attempted FLOAT NOT NULL,
	take_ons_succeeded FLOAT NOT NULL,
	times_tackled_during_take_on FLOAT NOT NULL,
	carries FLOAT NOT NULL,
	total_carrying_distance FLOAT NOT NULL,
	progressive_carrying_distance FLOAT NOT NULL,
	carries_into_final_third FLOAT NOT NULL,
	carries_into_penalty_area FLOAT NOT NULL,
	miscontrols FLOAT NOT NULL,
	dispossessed FLOAT NOT NULL,
	passes_received FLOAT NOT NULL,
	tackles FLOAT NOT NULL,
	tackles_won FLOAT NOT NULL,
	defensive_third_tackles FLOAT NOT NULL,
	middle_third_tackles FLOAT NOT NULL,
	attacking_third_tackles FLOAT NOT NULL,
	dribblers_tackled FLOAT NOT NULL,
	dribbler_tackles_attempted FLOAT NOT NULL,
	shots_blocked FLOAT NOT NULL,
	passes_blocked FLOAT NOT NULL,
	interceptions FLOAT NOT NULL,
	clearances FLOAT NOT NULL,
	errors_leading_to_shot FLOAT NOT NULL,
	goals_against FLOAT NOT NULL,
	shots_on_target_against FLOAT NOT NULL,
	saves FLOAT NOT NULL,
	clean_sheets FLOAT NOT NULL,
	penalties_faced FLOAT NOT NULL,
	penalties_allowed FLOAT NOT NULL,
	penalties_saved FLOAT NOT NULL,
	penalties_missed FLOAT NOT NULL,
	season VARCHAR NOT NULL,
	PRIMARY KEY (player_id, team_id, season)
);

CREATE TABLE manager (
	id VARCHAR(7) PRIMARY KEY,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	team_id VARCHAR(7) REFERENCES team(id) NOT NULL,
	start_date VARCHAR(10) NOT NULL,
	end_date VARCHAR(10) NOT NULL
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

ALTER TABLE manager
ADD CONSTRAINT manager_id_format_check
CHECK (id ~ '^mn-\d{4}$');

CREATE SEQUENCE team_id_seq START 1;
CREATE SEQUENCE player_id_seq START 1;
CREATE SEQUENCE match_id_seq START 1;
CREATE SEQUENCE country_id_seq START 1;
CREATE SEQUENCE competition_id_seq START 1;
CREATE SEQUENCE referee_id_seq START 1;
CREATE SEQUENCE manager_id_seq START 1;

CREATE OR REPLACE FUNCTION validate_id()
RETURNS TRIGGER AS $$
BEGIN

    CASE
        WHEN TG_TABLE_NAME = 'team' THEN
            NEW.id = 't-' || LPAD(nextval('team_id_seq')::TEXT, 5, '0');
        WHEN TG_TABLE_NAME = 'country' THEN
            NEW.id = 'c-' || LPAD(nextval('country_id_seq')::TEXT, 5, '0');
        WHEN TG_TABLE_NAME = 'competition' THEN
            NEW.id = 'x-' || LPAD(nextval('competition_id_seq')::TEXT, 5, '0');
        WHEN TG_TABLE_NAME = 'match' THEN
            NEW.id = 'm-' || LPAD(nextval('match_id_seq')::TEXT, 5, '0');
        WHEN TG_TABLE_NAME = 'referee' THEN
            NEW.id = 'r-' || LPAD(nextval('referee_id_seq')::TEXT, 5, '0');
        WHEN TG_TABLE_NAME = 'player' THEN
            NEW.id = 'p-' || LPAD(nextval('player_id_seq')::TEXT, 5, '0');
        WHEN TG_TABLE_NAME = 'manager' THEN
            NEW.id = 'mn-' || LPAD(nextval('manager_id_seq')::TEXT, 4, '0');
    END CASE;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER before_insert_or_update_team
BEFORE INSERT ON team
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_country
BEFORE INSERT ON country
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_competition
BEFORE INSERT ON competition
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_match
BEFORE INSERT ON match
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_referee
BEFORE INSERT ON referee
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_player
BEFORE INSERT ON player
FOR EACH ROW EXECUTE FUNCTION validate_id();

CREATE TRIGGER before_insert_or_update_manager
BEFORE INSERT ON manager
FOR EACH ROW EXECUTE FUNCTION validate_id();