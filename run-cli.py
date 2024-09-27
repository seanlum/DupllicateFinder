#!/usr/bin/env python3
import os
from DupllicateFinder.config import DFConfig
from DupllicateFinder.util import DFLogger
from DupllicateFinder.scan import DFScanner

logger = DFLogger(DFConfig.DF_APPLICATION_LOG_LEVEL, output='stdout')
scanner = DFScanner(logger, 'sha1')
duplicates_json = scanner.find_duplicates_json('/mnt')
print(duplicates_json)