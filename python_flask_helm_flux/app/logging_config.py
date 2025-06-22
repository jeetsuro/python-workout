import logging
import logging.config

LOG_CONFIG={
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] [%(levelname)s] [%(module)s] : %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "default",
                }
            },
            "root": {"level": "DEBUG", "handlers": ["console"]},
}

def setup_logging () -> logging :
    logger = logging
    logger.config.dictConfig(LOG_CONFIG)
    return logger
