#!/usr/bin/env python3
import os
import sys
from DupllicateFinder.config import DFConfig
from DupllicateFinder.util import DFLogger
from DupllicateFinder.scan import DFScanner

if __name__ == '__main__':
    logger = DFLogger(4, output='stdout')
    scanner = DFScanner(logger, 'sha512', 'test.db')
    scanner.enumerate_directory('.' + os.path.sep +  'test')
    for entry in scanner.db_get_duplicates():
        sys.stdout.write(entry[0] + ' (' + str(entry[2]) + ' duplicates) \n')
        for path in entry[1]:
            sys.stdout.write('\t' + path + '\n')