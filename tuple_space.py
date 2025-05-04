# -*- coding: utf-8 -*-
# tuple_space.py

import threading

class TupleSpace:
    def __init__(self):
        self._data = {}  # store tuples as key-value pairs
        self._lock = threading.Lock() #lock for thread safety

    def put(self, key, value):
        # Check if the key is valid
        with self._lock: # get lock to ensure thread safety
            # Check if the key already exists
            if key in self._data:
                print(f"[TupleSpace] PUT : key '{key}' exist.") 
                return False, "ERR_EXIST" 
            
            else:
                self._data[key] = value
                print(f"[TupleSpace]  add : ({key}, {value})") 
                return True, "OK_ADDED"

    def read(self, key):
        with self._lock: #get lock to ensure thread safety
            if key in self._data:
                value = self._data[key]
                print(f"[TupleSpace] read success : ({key}, {value})") # 
                return value, "OK_READ" 
            else:
                print(f"[TupleSpace] read failed : key '{key}' not exist.")
                return None, "ERR_NOEXIST" 

    def get(self, key):
        with self._lock: # get lock to ensure thread safety
            if key in self._data:

                # 
                value = self._data.pop(key)
                
                return value, "OK_REMOVED" #
            
            else:
                print(f"[TupleSpace] get failed : key '{key}' not exist.")
                return None, "ERR_NOEXIST" #

    def get_count(self):
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

            total_key_len = 0
            total_value_len = 0
            for key, value in self._data.items():
                # calculate the length of the key and valu
                total_key_len += len(key)
                total_value_len += len(value)

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