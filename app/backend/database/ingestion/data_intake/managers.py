from bs4 import BeautifulSoup
import csv, os
import pandas as pd
import numpy as np
from data_intake.utilities.unique_id import get_id_from_name
from app_logger import FluentLogger
from data_intake.utilities.remove_duplicates import remove_duplicate_rows
import requests

logger = FluentLogger("intake-manager").get_logger()

MANAGER_URL = "https://en.wikipedia.org/wiki/List_of_Premier_League_managers"
MANAGER_SAVE_PATH_ROOT = "data/manager_data/"
MANAGER_FILE_NAME = "managers.html"
MANAGER_FILE_PATH = os.path.join(MANAGER_SAVE_PATH_ROOT, MANAGER_FILE_NAME)

pd.set_option('display.max_rows', None)

def download_manager_html_data():
	"""
	Downloads the HTML content of the given URL and saves it to the specified path.

	Parameters:
	url (str): The URL from which the HTML content is to be downloaded.
	save_path (str): The path where the downloaded HTML content is to be saved.

	Returns:
	bool: True if the HTML content is downloaded and saved successfully, False otherwise.
	"""
	try:
		response = requests.get(MANAGER_URL)
		if response.status_code != 200:
			logger.error(f"Failed to download the HTML content. Status code: {response.status_code}")
			return False

		with open(MANAGER_FILE_PATH, "w") as file:
			file.write(response.text)
		logger.info(f"HTML content downloaded and saved to {MANAGER_FILE_PATH}")
		return True
	except Exception as e:
		logger.error(f"An error occurred while downloading the HTML content: {str(e)}")
		return False

def clean_manager(html_content, connector):
	try:
		# Parse the HTML content using BeautifulSoup
		soup = BeautifulSoup(html_content, 'html.parser')

		# Find the table in the HTML
		table = soup.find('table', {'class': 'wikitable sortable plainrowheaders'})

		# Extract table headers
		headers = []
		for th in table.find_all('th'):
			headers.append(th.get_text(strip=True).lower())

		# Extract table rows
		rows = []
		for tr in table.find_all('tr'):
			cells = tr.find_all(['td', 'th'])
			row = [cell.get_text(strip=True).lower() for cell in cells]
			if row:  # Avoid adding empty rows
				rows.append(row)

		# Write the data to a CSV file
		with open('./data/manager_data/managers.csv', 'w', newline='', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(headers)  # Write the header row
			writer.writerows(rows)    # Write the data rows

		print("CSV file has been created successfully.")

		df = pd.read_csv('./data/manager_data/managers.csv')
		df = df.iloc[1:]  # Drop the first row

		df = df[["name", "club", "nat.", "from", "until"]]
		df = df.rename(columns={"nat.": "nationality", "from": "start_date", "until": "end_date", "club": "team"})

		df[["first_name", "last_name"]] = df["name"].str.split(" ", n=1, expand=True)
		df["first_name"] = df["first_name"].str.replace('[^a-zA-Z]', '', regex=True)
		df["last_name"] = df["last_name"].str.replace('[^a-zA-Z]', '', regex=True)
		df = df.drop(columns=["name", "nationality"])

		df["start_date"] = df["start_date"].str.replace(r'\[\w\]', '', regex=True)
		df["end_date"] = df["end_date"].str.replace(r'\[\w\]', '', regex=True).replace("present*", np.nan)

		df["start_date"] = pd.to_datetime(df["start_date"], format="%d %B %Y").dt.strftime("%Y-%m-%d")
		df["end_date"] = pd.to_datetime(df["end_date"], format="%d %B %Y").dt.strftime("%Y-%m-%d")

		df["end_date"] = df["end_date"].replace(np.nan, "current")

		df["team_id"] = df["team"].apply(lambda team_name: get_id_from_name(connector, team_name, "team"))
		df = df.drop(columns=["team"])

		df = df[['first_name', 'last_name', 'team_id', 'start_date', 'end_date']]

		df = remove_duplicate_rows(connector, df, ["first_name", "last_name", "team_id", "start_date", "end_date"], "manager")

		return df
	except Exception as e:
		raise Exception(f"Error cleaning manager data: {e}")
	
def save_to_database(df, connection) -> None:
	# Save the data to a database
	try:
		with connection.connect() as conn:
			df.to_sql("manager", conn, if_exists="append", index=False)
	except Exception as e:
		logger.error(f"Error saving manager data: {e}")
		raise Exception(f"Error saving manager data: {e}")
	
def manager_main(con):
	try:
		with open('./data/manager_data/managers.html', 'r', encoding='utf-8') as file:
			html_content = file.read()

		df = clean_manager(html_content, con)
		
		save_to_database(df, con)
	except Exception as e:
		logger.error(e)
		raise Exception(e)