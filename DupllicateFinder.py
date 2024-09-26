# Written by https://www.github.com/seanlum
# seanjklum@gmail.com
# October, 06, 2021
import os
import hashlib
import json

debug_level = 0


# 0 means quiet
# 1 means Output: Stdout for results
# 2 means Feedback: Entry Names (Directories/Files)
# 3 means Verbose: Entry Names and Hashes
# 4 means Debug: Verbose + TimeDate Data
def log_statement(log_verbosity=0, log_string='', log_end=None):
    if log_verbosity <= debug_level:
        if log_end is not None:
            print(log_string, end=log_end)
        else:
            print(log_string)

def digest_get_instance(algorithm='sha256'):
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

def digest_file(input_file_name=os.DirEntry, algorithm='sha256'):
    if input_file_name == '':
        os.error('Invalid file name')
        exit()
    else:
        try:
            with open(input_file_name, 'br') as file_handle:
                dot_tick = 0
                dot_tick_mod = (1024 * 2048) * 1.5
                dot_tick_print_mod = 1024 * 32
                hash_digest_algorithm = digest_get_instance(algorithm)
                log_statement(3, 'Hashing:\n.', log_end='')
                for file_content_line in file_handle:
                    hash_digest_algorithm.update(file_content_line)
                    dot_tick = dot_tick + 1
                    if (dot_tick % dot_tick_mod) == 0:
                        log_statement(3, '', log_end='\n')
                    if (dot_tick % dot_tick_print_mod) == 0:
                        log_statement(3, '.', log_end='')
                file_handle.close()
                hash_ret_data = hash_digest_algorithm.hexdigest()
                log_statement(3, '')
                log_statement(3, str('Result Hash:\t' + hash_ret_data))
                return hash_ret_data
        except OSError:
            os.error('Could not open file for reading')
            exit()
        except ValueError:
            os.error('Could not read or digest file')
            exit()


def scan_directory(input_path_name=''):
    if input_path_name == '':
        os.error('Invalid path name')
        exit()
    else:
        try:
            with os.scandir(input_path_name) as starting_point:
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
            os.error('Could not open directory or file for reading')
            exit()


def item_in_list(item_to_check, list_to_check):
    try:
        if list_to_check.index(item_to_check):
            return True
        else:
            return False
    except ValueError:
        return False


def add_hash_storage_entry(hash_storage, hash_value, dir_entry_object):
    not_present = 0
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


def enumerate_directory(input_path_name=''):
    log_statement(2, str('Starting from: ' + input_path_name))
    hash_storage = {}
    output_files = list()
    entries = scan_directory(input_path_name)
    processing_files = list()
    processing_files.extend(entries['files'])
    processing_directories = list()
    processing_directories.extend(entries['directories'])
    processed_entries = []
    while (len(processing_files) > 0) or (len(processing_directories) > 0):
        for file_in_analysis in processing_files:
            if item_in_list(file_in_analysis.path, processed_entries):
                os.error('Duplicate entry being skipped')
                os.error(file_in_analysis.path)
                pass
            processing_files.remove(file_in_analysis)
            log_statement(2, str('Appending:\t' + file_in_analysis.path))
            output_files.append(os.path.abspath(file_in_analysis.path))
            ## add_hash_storage_entry(hash_storage, digest_file(file_in_analysis), file_in_analysis.path)
            processed_entries.append(file_in_analysis.path)
        for directory_entry in processing_directories:
            if item_in_list(directory_entry.path, processing_directories):
                os.error('Duplicate entry being skipped')
                os.error(directory_entry.path)
                pass
            processing_directories.remove(directory_entry)
            log_statement(2, str("Inspecting Directory: " + directory_entry.path))
            new_entries = scan_directory(directory_entry)
            if (len(new_entries['files']) == 0) and (len(new_entries['directories']) == 0):
                log_statement(3, 'Empty directory...')
            processing_directories.extend(new_entries['directories'])
            processing_files.extend(new_entries['files'])
    return output_files


def find_duplicates_json(directory_to_search):
    dup_data = enumerate_directory(directory_to_search)
    duplicates_dictionary = {}
    for data_key, data_value in dup_data.items():
        if len(data_value) > 1:
            duplicates_dictionary[data_key] = data_value
            log_statement(2, 'Hash with duplicates: ' + data_key)
            for duplicate_entry in data_value:
                log_statement(2, '\t ' + duplicate_entry.replace(directory_to_search, './'))
            log_statement(2, '')
    output_json = json.dumps(duplicates_dictionary, indent='    ')
    return output_json


__exports__ = ['log_statement', 'digest_file', 'scan_directory', 'enumerate_directory', 'find_duplicates_json']
