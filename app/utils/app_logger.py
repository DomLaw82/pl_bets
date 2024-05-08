import logging
from fluent import handler as fluent_handler
import os

class FluentLogger:
    def __init__(self, tag, host=os.getenv("FLUENT_APP_HOST_NAME"), port=24224, level=logging.INFO):
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
