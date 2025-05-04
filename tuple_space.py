# -*- coding: utf-8 -*-
# tuple_space.py

import threading
from typing import Dict

class TupleSpace:

    # Define constants for status codes
    # Define constants for status codes
    # Define constants for status codes
    OK_ADDED = "OK_ADDED"
    OK_READ = "OK_READ"
    OK_REMOVED = "OK_REMOVED"
    ERR_EXIST = "ERR_EXIST"
    ERR_NOEXIST = "ERR_NOEXIST"


    def __init__(self):
        self._data: Dict[str, str] = {}  # Internal dict to store key-value pairs
        self._lock = threading.Lock() #lock for thread safety

    def put(self, key: str, value: str):
        # Check if the key is valid

        #LBYL
        # Check if the key exists, if it does, return an error
        #if it doesn't, add the key-value pair to the dictionary
        with self._lock: # get lock to ensure thread safety
            # Check if the key already exists
            if key in self._data:
                print(f"[TupleSpace] put failed : key '{key}' already exist.")
                return False, self.ERR_EXIST #err exist
            
            else:
                self._data[key] = value
                print(f"[TupleSpace] put : key '{key}' added.")
                return True, self.OK_ADDED #ok added

    def read(self, key: str):
        with self._lock: #get lock to ensure thread safety
            # Use dictionary's get method which returns None if key is not found
            value = self._data.get(key)
            if value is not None:
                return value, self.OK_READ
                print(f"[TupleSpace] read : key '{key}' exist.")
            else:
                return None, self.ERR_NOEXIST
                print(f"[TupleSpace] read failed : key '{key}' not exist.")
                # Key does not exist, return None

    def get(self, key):
        with self._lock: # get lock to ensure thread safety
            try:
                value = self._data.pop(key)
                return value, self.OK_REMOVED
                # Key exists, remove it from the dictionary
                print(f"[TupleSpace] get : key '{key}' exist.")     
            
            except KeyError:
                # Key does not exist, return None
                print(f"[TupleSpace] get failed : key '{key}' not exist.")
                return None, self.ERR_NOEXIST

    def get_count(self) -> int:
        #safe access to the data
        #give the lock to ensure thread safety
        with self._lock: 
            return len(self._data)

    def calculate_stats(self):
        with self._lock: # get lock to ensure thread safety
            # calculate the average size of the tuples
            count = len(self._data)
            if count == 0:
                return {
                    'count': 0,
                    'avg_tuple_size': 0.0,
                    'avg_key_size': 0.0,
                    'avg_value_size': 0.0
                }


            # calculate the total size of the keys and values
            total_key_len = sum(len(key) for key in self._data.keys())
            total_value_len = sum(len(value) for value in self._data.values())
            # calculate the average size of the tuples
            # use float division to avoid integer division
            #calculate average sizes
            avg_key_size = total_key_len / count
            avg_value_size = total_value_len / count
            avg_tuple_size = (total_key_len + total_value_len) / count

            return {
                'count': count,
                'avg_tuple_size': avg_tuple_size,
                'avg_key_size': avg_key_size,
                'avg_value_size': avg_value_size
            }