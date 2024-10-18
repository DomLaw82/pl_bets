import os
from dotenv import load_dotenv

import os

def is_running_in_docker() -> bool:
	"""Check if the code is running inside a Docker container."""
	try:
		# Check if '/.dockerenv' exists, which is a good indicator
		if os.path.exists('/.dockerenv'):
			return True
		
		# Another check: read /proc/1/cgroup for 'docker' or 'container'
		with open('/proc/1/cgroup', 'rt') as f:
			content = f.read()
			if 'docker' in content or 'container' in content:
				return True
	except Exception as e:
		pass
	
	# If none of the checks indicate a container, assume it's running locally
	return False

def load_correct_environment_variables() -> None:
	"""
	Check if the application is running in a container.

	Returns:
		bool: True if the application is running in a container, False otherwise.
	"""
	if is_running_in_docker():
		load_dotenv('.env.development', override=True)
		return
	load_dotenv(f'.env.local', override=True)
	