from .DFDataWidget import DFDataWidget

from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog, QComboBox, QGroupBox, QGridLayout
from PyQt5.QtCore import QRect

class DFOptions(DFDataWidget):
    def __init__(self, model, logger):
        super().__init__(model, logger)
        self.logger.log_line(3, 'DFOptions.__init')
        self.init_ui()
        
    def select_directory(self):
        self.logger.log_line(3, 'DFOptions.select_directory')
        # for when a directory is selected
        pass
    
    def hash_algo_change(self, text):
        self.logger.log_line(3, 'DFOptions.hash_algo_change')
        self.logger.log_line(4, f"Hash Algo Changed: {text}")
        self.logger.log_line(4, str(self.model.get_data('argv')))
        self.logger.log_line(4, 'Got data')
        pass
    
    def select_file(self):
        self.logger.log_line(3, 'DFOptions.select_file')
        # for when a file is selected
    
    def scan_files(self):
        self.logger.log_line(3, 'DFOptions.scan_files')
        # for when the scan button is clicked

    def init_options_log_label(self):
        self.logger.log_line(3, 'DFOptions.init_options_log_label')
        options_log_label = QLabel()
        options_log_label.move(20, 20)
        options_log_label.setText("For when the checkboxes change")
        self.main_layout.addWidget(options_log_label)

    def init_start_button(self):
        self.logger.log_line(3, 'DFOptions.init_start_button')
        scan_button = QPushButton()
        scan_button.setText("Scan for duplicates")
        scan_button.clicked.connect(self.scan_files)
        self.main_layout.addWidget(scan_button)
    
    def init_hash_path_button(self):
        self.logger.log_line(3, 'DFOptions.init_hash_path_button')
        hash_path_button = QPushButton()
        hash_path_button.setText("Select File")
        hash_path_button.move(40, 40)
        hash_path_dialog = QFileDialog()
        hash_path_dialog.setFileMode(QFileDialog.AnyFile)
        hash_path_button.clicked.connect(self.select_file)
        self.main_layout.addWidget(hash_path_button)

    def init_hash_path_label(self):
        self.logger.log_line(3, 'DFOptions.init_hash_path_label')
        path_field_label = QLabel()
        path_field_label.setText("Path of File to Hash: (single file mode)")
        path_field_label.wordWrap()
        path_field_label.move(40, 20)
        self.main_layout.addWidget(path_field_label)

    def init_scan_path_button(self):
        self.logger.log_line(3, 'DFOptions.init_scan_path_button')
        scan_path_button = QPushButton()
        scan_path_button.setText("Select Directory")
        scan_path_button.move(40, 20)
        scan_path_button.clicked.connect(self.select_directory)
        scan_path_dialog = QFileDialog()
        scan_path_dialog.setFileMode(QFileDialog.Directory)
        self.main_layout.addWidget(scan_path_button)

    def init_scan_path_label(self):
        self.logger.log_line(3, 'DFOptions.init_scan_path_label')
        scan_path_label = QLabel()
        scan_path_label.setText("Path to Scan: (directory mode)")
        scan_path_label.wordWrap()
        scan_path_label.move(40, 20)
        self.main_layout.addWidget(scan_path_label)
    
    def init_option_checkbox(self, option):
        pass 
    
    def init_options_checkbox(self):
        self.logger.log_line(3, 'DFOptions.init_options_checkbox')
        soft_options = [
            { 'title' : 'JSON Output Database File', 'option' : 'JSON_DB_OUTPUT', 'enabled' : 'no' },
            { 'title' : 'SQLite3 Internal Database', 'option' : 'SQLITE_DB_INIT', 'enabled' : 'no' },
            { 'title' : 'Log Activities in Software', 'option' : 'LOG_FS_ACTIVITY', 'enabled' : 'no' }
        ]
        [self.init_option_checkbox(option) for option in soft_options]

    def init_hash_algo_combo(self):
        self.logger.log_line(3, 'DFOptions.init_hash_algo_combo')
        combo_box = QComboBox()
        combo_box.move(20, 20)
        combo_box.addItem("sha256")
        combo_box.addItem("md5")
        combo_box.addItem("sha1")
        combo_box.addItem("sha512")
        combo_box.activated[str].connect(self.hash_algo_change)
        combo_box.setCurrentText("sha256")
        self.main_layout.addWidget(combo_box)

    def init_hash_algo_label(self):
        self.logger.log_line(3, 'DFOptions.init_hash_algo_label')
        hash_algo_label = QLabel()
        hash_algo_label.move(20, 20)
        hash_algo_label.setText("sha256 (hash options and checkbox options do not work)")
        hash_algo_label.wordWrap()
        self.main_layout.addWidget(hash_algo_label)

    def init_header(self):
        self.logger.log_line(3, 'DFOptions.init_header')
        dupllicate_header_label = QLabel()
        dupllicate_header_label.wordWrap()
        dupllicate_header_label.setText("DupllicateFinder - a file-checksum-based duplicate file detector")
        dupllicate_header_label.move(20, 20)
        self.main_layout.addWidget(dupllicate_header_label)

    def init_ui(self):
        self.logger.log_line(3, 'DFOptions.init_ui')
        self.main_column = QGroupBox()
        self.main_column.setGeometry(QRect(10, 10, 600, 400))
        self.main_layout = QGridLayout(self.main_column)
        self.init_header()
        self.init_scan_path_label()
        self.init_scan_path_button()
        self.init_hash_algo_label()
        self.init_hash_algo_combo()
        self.init_hash_path_label()
        self.init_hash_path_button()
        self.init_options_checkbox()
        self.init_options_log_label()
        self.init_start_button()
        self.logger.log_line(3, 'DFOptions.init_ui bootstrapping done')
        self.setLayout(self.main_layout)
        self.logger.log_line(3, 'DFOptions.init_ui done')