#!/usr/bin/env python3
import os
from DupllicateFinder.config import DFConfig
from DupllicateFinder.util import DFLogger
from DupllicateFinder.scan import DFScanner

logger = DFLogger(2, output='stdout')
scanner = DFScanner(logger, 'sha1')
scanner.find_duplicates_json('/mnt/d/Code')
#with open('output.json', 'w') as f:
#    f.write(duplicates_json)
#print(duplicates_json)