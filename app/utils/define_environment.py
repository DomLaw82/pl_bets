import os
from dotenv import load_dotenv

def load_correct_environment_variables() -> None:
	"""
	Check if the application is running in a container.

	Returns:
		bool: True if the application is running in a container, False otherwise.
	"""
	load_dotenv(f'.env.{os.getenv("ENVIRONMENT")}', override=True)
	