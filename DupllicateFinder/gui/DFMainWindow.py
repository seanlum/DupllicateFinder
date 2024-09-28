import sys
import os
sys.path.append(os.path.abspath('../../DupllicateFinder'))

from DupllicateFinder.util   import DFLogger
from DupllicateFinder.config import DFConfig
from DupllicateFinder.model  import DFAppData

from .DFOptions import DFOptions
from .DFResults import DFResults

from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

class DFMainWindow(QMainWindow):
    click_count = 0
    
    def init_columns(self):
        self.logger.log_line(3, 'DFMainWindow.init_columns')
        centralWidget = QWidget()
        centralLayout = QGridLayout()
        options = DFOptions(self.model, self.logger)
        results = DFResults(self.model, self.logger)
        centralLayout.addWidget(options, 0, 0)
        centralLayout.addWidget(results, 0, 1)
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

    def init_ui(self):
        self.logger.log_line(3, 'DFMainWindow.init_ui')
        self.init_columns()
        self.setWindowTitle("DEMO GUI - Dupllicate Finder - (Alpha UI Design | Single Hash Mode)")
        self.setGeometry(0, 0, 1440, 420)
       

    def __init__(self, sys_argv, logger):
        super().__init__()
        if (isinstance(logger, DFLogger)):
            self.logger = logger
        else:
            self.logger = DFLogger(DFConfig.DF_APPLICATION_LOG_LEVEL)
        self.model = DFAppData()
        self.model.set_data('argv', sys_argv)
        self.init_ui()
        # Commenting out the code below