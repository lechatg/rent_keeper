import logging
import logging.config
import os

# Set path for logs directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_directory = os.path.join(base_dir, 'logs')

# Create directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        '''
        Add ":" to levelname in 'mycustom' formatter.
        '''
        original_levelname = record.levelname
        record.levelname = f"{original_levelname}:"
        formatted_message = super().format(record)
        record.levelname = original_levelname
        return formatted_message
    

def setup_logging(level=logging.DEBUG):
    level_uvicorn = logging.INFO
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'format': '%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]'
            },

            'mycustom': {
                '()': CustomFormatter,
                'datefmt': '%Y-%m-%d %H:%M:%S',
                # 'format': "[%(asctime)s.%(msecs)03d] %(name)20s:%(lineno)-3d %(levelname)-7s - %(message)s",
                'format': "[%(asctime)s.%(msecs)03d] %(name)20s:%(lineno)-3d %(levelname)-8s  %(message)s",
            },
            
            'formatter_uvicorn_console_default': {
                "()": "uvicorn.logging.DefaultFormatter",
                'datefmt': '%Y-%m-%d %H:%M:%S',
                # "fmt": "%(levelprefix)s %(message)s",
                "fmt": "[%(asctime)s.%(msecs)03d] %(name)20s:%(lineno)-3d %(levelprefix)s %(message)s",
                "use_colors": True,
            },

            "formatter_uvicorn_file_default": {
                "()": "uvicorn.logging.DefaultFormatter",
                'datefmt': '%Y-%m-%d %H:%M:%S',
                "fmt": "[%(asctime)s.%(msecs)03d] %(name)20s:%(lineno)-3d %(levelprefix)s %(message)s",
                "use_colors": False,
            },


            "formatter_uvicorn_console_access": {
                "()": "uvicorn.logging.AccessFormatter",
                'datefmt': '%Y-%m-%d %H:%M:%S',
                # "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
                'fmt': '[%(asctime)s.%(msecs)03d] %(name)20s:%(lineno)-3d %(levelprefix)-7s %(client_addr)s - "%(request_line)s" %(status_code)s',
                "use_colors": True
            },

            "formatter_uvicorn_file_access": {
                "()": "uvicorn.logging.AccessFormatter",
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'fmt': '[%(asctime)s.%(msecs)03d] %(name)20s:%(lineno)-3d %(levelprefix)-7s %(client_addr)s - "%(request_line)s" %(status_code)s',
                "use_colors": False
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'mycustom',
                'level': level,
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'mycustom',
                'level': level,
                # 'filename': 'fastapi_app.log',
                'filename': os.path.join(log_directory, 'fastapi_app.log'),
                'when': 'midnight',
                'interval': 1,  # Interval of 1 day
                'backupCount': 30,  # Store up to 30 archive log files (one for each day)
                'encoding': 'utf-8',
                'utc': True, # Use UTC for file names
            },

            'uvicorn_console_default': {
                'class': 'logging.StreamHandler',
                'formatter': 'formatter_uvicorn_console_default',
                'level': level_uvicorn,
                'stream': 'ext://sys.stdout',
            },

            'uvicorn_console_access': {
                'class': 'logging.StreamHandler',
                'formatter': 'formatter_uvicorn_console_access',
                'level': level_uvicorn,
                'stream': 'ext://sys.stdout',
            },

            'uvicorn_file_default': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'formatter_uvicorn_file_default',
                'level': level_uvicorn,
                'filename': os.path.join(log_directory, 'fastapi_app.log'),
                'when': 'midnight',
                'interval': 1,  # Interval of 1 day
                'backupCount': 30,  # Store up to 30 archive log files (one for each day)
                'encoding': 'utf-8',
                'utc': True, # Use UTC for file names
            },

            'uvicorn_file_access': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'formatter_uvicorn_file_access',
                'level': level_uvicorn,
                'filename': os.path.join(log_directory, 'fastapi_app.log'),
                'when': 'midnight',
                'interval': 1,  # Interval of 1 day
                'backupCount': 30,  # Store up to 30 archive log files (one for each day)
                'encoding': 'utf-8',
                'utc': True, # Use UTC for file names
            },

        },
        'root': {
                'handlers': ['console', 'file'],
                'level': level,
        },
        'loggers': {
            
            # Add logger for 'multipart' module
            'multipart': { 
                'handlers': ['console', 'file'],
                'level': 'INFO', # Do not need Debug level logs
                'propagate': False,
            },
            

            'uvicorn': {
                'handlers': ['uvicorn_console_default', 'uvicorn_file_default'],
                'level': level_uvicorn,
                'propagate': False,
            },
            'uvicorn.error': {
                'handlers': ['uvicorn_console_default', 'uvicorn_file_default'],
                'level': level_uvicorn,
                'propagate': False,
            },
            'uvicorn.access': {
                'handlers': ['uvicorn_console_access', 'uvicorn_file_access'],
                'level': level_uvicorn,
                'propagate': False,
            },
        },
    }

    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(__name__)
    logger.info("Logging configured.")


