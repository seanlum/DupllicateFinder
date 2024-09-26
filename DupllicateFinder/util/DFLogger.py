import logging

import sys
import os
sys.path.append(os.path.abspath('../../DupllicateFinder'))

from DupllicateFinder.config import DFConfig
from .DFSingletonMeta    import DFSingletonMeta
from .DFFlushFileHandler import DFFlushFileHandler

# Set the log level to 3 for debugging
# Log level 0 is no logging
# Log level 1 is errors only
# Log level 2 is errors and warnings
# Log level 3 is errors, warnings, and info
# Log level 4 is debug, errors, warnings, and info
class DFLogger(metaclass=DFSingletonMeta):
    log_level = 3
    
    def emit(self, record):
        super().emit(record)
        self.flush()

    def __init__(self, base_log_level):
        print('DFLogger.__init__')
        self.log_level = base_log_level
        logging_level = logging.DEBUG
        logging_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging_handlers = [ DFFlushFileHandler(DFConfig.DF_APPLICATION_LOG_FILENAME, mode='w') ]
        logging.basicConfig(level=logging_level, format=logging_format, handlers=logging_handlers)
        self.log = logging
        print(self.log)

    def log_by_level(self, level, message):
        if (self.log is None):
            print('Logger not initialized')
            quit()
        if (self.log_level >= level):
            if (level == 1):
                self.log.error(message)
            elif (level == 2):
                self.log.warning(message)
            elif (level == 3):
                self.log.info(message)
            elif (level == 4):
                self.log.debug(message)

                
    def log_line(self, level, message):
        self.log_by_level(level, message)

    def log(self, level, message):
        self.log_by_level(level, message)