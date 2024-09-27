
import sys
import os
import hashlib
import json
import traceback
sys.path.append(os.path.abspath('../../DupllicateFinder'))

from DupllicateFinder.config import DFConfig
from DupllicateFinder.util import DFSingletonMeta, DFLogger

class DFScanner(metaclass=DFSingletonMeta):
    def __init__(self, logger, hash_algorithm):
        super().__init__()
        if (isinstance(logger, DFLogger)):
            self.logger = logger
        else:
            self.logger = DFLogger(DFConfig.DF_APPLICATION_LOG_LEVEL)
        if hash_algorithm != None:
            self.hash_algorithm = hash_algorithm
        else:
            self.hash_algorithm = 'sha1'

    def item_in_list(self, item_to_check, list_to_check):
        try:
            if list_to_check.index(item_to_check):
                return True
            else:
                return False
        except ValueError:
            return False

    # 0 means quiet
    # 1 means Output: Stdout for results
    # 2 means Feedback: Entry Names (Directories/Files)
    # 3 means Verbose: Entry Names and Hashes
    # 4 means Debug: Verbose + TimeDate Data        
    def log_statement(self, log_verbosity=0, log_string='', log_end=None):
        print(log_verbosity, log_string)
        self.logger.log_line(log_verbosity, log_string)

    def digest_get_instance(self, algorithm=None):
        if algorithm == None:
            algorithm = self.hash_algorithm
        if algorithm == 'md5':
            return hashlib.md5()
        elif algorithm == 'sha1':
            return hashlib.sha1()
        elif algorithm == 'sha224':
            return hashlib.sha224()
        elif algorithm == 'sha256':
            return hashlib.sha256()
        elif algorithm == 'sha384':
            return hashlib.sha384()
        elif algorithm == 'sha512':
            return hashlib.sha512()
        else:
            os.error('Invalid algorithm')
            exit()
            
    def digest_file(self, input_file_name=os.DirEntry, algorithm=None):
        if algorithm == None:
            algorithm = self.hash_algorithm
        if input_file_name == '':
            os.error('Invalid file name')
            exit()
        else:
            try:
                with open(input_file_name, 'br') as file_handle:
                    dot_tick = 0
                    dot_tick_mod = (1024 * 2048) * 1.5
                    dot_tick_print_mod = 1024 * 32
                    hash_digest_algorithm = self.digest_get_instance(algorithm)
                    # self.log_statement(3, 'Hashing:\n.', log_end='')
                    for file_content_line in file_handle:
                        hash_digest_algorithm.update(file_content_line)
                        dot_tick = dot_tick + 1
                        if (dot_tick % dot_tick_mod) == 0:
                            pass
                            # self.log_statement(3, '', log_end='\n')
                        if (dot_tick % dot_tick_print_mod) == 0:
                            pass
                            # log_statement(3, '.', log_end='')
                    file_handle.close()
                    hash_ret_data = hash_digest_algorithm.hexdigest()
                    # log_statement(3, '')
                    # self.log_statement(3, str('Result Hash:\t' + hash_ret_data))
                    return hash_ret_data
            except OSError:
                self.log_statement(4, 'Skipping: ' + input_file_name)
            except ValueError:
                self.log_statement(4, 'Skipping (Could not digest): ' + input_file_name)
                
    def scan_directory(self, input_path_name=''):
        if input_path_name == '':
            os.error('Invalid path name')
            exit()
        else:
            try:
                self.log_statement(3, 'Scanning: ' + str(input_path_name))
                starting_point = os.scandir(input_path_name)
                results = {
                    "path": input_path_name,
                    "files": [],
                    "directories": [],
                }
                for dir_entry in starting_point:
                    if dir_entry.is_file():
                        results['files'].append(dir_entry)
                    elif dir_entry.is_dir():
                        results['directories'].append(dir_entry)
                    else:
                        os.error('Neither file nor directory')
                starting_point.close()
                return results
            except OSError:
                self.log_statement(3, 'Skipping ' + str(input_path_name))
                # os.error('Could not open directory or file for reading')
            except Exception as e:
                self.log_statement(3, 'Skipping ' + str(input_path_name))
                # os.error('Could not scan directory')
                #os.error(traceback.format_exc())
                # exit()
             

    def add_hash_storage_entry(self, hash_storage, hash_value, dir_entry_object):
        not_present = 0
        if (hash_value == None) or (hash_value == ''):
            return
        try:
            if hash_storage[hash_value] and (hash_storage[hash_value].append is not None):
                pass
            else:
                not_present = 1
        except KeyError:
            not_present = 1
        if not_present != 0:
            hash_storage[hash_value] = list()
        hash_storage[hash_value].append(dir_entry_object)
        if (len(hash_storage[hash_value]) > 1):
            self.log_statement(3, 'Duplicate: ' + hash_value)
            for entry in hash_storage[hash_value]:
                self.log_statement(3, '\t' + entry)
            self.log_statement(3, '')
        
    def enumerate_directory(self, input_path_name=''):
        hash_storage = {}
        for entry in os.walk(input_path_name):
            if (os.path.isdir(entry[0])):
                for entryfile in entry[2]:
                    temp_path = entry[0] + os.path.sep + entryfile    
                    # self.log_statement(4, 'Processing: ' + temp_path)    
                    output_hash = self.digest_file(temp_path)
                    self.add_hash_storage_entry(hash_storage, output_hash, temp_path)
        return hash_storage

    def find_duplicates_json(self, directory_to_search):
        dup_data = self.enumerate_directory(directory_to_search)
        duplicates_dictionary = {}
        for data_key, data_value in dup_data.items():
            if len(data_value) > 1:
                duplicates_dictionary[data_key] = data_value
                self.log_statement(2, 'Hash with duplicates: ' + data_key)
                for duplicate_entry in data_value:
                    self.log_statement(2, '\t ' + duplicate_entry.replace(directory_to_search, './'))
                self.log_statement(2, '')
        output_json = json.dumps(duplicates_dictionary, indent='    ')
        return output_json