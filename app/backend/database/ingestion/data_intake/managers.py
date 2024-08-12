from bs4 import BeautifulSoup
import csv, os
import pandas as pd
import numpy as np
from utilities.unique_id import get_team_id
from db_connection import SQLConnection
from dotenv import load_dotenv

load_dotenv()

pd.set_option('display.max_rows', None)

def clean_manager(html_content, connector):

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
	df["last_name"] = df["last_name"].str.replace(r'‡', '')
	df = df.drop(columns=["name", "nationality"])

	df["start_date"] = df["start_date"].str.replace(r'\[\w\]', '', regex=True)
	df["end_date"] = df["end_date"].str.replace(r'\[\w\]', '', regex=True).replace("present*", np.nan)

	df["start_date"] = pd.to_datetime(df["start_date"], format="%d %B %Y").dt.strftime("%Y-%m-%d")
	df["end_date"] = pd.to_datetime(df["end_date"], format="%d %B %Y").dt.strftime("%Y-%m-%d")

	df["team_id"] = df["team"].apply(lambda team_name: get_team_id(connector, team_name))
	df = df.drop(columns=["team"])

	df = df[['first_name', 'last_name', 'team_id', 'start_date', 'end_date']]

	return df
	
def save_to_database(df, engine):
	# Save the data to a database
	df.to_sql('managers', con=engine, if_exists='append', index=False)

	print("Data has been saved to the database successfully.")

def manager_main(con):

	# Read the HTML content
	with open('./data/manager_data/managers.html', 'r', encoding='utf-8') as file:
		html_content = file.read()

	df = clean_manager(html_content, con)
	save_to_database(df, con.connect())