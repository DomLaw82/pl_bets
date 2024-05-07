import os
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

class SQLConnection:
    """Create a PostgreSQL connection class."""
    def __init__(self, username: str, password: str, host: str, port: str, db_name: str) -> None:
        connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
        self.engine = sqlalchemy.create_engine(connection_string, isolation_level='AUTOCOMMIT')
        self.conn = self.engine.connect()

    def get_df(self, query: str) -> pd.DataFrame:
        """Query the database and return a DataFrame."""
        query = sqlalchemy.text(query)
        try:
            res = pd.read_sql_query(query, self.conn)
            if res.empty:
                print('No data returned')
            return res
        except SQLAlchemyError as e:
            print('Database error:', e)
        except ValueError as e:
            print(e)

    def get_list(self, query: str) -> list:
        """Execute a query and return a list."""
        return self._execute_query(query, fetch='all')

    def execute(self, query: str) -> None:
        """Execute a non-return query."""
        self._execute_query(query, fetch=None)

    def get_dict(self, query: str) -> dict:
        """Execute a query and return a list of dictionaries."""
        return self._execute_query(query, fetch='dict')

    def _execute_query(self, query: str, fetch: str = 'all'):
        """Helper method to execute queries and manage fetch types."""
        query = sqlalchemy.text(query)
        try:
            result = self.conn.execute(query)
            if fetch == 'all':
                return result.fetchall()
            elif fetch == 'dict':
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except SQLAlchemyError as e:
            print('Database error:', e)

    def close(self):
        """Close connection to the database."""
        self.conn.close()
        self.engine.dispose()