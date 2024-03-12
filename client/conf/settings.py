"""
configuration file

"""
import os
import logging.config

# server address configuration
HOST = 'localhost'
PORT = 9000


# protocol configration
REQUEST_REGISTER = 'register'
REQUEST_LOGIN = 'login'
REQUEST_CHAT = 'chat'
REQUEST_FILE = 'file'
REQUEST_ONLINE = 'online'
REQUEST_OFFLINE = 'offline'
REQUEST_RECONNECT = 'reconnect'
PROTOCOL_LENGTH = 8


# color config
USER_COLOR = 'gray'
MSG_COLOR = 'black'

INTERVAL = 60

# images suffix
IMG_TYPES = ['png', 'jpg', 'jpeg', 'jif', 'bmp']

# group announcement
NOTICE = '请文明发言！'


# routes configuration
BASE_DIR = os.path.dirname(os.path.dirname(__file__))       # project root directory
INFO_LOG_DIR = os.path.join(BASE_DIR, 'log', 'info.log')
ERROR_LOG_DIR = os.path.join(BASE_DIR, 'log', 'error.log')
IMG_DIR = os.path.join(BASE_DIR, 'imgs')
FILE_DIR = os.path.join(BASE_DIR, 'datas')

LEVEL = 'DEBUG'

# log configuration dictionary
LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # log format
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
    # log handlers
    'handlers': {
        'console_debug_handler': {
            'level': LEVEL,  # limit of logging handler level
            'class': 'logging.StreamHandler',  # output into terminal
            'formatter': 'simple'  # log configuration
        },
        # 'file_info_handler': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # save as file, log rotating
        #     'filename': INFO_LOG_DIR,
        #     'maxBytes': 1024*1024*10,  # log size 10M
        #     'backupCount': 10,  # limit the number of log files that can be saved
        #     'encoding': 'utf-8',
        #     'formatter': 'standard',
        # },
        # 'file_error_handler': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # save as file, log rotating
        #     'filename': ERROR_LOG_DIR,
        #     'maxBytes': 1024*1024*10,  # log size 10M
        #     'backupCount': 10,  # limit the number of log files that can be saved
        #     'encoding': 'utf-8',
        #     'formatter': 'standard',
        # },
        # 'file_asyncio_handler': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # save as file, log rotating
        #     'filename': ASYNCIO_ERROR_LOG_DIR,
        #     'maxBytes': 1024*1024*10,  # log size 10M
        #     'backupCount': 10,  # limit the number of log files that can be saved
        #     'encoding': 'utf-8',
        #     'formatter': 'standard',
        # },
    },
    # loggers
    # 'loggers': {
    #     '': {  # 导入时logging.getLogger时使用的app_name
    #         'handlers': ['console_debug_handler', 'file_info_handler'],  # 日志分配到哪个handlers中
    #         'level': 'DEBUG',  # 日志记录的级别限制
    #         'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
    #     },
        # 'error_logger': {  # 导入时logging.getLogger时使用的app_name
        #     'handlers': ['file_error_handler', 'console_debug_handler'],  # 日志分配到哪个handlers中
        #     'level': 'ERROR',  # 日志记录的级别限制
        #     'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        # },
        # 'asyncio': {  # 导入时logging.getLogger时使用的app_name
        #     'handlers': ['file_asyncio_handler'],  # 日志分配到哪个handlers中
        #     'level': 'ERROR',  # 日志记录的级别限制
        #     'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        # },
    # }
}

logging.config.dictConfig(LOGGING_DIC)
LOGGER = logging.getLogger('client')
ERROR_LOGGER = logging.getLogger('error_logger')