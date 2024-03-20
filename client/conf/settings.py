"""
Configuration file for the application.
"""

import os
import logging.config

# Configuration for the server address
HOST = 'localhost'
PORT = 9000

# Configuration for different types of requests
REQUEST_REGISTER = 'register'
REQUEST_LOGIN = 'login'
REQUEST_CHAT = 'chat'
REQUEST_FILE = 'file'
REQUEST_ONLINE = 'online'
REQUEST_OFFLINE = 'offline'
REQUEST_RECONNECT = 'reconnect'
PROTOCOL_LENGTH = 8  # Fixed length for protocol messages

# Configuration for message and user display colors
USER_COLOR = 'gray'
MSG_COLOR = 'black'

INTERVAL = 60  # General purpose interval (e.g., for polling) in seconds

# Supported image file types
IMG_TYPES = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

# Announcement or notice to users in a group
NOTICE = 'Please speak politely!'

# Configuration for file and logging paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Root directory of the project
INFO_LOG_DIR = os.path.join(BASE_DIR, 'log', 'info.log')  # Path for info log files
ERROR_LOG_DIR = os.path.join(BASE_DIR, 'log', 'error.log')  # Path for error log files
IMG_DIR = os.path.join(BASE_DIR, 'imgs')  # Directory for storing images
FILE_DIR = os.path.join(BASE_DIR, 'datas')  # Directory for storing other data files

LEVEL = 'DEBUG'  # Default logging level

# Logging configuration dictionary
LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # Formatters define the log message format
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
    # Handlers specify the destination of the log messages
    'handlers': {
        'console_debug_handler': {
            'level': LEVEL,  # Log level for this handler
            'class': 'logging.StreamHandler',  # Output to console
            'formatter': 'simple',  # Use the simple format
        },
        'file_info_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Save to file, with log rotation
            'filename': INFO_LOG_DIR,  # Path to log file
            'maxBytes': 1024*1024*10,  # Log file size 10MB
            'backupCount': 10,  # Limit on number of log files to keep
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
        'file_error_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Save to file, with log rotation
            'filename': ERROR_LOG_DIR,  # Path to error log file
            'maxBytes': 1024*1024*10,  # Log file size 10MB
            'backupCount': 10,  # Limit on number of log files to keep
            'encoding': 'utf-8',
            'formatter': 'standard',
        },
    },
    # Loggers are the entry point of the logging system
    'loggers': {
        '': {  # Root logger
            'handlers': ['console_debug_handler', 'file_info_handler'],  # Handlers assigned to this logger
            'level': 'DEBUG',  # Logging level
            'propagate': False,  # Prevents log messages from being propagated to the root logger
        },
        'error_logger': {  # Specific logger for errors
            'handlers': ['file_error_handler', 'console_debug_handler'],  # Handlers assigned to this logger
            'level': 'ERROR',  # Logging level for this logger
            'propagate': False,  # Prevents log messages from being propagated to the root logger
        },
    }
}

logging.config.dictConfig(LOGGING_DIC)  # Applies the logging configuration
LOGGER = logging.getLogger('client')  # General logger for client events
ERROR_LOGGER = logging.getLogger('error_logger')  # Logger for error events
