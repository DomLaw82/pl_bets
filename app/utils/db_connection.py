import os
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

class SQLConnection:
    """Create a PostgreSQL connection class with context management within each method."""

    def __init__(self, username: str, password: str, host: str, port: str, db_name: str):
        """Initialize connection parameters."""
        try:
            self.connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
            self.engine = None
        except Exception as e:
            print(e)

    def connect(self):
        """Context manager that yields a connection from the pool."""
        if self.engine is None:
            self.engine = sqlalchemy.create_engine(self.connection_string, isolation_level='AUTOCOMMIT')
        return self.engine.connect()

    def get_df(self, query: str):
        """Query the database and return a DataFrame, managing context internally."""
        with self.connect() as conn:
            try:
                res = pd.read_sql_query(query, conn)
                return res
            except Exception as e:
                raise ValueError(e) # Optionally re-raise the exception after logging

    def get_list(self, query: str):
        """Execute a query and return a list, managing context internally."""
        try:
            with self.connect() as conn:
                return self._execute_query(conn, query, fetch='all')
        except Exception as e:
            raise ValueError(e)

    def get_dict(self, query: str):
        """Execute a query and return a list of dictionaries, managing context internally."""
        with self.connect() as conn:
            return self._execute_query(conn, query, fetch='dict')

    def execute(self, query):
        """Execute a non-return query, managing context internally."""
        with self.connect() as conn:
            try:
                conn.execute(sqlalchemy.text(query))
            except SQLAlchemyError as e:
                print('Database error:', e)
                raise

    def _execute_query(self, conn, query: str, fetch='all'):
        """Helper method to execute queries and manage fetch types."""
        try:
            result = conn.execute(sqlalchemy.text(query))
            if fetch == 'all':
                return result.fetchall()
            elif fetch == 'dict':
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except SQLAlchemyError as e:
            print('Database error:', e)
            raise

    def close(self):
        """Close the engine if it has been created."""
        if self.engine:
            self.engine.dispose()