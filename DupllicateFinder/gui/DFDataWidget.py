import sys
import os
sys.path.append(os.path.abspath('../../DupllicateFinder'))

from DupllicateFinder.config import DFConfig
from DupllicateFinder.util   import DFLogger
from DupllicateFinder.model  import DFAppData

from PyQt5.QtWidgets import QWidget

class DFDataWidget(QWidget):
    def __init__(self, model, logger):
        super().__init__()
        self.init_logger(logger)
        self.init_data(model)
        
    def init_logger(self, logger):
        if (isinstance(logger, DFLogger)):
            self.logger = logger
        else:
            self.logger = DFLogger(DFConfig.DF_APPLICATION_LOG_LEVEL)

    def init_data(self, model):
        self.logger.log_line(3, 'DFDataWidget.init_data')
        if (isinstance(model, DFAppData)):
            self.model = model
        else:
            self.model = DFAppData()