from db_connection import local_pl_stats_connector
from app.backend.database.ingestion.data_intake.season_schedule import schedule_main
from app.backend.database.ingestion.data_intake.team_ref_match import team_ref_match_main
from app.backend.database.ingestion.data_intake.player import player_main
from app.backend.database.ingestion.data_intake.country_competition import country_competition_main
from app.backend.database.ingestion.data_intake.per_90_stats import per_90_main


# Ingest locally stored data into the database

# format season schedule [schedule]
schedule_main(local_pl_stats_connector)
    
# format game data [team, match, referee]
team_ref_match_main(local_pl_stats_connector)

# format squad data [player, player_team]
player_main(local_pl_stats_connector)

# [country, competition]
country_competition_main(local_pl_stats_connector)
	
# [historic_player_per_ninety]
per_90_main(local_pl_stats_connector)