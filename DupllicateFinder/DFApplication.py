import sys
import os

sys.path.append(os.path.abspath('../'))

from DupllicateFinder.gui import DFMainWindow
from DupllicateFinder.util import DFLogger
from DupllicateFinder.config import DFConfig

from PyQt5.QtWidgets import QApplication

class DFApplication(QApplication):
    def __init__(self, sys_argv):
        self.logger = DFLogger(DFConfig.DF_APPLICATION_LOG_LEVEL)
        self.logger.log_line(3, 'DFApplication.__init__')
        super().__init__(sys_argv)
        self.window = DFMainWindow(sys_argv, self.logger)
        self.logger.log_line(3, 'DFApplication.window.show')
        self.window.show()