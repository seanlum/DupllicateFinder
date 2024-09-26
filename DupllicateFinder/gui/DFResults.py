from .DFDataWidget import DFDataWidget

from PyQt5.QtWidgets import QGroupBox, QGridLayout, QTextEdit
from PyQt5.QtCore import QRect

class DFResults(DFDataWidget):
    def __init__(self, model, logger):
        super().__init__(model, logger)
        self.logger.log_line(3, 'DFResults.__init__')
        self.init_ui()
    
    def init_results_text(self):
        self.logger.log_line(3, 'DFResults.init_results_text')
        path_label = QTextEdit()
        path_label.wordWrapMode()
        path_label.setText('')
        path_label.move(20, 20)
        self.main_layout.addWidget(path_label)

    def init_ui(self):
        self.logger.log_line(3, 'DFResults.init_ui')
        self.results_column = QGroupBox()
        self.results_column.setGeometry(QRect(620, 10, 800, 400))
        self.main_layout = QGridLayout(self.results_column)
        self.setLayout(self.main_layout)