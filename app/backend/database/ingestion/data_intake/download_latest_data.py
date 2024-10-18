import requests, os, time
from bs4 import BeautifulSoup
import datetime
from app_logger import FluentLogger
from data_intake.player import download_player_data
from data_intake.ref_match import download_all_game_data
from data_intake.season_schedule import download_all_fixture_data
from data_intake.managers import download_manager_html_data
import pandas as pd
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

logger = FluentLogger("download_latest_data").get_logger()

def download_latest_data():
	logger.info("---Fetching latest data---")
	
	# This code is used to initially download the data from the web, but also to update the data on the fly from the frontend
		
		# game data download
	try:
		download_all_game_data()
	except Exception as e:
		logger.error(f"Error downloading the latest match data : line {e.__traceback__.tb_lineno} : {e}")
		# return f"Error downloading the latest match data: {e}"
		
		# fixture data download
	try:
		download_all_fixture_data()
	except Exception as e:
		logger.error(f"Error downloading the latest schedule data : line {e.__traceback__.tb_lineno} : {e}")
		# return f"Error downloading the latest schedule data: {e}"
		
	# player data download
	try:
		download_player_data()
	except Exception as e:
		logger.error(f"Error downloading the latest player data : line {e.__traceback__.tb_lineno} : {e}")
		# return f"Error downloading the latest player data: {e}"

	try:
		# Download
		# Managers data
		download_manager_html_data()
	except Exception as e:
		logger.error(f"Error downloading the latest manager data : line {e.__traceback__.tb_lineno} : {e}")
		# return {"error": f"Error downloading the latest manager data: {e}"}


		

	