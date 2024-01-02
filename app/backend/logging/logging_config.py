import logging.config
from pythonjsonlogger import jsonlogger

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": f"%(asctime)s--%(levelname)s--%(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        }
    },
    "loggers": {"": {"handlers": ["stdout"], "level": "DEBUG"}},
}


logging.config.dictConfig(LOGGING)