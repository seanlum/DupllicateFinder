import sys
import os
sys.path.append(os.path.abspath('../../DupllicateFinder'))

from DupllicateFinder.util import DFSingletonMeta

class DFAppData(metaclass=DFSingletonMeta):
    def __init__(self):
        self.data = {}

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)