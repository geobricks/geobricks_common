import logging
from geobricks_common.config.config import config

settings = {
    # Logging configurations
    "logging": {
        "level": config["settings"]["logging"]["level"],
        "format": "%(asctime)s | %(levelname)-8s | Line: %(lineno)-5d  | %(name)-20s | %(message)s",
        # "format": "%(asctime)s | %(levelname)-8s | Line: %(lineno)-5d | %(message)s | %(name)-20s ",
        "datefmt": "%d-%m-%Y | %H:%M:%s"
    }
}


level = settings["logging"]["level"]
format = settings["logging"]["format"]
datefmt = settings["logging"]["datefmt"]
logging.basicConfig(level=level, format=format, datefmt=datefmt)


def logger(loggerName=None):
    logger = logging.getLogger(loggerName)
    logger.setLevel(level)
    return logger