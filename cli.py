#!/usr/bin/env python3
from DupllicateFinder import find_duplicates_json

json_file_handle = open('/Data/1938-home-directory-profile-drive.json', 'w+')
duplicates_json = find_duplicates_json('/media/seanlum/Profile')
json_file_handle.write(duplicates_json)
json_file_handle.close()
