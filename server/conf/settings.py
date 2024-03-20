"""
Configuration file for the server.

This configuration file sets up the necessary parameters and logging for the server. It includes settings for server address, protocol configurations, paths for logs and data storage, and logging configurations.
"""

import os
import logging.config

# Server address configuration
HOST = 'localhost'
PORT = 9000

# Protocol configuration for server responses
RESPONSE_SUCCESS_CODE = 200
RESPONSE_ERROR_CODE = 400
RESPONSE_REGISTER = 'register'
RESPONSE_LOGIN = 'login'
RESPONSE_BROADCAST = 'broadcast'
RESPONSE_ONLINE = 'online'
RESPONSE_OFFLINE = 'offline'
RESPONSE_CHAT = 'chat'
RESPONSE_FILE = 'file'
RESPONSE_RECONNECT = 'reconnect'
PROTOCOL_LENGTH = 8  # The fixed length for the protocol header

# Announcement for group chats
NOTICE = 'Please speak politely!'

# Configuration for file storage and logging paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Project root directory
INFO_LOG_DIR = os.path.join(BASE_DIR, 'log', 'info.log')  # Path for info logs
ERROR_LOG_DIR = os.path.join(BASE_DIR, 'log', 'error.log')  # Path for error logs
ASYNCIO_ERROR_LOG_DIR = os.path.join(BASE_DIR, 'log', 'asyncio_error.log')  # Path for asyncio error logs
USER_DIR = os.path.join(BASE_DIR, 'db', 'users')  # Directory for user data
FILE_DIR = os.path.join(BASE_DIR, 'db', 'files')  # Directory for file transfers

LEVEL = 'DEBUG'  # Default logging level

# Log configuration dictionary
LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # Log format configurations
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s [%(name)s] %(levelname)s  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'test': {
            'format': '%(asctime)s %(message)s',
        },
    },
    'filters': {},
    # Log handlers specify where to output the logs
    'handlers': {
        'console_debug_handler': {
            'level': LEVEL,
            'class': 'logging.StreamHandler',  # Output to console
            'formatter': 'simple',
        },
        'file_info_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Rotating file handler for info logs
            'filename': INFO_LOG_DIR,
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_error_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Rotating file handler for error logs
            'filename': ERROR_LOG_DIR,
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_asyncio_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Rotating file handler for asyncio error logs
            'filename': ASYNCIO_ERROR_LOG_DIR,
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 10,
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
    },
    # Loggers define the logging behavior
    'loggers': {
        '': {  # Default logger
            'handlers': ['console_debug_handler', 'file_info_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'error_logger': {
            'handlers': ['file_error_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
        'asyncio': {
            'handlers': ['file_asyncio_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOGGING_DIC)  # Apply the logging configuration
LOGGER = logging.getLogger('server')  # General logger for server events
ERROR_LOGGER = logging.getLogger('error_logger')  # Logger for error events
