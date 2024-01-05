import psycopg2
import pandas as pd
import sqlalchemy, os

class SQLConnection():
	"""Create a PostgreSQL connection class
	"""
	def __init__(self, username:str, password:str, host:str, port:str, db_name:str) -> None:
		self.engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}', isolation_level='AUTOCOMMIT')
		self.conn = self.engine.connect()
	
	def get_df(self, query:str) -> pd.DataFrame:
		"""
		query the database

		Args:
			query (str): string used to query the database

		Returns:
			pd.DataFrame: result of the query
		"""
		query = sqlalchemy.text(query)
		try:
			res = pd.read_sql_query(query, self.conn)
			return res
		except Exception as e:
			print('Exception Thrown:')
			print(e)
			print('\n')

	def get_list(self, query:str) -> list:
		"""
		Execute a query on the db

		Args:
				query (str): query string

		Returns:
				list: returned from query
		"""
		print(query)
		query = sqlalchemy.text(query)
		try:
			res = self.conn.execute(query)
			res = res.fetchall()
			return res
		except Exception as e:
			print('Exception Thrown:')
			print(e)
			print('\n')

	def execute(self, query:str) -> None:
		"""
		Execute a query on the db

		Args:
				query (str): query string
		"""
		query = sqlalchemy.text(query)
		try:
			res = self.conn.execute(query)
			return res
		except Exception as e:
			print('Exception Thrown:')
			print(e)
			print('\n')
	
	def get_dict(self, query:str) -> dict:
		"""
		Execute a query on the db

		Args:
				query (str): query string

		Returns:
				list: returned from query
		"""
		query = sqlalchemy.text(query)
		try:
			res = self.conn.execute(query)
			res_columns = list(self.conn.execute(query).keys())
			res = res.fetchall()
			
			result_dict = {}
			for index_a, row in enumerate(res):
				entry = {}
				for index_b, col in enumerate(row):
					entry[res_columns[index_b]] = col
				result_dict[index_a] = entry

			return result_dict
		except Exception as e:
			print('Exception Thrown:')
			print(e)
			print('\n')

local_pl_stats_connector = SQLConnection(os.environ.get("POSTGRES_USER"), os.environ.get("POSTGRES_PASSWORD"), os.environ.get("POSTGRES_CONTAINER"), os.environ.get("POSTGRES_PORT"), os.environ.get("POSTGRES_DB"))