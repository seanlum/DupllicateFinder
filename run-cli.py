#!/usr/bin/env python3
import os
import sys
from DupllicateFinder.config import DFConfig
from DupllicateFinder.util import DFLogger
from DupllicateFinder.scan import DFScanner

logger = DFLogger(4, output='stdout')
scanner = DFScanner(logger, 'sha1', 'test.db')
scanner.enumerate_directory('./test')
for entry in scanner.db_get_duplicates():
    sys.stdout.write(entry[0] + ' (' + str(entry[2]) + ' duplicates) \n')
    for path in entry[1]:
        sys.stdout.write('\t' + path + '\n')