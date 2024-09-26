import logging

class DFFlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()