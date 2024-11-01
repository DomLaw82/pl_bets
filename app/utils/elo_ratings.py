import requests
from io import StringIO
import pandas as pd
from app_logger import FluentLogger
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("elo_ratings").get_logger()

elo_name_conversion = {
	"AFC Wimbledon": "Wimbledon",
	"Arsenal": "Arsenal",
	"Aston Villa": "AstonVilla",
	"Barnsley": "Barnsley",
	"Birmingham City": "Birmingham",
	"Blackburn Rovers": "Blackburn",
	"Blackpool": "Blackpool",
	"Bolton Wanderers": "Bolton",
	"Bournemouth": "Bournemouth",
	"Bradford City": "Bradford",
	"Brentford": "Brentford",
	"Brighton and Hove Albion": "Brighton",
	"Bristol City": "BristolCity",
	"Burnley": "Burnley",
	"Burton Albion": "Burton",
	"Cardiff City": "Cardiff",
	"Charlton Athletic": "Charlton",
	"Chelsea": "Chelsea",	
	"Colchester United": "Colchester",
	"Coventry City": "Coventry",
	"Crewe Alexandra": "Crewe",
	"Crystal Palace": "CrystalPalace",
	"Derby County": "Derby",
	"Doncaster Rovers": "Doncaster",
	"Everton": "Everton",
	"Fulham": "Fulham",
	"Gillingham": "Gillingham",
	"Huddersfield Town": "Huddersfield",
	"Hull City": "Hull",
	"Ipswich Town": "Ipswich",
	"Leeds United": "Leeds",
	"Leicester City": "Leicester",
	"Liverpool": "Liverpool",
	"Luton Town": "Luton",
	"Manchester City": "ManCity",
	"Manchester United": "ManUnited",
	"Middlesbrough": "Middlesbrough",
	"Millwall": "Millwall",
	"Milton Keynes Dons": "MKDons",
	"Newcastle United": "Newcastle",
	"Norwich City": "Norwich",
	"Nottingham Forest": "Forest",
	"Oldham Athletic": "Oldham",
	"Oxford United": "Oxford",
	"Peterborough United": "Peterborough",
	"Plymouth Argyle": "Plymouth",
	"Port Vale": "PortVale",
	"Portsmouth": "Portsmouth",
	"Preston North End": "Preston",
	"Queens Park Rangers": "QPR",
	"Reading": "Reading",
	"Rotherham United": "Rotherham",
	"Salford City": "Salford",
	"Scunthorpe United": "Scunthorpe",
	"Sheffield United": "SheffieldUnited",
	"Sheffield Wednesday": "SheffieldWeds",
	"Southampton": "Southampton",
	"Southend United": "Southend",
	"Stevenage": "Stevenage",
	"Stoke City": "Stoke",
	"Sunderland": "Sunderland",
	"Swansea City": "Swansea",
	"Swindon Town": "Swindon",
	"Tottenham Hotspur": "Tottenham",
	"Tranmere Rovers": "Tranmere",
	"Walsall": "Walsall",
	"Watford": "Watford",
	"West Bromwich Albion": "WestBrom",
	"West Ham United": "WestHam",
	"Wigan Athletic": "Wigan",
	"Wolverhampton Wanderers": "Wolves",
	"Wycombe Wanderers": "Wycombe",
	"Yeovil Town": "Yeovil",
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
			df = format_elo_df(df)
			df["Club"] = team_name
			df = df.reset_index(drop=True)
			return df
		else:
			logger.error(f"Error finding ELO for {elo_team_name}: {response.status_code}")
			print(f"Error finding ELO for {elo_team_name}: {response.status_code}")
			return pd.DataFrame()
	except Exception as e:
		logger.error(f"Error finding ELO for {elo_team_name}: {e}")
		print(f"Error finding ELO for {elo_team_name}: {e}")
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