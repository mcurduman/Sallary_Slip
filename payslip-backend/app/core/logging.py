from flask import Flask
from logging.config import dictConfig
from app.core.config import get_settings

cfg = get_settings()
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'app.log'
        }
    },
    'root': {
        'level': cfg.LOG_LEVEL if hasattr(cfg, 'LOG_LEVEL') else 'INFO',
        'handlers': ['console', 'file']
    }
})  
