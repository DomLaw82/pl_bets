from datetime import datetime
from app_logger import FluentLogger

def time_this_function(func):

	def wrapper(*args, **kwargs):
		start = datetime.now()
		result = func(*args, **kwargs)
		end = datetime.now()
		print(f"Function {func.__name__} took {end - start} to run.")
		return result
	
	return wrapper

def handle_exceptions(func):

	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
			return result
		except Exception as e:
			print(f"An error occurred: {e}")
	
	return wrapper