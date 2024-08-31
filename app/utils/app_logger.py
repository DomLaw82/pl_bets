import logging
from fluent import handler as fluent_handler
import requests
import os

class FluentLogger:
    def __init__(self, tag, host=os.getenv("FLUENT_APP_HOST_NAME"), port=24224, level=logging.DEBUG):
        """
        Initialize the Fluent Logger.

        Args:
            tag (str): Tag used for Fluentd to categorize incoming logs.
            host (str): Hostname of the Fluentd server.
            port (int): Port number on which Fluentd server is listening.
            level (logging.level): Minimum logging level for the logger.
        """
        self.logger = logging.getLogger(tag)
        self.logger.setLevel(level)
        self.logger.propagate = False

        # Fluentd handler
        fluent = fluent_handler.FluentHandler(tag, host=host, port=port)
        fluent.setLevel(level)
        fluent.setFormatter(
            fluent_handler.FluentRecordFormatter({
				'host': '%(hostname)s',
				'where': '%(module)s.%(funcName)s',
				'type': '%(levelname)s',
				'stack_trace': '%(exc_text)s'
			})
        )

        # # Console handler
        # console = logging.StreamHandler()
        # console.setLevel(level)
        # console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # console.setFormatter(console_formatter)

        # # Add handlers to the logger
        # self.logger.addHandler(console)
        self.logger.addHandler(fluent)

    def get_logger(self):
        """
        Returns the configured logger.

        Returns:
            logging.Logger: The configured logger object.
        """
        return self.logger
    
    def log_http_request(self, url, response: requests.Response):
        """Helper function to log HTTP request and response details"""
        self.logger.debug(f"Request to {url} executed - response code: {response.status_code}")
        self.logger.debug(f"Response code: {response.status_code}")
        self.logger.debug(f"Response reason: {response.reason}")

    def log_sql_query_execution(self, query: str):
        """Helper function to log SQL queries"""
        self.logger.debug(f"Executing SQL query: {query}")

    def log_error(self, error_message: Exception):
        """Helper function to log error messages"""
        self.logger.error(f"Error : line {error_message.__traceback__.tb_lineno} : {error_message}")