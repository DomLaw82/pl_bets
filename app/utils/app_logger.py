import logging
from fluent import handler as fluent_handler
import requests
import os
import re
from define_environment import load_correct_environment_variables

load_correct_environment_variables()

class FluentLogger:
    def __init__(self, tag: str, host: str = os.getenv("FLUENT_APP_HOST_NAME"), port: int = 24224, level=logging.DEBUG):
        """
        Initialize the Fluent Logger.

        Args:
            tag (str): Tag used for Fluentd to categorize incoming logs.
            host (str): Hostname of the Fluentd server.
            port (int): Port number on which Fluentd server is listening.
            level (logging.level): Minimum logging level for the logger.
        """
        self.tag = tag
        self.host = host
        self.port = port
        self.level = level
        
        self.logger = logging.getLogger(self.tag)
        self.logger.setLevel(self.level)
        self.logger.propagate = False

        # Fluentd handler
        fluent = fluent_handler.FluentHandler(self.tag, host=self.host, port=self.port)
        fluent.setLevel(self.level)
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

    def __repr__(self):
        return f"FluentLogger(tag={self.tag}, host={self.host}, port={self.port}, level={self.level})"

    def __str__(self):
        return f"FluentLogger for module {self.logger.name}"

    def get_logger(self):
        """
        Returns the configured logger.

        Returns:
            logging.Logger: The configured logger object.
        """
        return self.logger
    
    def log_http_request(self, url, response: requests.Response):
        """Helper function to log HTTP request and response details"""
        self.logger.debug(f"Request to {url} executed")
        self.logger.debug(f"Response code: {response.status_code}")
        self.logger.debug(f"Response reason: {response.reason}")

    def log_sql_query_execution(self, query: str):
        """Helper function to log SQL queries"""
        self.logger.debug("Executing SQL query: {}".format(re.sub(r'\s+', ' ', query.replace('\n', ' ').replace('\t', ' ')).strip()))

    def log_error(self, error_message: Exception):
        """Helper function to log error messages"""
        self.logger.error(f"Error : {error_message.__context__} : line {error_message.__traceback__.tb_lineno} : {error_message}")