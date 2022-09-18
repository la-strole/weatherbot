import logging
import os
from typing import Dict, Optional

# Add logger
logger = logging.getLogger('handlers')
f_handler = logging.FileHandler('log.txt')
f_format = logging.Formatter('%(asctime)s - %(name)s - '
                             '%(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
logger.setLevel(os.getenv('LOG_LEVEL', 'DEBUG'))

forcast_history: Dict[int, Optional[Dict[int, str]]] = {}
