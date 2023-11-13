import logging
import sys
import os
from .config import config

# Create a logger
logger = logging.getLogger('you_look_fine')
logger.setLevel(logging.DEBUG)  # Set the minimum logged level to DEBUG

# Check if the log directory exists and create it if it doesn't
if not os.path.exists('log'):
    os.makedirs('log')

# Create a file handler that logs debug and higher level messages to a file
file_handler = logging.FileHandler('log/you_look_fine.log')
file_handler.setLevel(logging.DEBUG)

# Create a stream handler that logs info and higher level messages to sys.stdout
stream_handler = logging.StreamHandler(sys.stdout)
log_level = logging.DEBUG if config['debug'] else logging.INFO
stream_handler.setLevel(log_level)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)