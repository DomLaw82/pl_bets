from datetime import datetime

def time_this_function(func):

	def wrapper(*args, **kwargs):
		start = datetime.now()
		result = func(*args, **kwargs)
		end = datetime.now()
		print(f"Function {func.__name__} took {end - start} to run.")
		return result
	
	return wrapper