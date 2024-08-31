import pandas as pd
import numpy as np
from app_logger import FluentLogger
from db_connection import SQLConnection
from data_intake.utilities.save_to_database import save_to_database

logger = FluentLogger("intake-team").get_logger()

teams_since_2000 = ["Arsenal"
	,"Aston Villa"
	,"Barnsley"
	,"Birmingham City"
	,"Blackburn Rovers"
	,"Blackpool"
	,"Bolton Wanderers"
	,"Bournemouth"
	,"Bradford City"
	,"Brentford"
	,"Brighton & Hove Albion"
	,"Burnley"
	,"Cardiff City"
	,"Charlton Athletic"
	,"Chelsea"
	,"Coventry City"
	,"Crystal Palace"
	,"Derby County"
	,"Everton"
	,"Fulham"
	,"Huddersfield Town"
	,"Hull City"
	,"Ipswich Town"
	,"Leeds United"
	,"Leicester City"
	,"Liverpool"
	,"Luton Town"
	,"Manchester City"
	,"Manchester United"
	,"Middlesbrough"
	,"Newcastle United"
	,"Norwich City"
	,"Nottingham Forest"
	,"Oldham Athletic"
	,"Portsmouth"
	,"Queens Park Rangers"
	,"Reading"
	,"Sheffield United"
	,"Sheffield Wednesday"
	,"Southampton"
	,"Stoke City"
	,"Sunderland"
	,"Swansea City"
	,"Swindon Town"
	,"Tottenham Hotspur"
	,"Watford"
	,"West Bromwich Albion"
	,"West Ham United"
	,"Wigan Athletic"
	,"Wimbledon"
	,"Wolverhampton Wanderers"
]

def team_main(db_connection: SQLConnection) -> None:
	teams = pd.DataFrame(teams_since_2000, columns=["name"])
	teams["name"] = teams["name"].apply(lambda name: name.replace("'", "`"))
	save_to_database(db_connection, teams, "team")