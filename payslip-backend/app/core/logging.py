from functools import lru_cache
import logging
import logging.config
from app.core.config import get_settings

cfg = get_settings()
logging_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s - %(asctime)s]: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': './app.log'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}
logging.config.dictConfig(logging_config)

@lru_cache()
def get_logger(name: str = None):
    return logging.getLogger(name)