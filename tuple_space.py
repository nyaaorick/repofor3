# -*- coding: utf-8 -*-
# tuple_space.py

import threading

class TupleSpace:
   
    def __init__(self):
        """初始化一个空的元组空间和用于同步的锁."""
        self._data = {}  # 内部字典，用于存储 key-value 对    store key
        self._lock = threading.Lock() # 用于保护 _data 的锁  lock

    def put(self, key, value):
        """
        尝试将 (key, value) 添加到元组空间.

        Args:
            key (str): 要添加的键.
            value (str): 要添加的值.

        Returns:
            tuple: 一个包含两个元素的元组:
                   - bool: True 如果添加成功, False 如果键已存在.
                   - str: 状态码 ("OK_ADDED" 或 "ERR_EXIST").
        """
        

        with self._lock: # 获取锁以保证线程安全 lock to protect thread
            if key in self._data:
                print(f"[TupleSpace] Attempted PUT failed: Key '{key}' already exists.")
                return False, "ERR_EXIST" # 键已存在 staus errexist
            else:
                self._data[key] = value
                print(f"[TupleSpace] Added: ({key}, {value})")
                return True, "OK_ADDED" # 添加成功 status okadded

    def read(self, key):
        """
        尝试读取键为 key 的元组的值.

        Args:
            key (str): 要读取的键.

        Returns:
            tuple: 一个包含两个元素的元组:
                   - str or None: 如果 key 存在, 返回对应的值 (str); 否则返回 None.
                   - str: 状态码 ("OK_READ" 或 "ERR_NOEXIST").
        """
        with self._lock: # 获取锁
            if key in self._data:
                value = self._data[key]
                print(f"[TupleSpace] Read: ({key}, {value})")
                return value, "OK_READ" # 读取成功 status okread
            else:
                print(f"[TupleSpace] Attempted READ failed: Key '{key}' does not exist.")
                return None, "ERR_NOEXIST" # 键不存在 status errnoexist

    def get(self, key):
        """
        尝试读取并移除键为 key 的元组.

        Args:
            key (str): 要获取并移除的键.

        Returns:
            tuple: 一个包含两个元素的元组:
                   - str or None: 如果 key 存在, 返回被移除的值 (str); 否则返回 None.
                   - str: 状态码 ("OK_REMOVED" 或 "ERR_NOEXIST").
        """
        with self._lock: # 获取锁
            if key in self._data:
                # dict.pop(key) 会返回与 key 关联的值，并从字典中移除该键值对
                value = self._data.pop(key)
                print(f"[TupleSpace] Removed: ({key}, {value})")
                return value, "OK_REMOVED" # 获取并移除成功 status okremoved
            else:
                print(f"[TupleSpace] Attempted GET failed: Key '{key}' does not exist.")
                return None, "ERR_NOEXIST" # 键不存在 status errnoexist

    def get_count(self):
      
        with self._lock: # 获取锁 
            return len(self._data)

    #test
if __name__ == '__main__':
    ts = TupleSpace()

    # 测试 PUT
    success, status = ts.put("greeting", "hello")
    print(f"PUT greeting: {success}, {status}") #  expect:   True, OK_ADDED
    success, status = ts.put("greeting", "hi")
    print(f"PUT greeting again: {success}, {status}") # expect:    False, ERR_EXIST


  