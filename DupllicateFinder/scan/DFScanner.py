
import sys
import os
import hashlib
import json
import traceback
import multiprocessing
import psutil
import time
import sqlite3

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
        self.num_cores = multiprocessing.cpu_count()
        self.processes = []
        # self.manager = multiprocessing.Manager()
        #self.temp_path_store = self.manager.list()
        #self.temp_store = self.manager.list()
        # self.lock = multiprocessing.Lock()
        self.output_results = []
        self.temp_lim = 1000
        self.process_limit = 100
        self.task_limit = 10
        self.max_open_files = 1000
        self.i = 0

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
        self.logger.log_line(log_verbosity, '[' + str(os.getpid()) + '] ' + log_string)

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

    def close_open_file_descriptors(self):
        process = psutil.Process()
        open_files = process.open_files()
    
        for open_file in open_files:
            fd = open_file.fd
            try:
                os.close(fd)
                self.log_statement(4, f"Closed file descriptor: {fd}")
            except OSError as e:
                self.log_statement(4, f"Error closing file descriptor {fd}: {e}")
        #process.terminate()

    def close_all_file_descriptors(self):
        for process in self.processes:
            try:
                process = psutil.Process(process.pid)
                try:
                    for open_file in process.open_files():
                        print(str(process.pid) + ' - ' + open_file.path)
                except:
                    pass
            except psutil.NoSuchProcess:
                process.terminate()
                self.processes.remove(process)
            
    def digest_file(self, input_file_name, algorithm=None):
        self.log_statement(4, 'Processing: ' + input_file_name)
        algorithm = algorithm or self.hash_algorithm
        hash_ret_data = None
        try:
            with open(input_file_name, 'br') as file_handle: 
                self.log_statement(4, 'Opened ' + str(self.get_open_file_descriptors()))
                """ may need this for a ticker later
                dot_tick = 0
                dot_tick_mod = (1024 * 2048) * 1.5
                dot_tick_print_mod = 1024 * 32
                """
                hash_digest_algorithm = self.digest_get_instance(algorithm)
                for file_content_line in file_handle:
                    hash_digest_algorithm.update(file_content_line)
                hash_ret_data = hash_digest_algorithm.hexdigest()
                self.log_statement(3, hash_ret_data + ' - ' + input_file_name)
                self.log_statement(4, 'Closed ' + str(self.get_open_file_descriptors()))
        except OSError:
            self.log_statement(4, 'Skipping: ' + input_file_name)
        except ValueError:
            self.log_statement(4, 'Skipping (Could not digest): ' + input_file_name)
        self.close_open_file_descriptors()
        return ( input_file_name, hash_ret_data )

    def db_worker(self, temp_store):
        self.log_statement(4, 'DB Worker lock')
        #self.lock.acquire()
        with sqlite3.connect('hashes.db') as conn:
            conn.execute('PRAGMA journal_mode=WAL;')
            conn.execute('CREATE TABLE IF NOT EXISTS paths (path TEXT PRIMARY KEY, hash_key TEXT);')
            count = conn.execute('SELECT COUNT(*) FROM paths').fetchone()[0]
            self.log_statement(2, 'DB Worker: ' + str(count) + ' entries')
            #print('Writing 100 DB Writes')
            cursor = conn.cursor()
            query = 'INSERT OR IGNORE INTO paths (path, hash_key) VALUES (?, ?)'
            cursor.executemany(query, temp_store)
            self.log_statement(3, 'DB Worker: ' + str(len(temp_store)) + ' entries')
            #print('Wrote 100 DB Writes')
            conn.commit()
            self.output_results[:] = []
        # self.log_statement(4, 'DB Worker unlocking')
        # self.close_open_file_descriptors()
        # self.lock.release()
        # self.log_statement(4, 'DB Worker unlock')

    def add_hash_storage_entry(self, hash_value, dir_entry_object):
        self.log_statement(4, 'self.add_hash_storage_entry')
        if hash_value and dir_entry_object:
            self.log_statement(4, 'add hash storage lock')
            self.log_statement(3, '[' + str(len(self.temp_store)) +  '] ' + hash_value + ' - ' + dir_entry_object)
            self.temp_store.append((dir_entry_object, hash_value))
            if len(self.temp_store) >= 250:
                #print('Queued 100 DB writes')
                self.db_worker(self.temp_store)
                self.temp_store[:] = []
    
    def worker_function(self, entries):
        self.log_statement(4, 'self.worker_function')
        # temp_path = self.entry[0] + os.path.sep + filename
        # self.temp_path_store.append(temp_path)
        self.log_statement(4, 'self.worker_function Entering pool')
        with multiprocessing.Pool(processes=self.process_limit, maxtasksperchild=self.task_limit) as pool:
            self.log_statement(4, 'self.worker_function pool started')
            # self.log_statement(4, 'self.temp_path_store limit reached')
            self.log_statement(4, 'calling pool.starmap')
            #self.start_process_with_retry(self.digest_file, args=(filepath,))
            results = pool.starmap(self.digest_file, [ (digestfile, ) for digestfile in entries ] )
            #for process in self.processes:
            #    process.join()
            #self.temp_path_store[:] = []
        if len(results) > 0:
            self.output_results.extend(results)
        if len(self.output_results) > 250:
            self.db_worker(results)


    # Function to get the number of open file descriptors
    def get_open_file_descriptors(self):
        self.log_statement(4, 'self.get_open_file_descriptors')
        process = psutil.Process()
        try:
            # On Unix-like systems, use num_fds()
            num_fds = process.num_fds()
        except AttributeError:
            # On Windows, use open_files() and count the number of open files
            num_fds = len(process.open_files())
        return num_fds
   
    # Function to start a process with retry mechanism
    def start_process_with_retry(self, target_func, args=()):
        self.log_statement(4, 'self.start_process_with_retry')
        while True:
            num_fds = self.get_open_file_descriptors()
            #print(num_fds)
            if num_fds < self.max_open_files:
                p = multiprocessing.Process(target=target_func, args=args)
                self.processes.append(p)
                p.start()
                return p
            else:
                self.log_statement(4, f"Resource limit reached: {num_fds} open file descriptors. Retrying...")
                self.close_all_file_descriptors()
                self.log_statement(4, f"Closed all file descriptors. Retrying...")
                # time.sleep(1)

    def enumerate_directory(self, input_path_name=''):
        self.log_statement(4, 'self.enumerate_directory')
        for entry in os.walk(input_path_name):
            if (os.path.isdir(entry[0])):
                self.entry = entry
                self.log_statement(4, 'calling self.worker_function')
                self.worker_function([ entry[0] + os.path.sep + sub for sub in entry[2] ])

        return self.hash_storage

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