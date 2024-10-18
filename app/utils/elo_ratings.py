import requests
from io import StringIO
import pandas as pd
from app_logger import FluentLogger
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("elo_ratings").get_logger()

elo_name_conversion = {
	"Manchester City": "ManCity",
	"Man City": "ManCity",
	"Arsenal": "Arsenal",
	"Liverpool": "Liverpool",
	"Chelsea": "Chelsea",
	"Newcastle United": "Newcastle",
	"Tottenham Hotspur": "Tottenham",
	"Spurs": "Tottenham",
	"Manchester United": "ManUnited",
	"Man Utd": "ManUnited",
	"Huddersfield Town": "Huddersfield",
	"Aston Villa": "AstonVilla",
	"Crystal Palace": "CrystalPalace",
	"West Ham United": "WestHam",
	"West Ham": "WestHam",
	"Fulham": "Fulham",
	"Brighton & Hove Albion": "Brighton",
	"Brentford": "Brentford",
	"Everton": "Everton",
	"Bournemouth": "Bournemouth",
	"Wolverhampton Wanderers": "Wolves",
	"Nottingham Forest": "Forest",
	"Nott'm Forest": "Forest",
	"Leicester City": "Leicester",
	"Southampton": "Southampton",
	"Ipswich Town": "Ipswich",
	"Burnley": "Burnley",
	"Leeds United": "Leeds",
	"Luton Town": "Luton",
	"Middlesbrough": "Middlesbrough",
	"West Bromwich Albion": "WestBrom",
	"West Brom": "WestBrom",
	"Sheffield United": "SheffieldUnited",
	"Sheffield Utd": "SheffieldUnited",
	"Norwich City": "Norwich",
	"Hull City": "Hull",
	"Coventry City": "Coventry",
	"Watford": "Watford",
	"Bristol City": "Bristol City",
	"Swansea City": "Swansea",
	"Stoke City": "Stoke",
	"Sheffield Wednesday": "SheffieldWeds",
	"Blackburn Rovers": "Blackburn",
	"Millwall": "Millwall",
	"Sunderland": "Sunderland",
	"Queens Park Rangers": "QPR",
	"Preston North End": "Preston",
	"Plymouth Argyle": "Plymouth",
	"Oxford United": "Oxford",
	"Cardiff City": "Cardiff",
	"Portsmouth": "Portsmouth",
	"Derby County": "Derby",
	"Bristol City": "Bristol",
	"Wigan Athletic": "Wigan",
	"Birmingham City": "Birmingham",
	"Charlton Athletic": "Charlton",
	"Rotherham United": "Rotherham",
	"Wycombe Wanderers": "Wycombe",
	"Peterborough United": "Peterborough",
}

def get_team_elo_rating(team_name: str) -> pd.DataFrame:
	"""
	Get the ELO rating of a team on a specific date.

	Args:
		team_name (str): The name of the team.

	Returns:
		pd.DataFrame: The ELO rating DataFrame of the team on the given date.
	"""
	try:
		elo_team_name = elo_name_conversion.get(team_name, team_name)
		url = f"http://api.clubelo.com/{elo_team_name}"
		logger.info(f"Getting ELO rating for {elo_team_name}: {url}.")
		response = requests.get(url)

		if response.status_code == 200:
			csv_data = StringIO(response.text)
			df = pd.read_csv(csv_data)
			df["Club"] = team_name
			df = format_elo_df(df)
			return df
		else:
			logger.error(f"Error finding ELO for {elo_team_name}: {response.status_code}")
			return pd.DataFrame()
	except Exception as e:
		logger.error(f"Error finding ELO for {elo_team_name}: {e}")
		return pd.DataFrame()
	
def format_elo_df(elos: pd.DataFrame) -> pd.DataFrame:
	if not elos.empty:
		elos['From'] = pd.to_datetime(elos['From'])
		elos['To'] = pd.to_datetime(elos['To'])

		elos_expanded = pd.DataFrame({
			'Date': pd.date_range(start=elos['From'].min(), end=elos['To'].max(), freq='D')
		})
		elos_expanded = elos_expanded.merge(elos, left_on='Date', right_on='From', how='left').ffill()
		elos_expanded["Date"] = pd.to_datetime(elos_expanded["Date"]).dt.strftime("%Y-%m-%d")
		return elos_expanded