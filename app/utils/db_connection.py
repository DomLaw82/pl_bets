import os
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from app_logger import FluentLogger

log_class = FluentLogger("db-connection")
logger = log_class.get_logger()

class SQLConnection:
    """Create a PostgreSQL connection class with context management within each method."""

    def __init__(self, username: str, password: str, host: str, port: str, db_name: str):
        """Initialize connection parameters."""
        try:
            self.connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
            self.engine = None
        except Exception as e:
            logger.error(f"Error initializing database connection: {e}")
            raise e

    def connect(self):
        """Context manager that yields a connection from the pool."""
        if self.engine is None:
            self.engine = sqlalchemy.create_engine(self.connection_string, isolation_level='AUTOCOMMIT')
        return self.engine.connect()

    def get_df(self, query: str) -> pd.DataFrame:
        """Query the database and return a DataFrame, managing context internally."""
        with self.connect() as conn:
            try:
                log_class.log_sql_query_execution(query)
                res = pd.read_sql_query(query, conn)
                return res
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                raise e # Optionally re-raise the exception after logging

    def get_list(self, query: str) -> list[tuple]:
        """Execute a query and return a list of tuples, each representing a row, managing context internally."""
        try:
            with self.connect() as conn:
                log_class.log_sql_query_execution(query)
                return self._execute_query(conn, query, fetch='all')
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise e

    def get_dict(self, query: str) -> list[dict]:
        """Execute a query and return a list of dictionaries, each representing a row, managing context internally."""
        try:
            with self.connect() as conn:
                log_class.log_sql_query_execution(query)
                return self._execute_query(conn, query, fetch='dict')
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise e

    def execute(self, query) -> None:
        """Execute a non-return query, managing context internally."""
        try:
            with self.connect() as conn:
                log_class.log_sql_query_execution(query)
                conn.execute(sqlalchemy.text(query))
        except SQLAlchemyError as e:
            logger.error(f"Error executing query: {e}")
            raise e

    def _execute_query(self, conn, query: str, fetch='all') -> list:
        """Helper method to execute queries and manage fetch types."""
        try:
            log_class.log_sql_query_execution(query)
            result = conn.execute(sqlalchemy.text(query))
            if fetch == 'all':
                return result.fetchall()
            elif fetch == 'dict':
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        except SQLAlchemyError as e:
            logger.error(f"Error executing query: {e}")
            raise e

    def close(self):
        """Close the engine if it has been created."""
        if self.engine:
            self.engine.dispose()