# -*- coding: utf-8 -*-
# tuple_space.py

import threading

class TupleSpace:
    """
    封装元组空间数据和操作的类.
    这个类是线程安全的.
    """
    def __init__(self):
        """初始化一个空的元组空间和用于同步的锁."""
        self._data = {}  # 内部字典，用于存储 key-value 对
        self._lock = threading.Lock() # 用于保护 _data 的锁

    def put(self, key, value):
        """
        尝试将 (key, value) 添加到元组空间.
        返回 (bool, str): (成功与否, 内部状态码)
        """
        with self._lock: # 获取锁以保证线程安全
            if key in self._data:
                # print(f"[TupleSpace] PUT 失败: 键 '{key}' 已存在.") # 可选调试
                return False, "ERR_EXIST" # 键已存在
            else:
                self._data[key] = value
                # print(f"[TupleSpace] 添加成功: ({key}, {value})") # 可选调试
                return True, "OK_ADDED" # 添加成功

    def read(self, key):
        """
        尝试读取键为 key 的元组的值.
        返回 (str or None, str): (读取到的值或None, 内部状态码)
        """
        with self._lock: # 获取锁
            if key in self._data:
                value = self._data[key]
                # print(f"[TupleSpace] 读取: ({key}, {value})") # 可选调试
                return value, "OK_READ" # 读取成功
            else:
                # print(f"[TupleSpace] READ 失败: 键 '{key}' 不存在.") # 可选调试
                return None, "ERR_NOEXIST" # 键不存在

    def get(self, key):
        """
        尝试读取并移除键为 key 的元组.
        返回 (str or None, str): (移除的值或None, 内部状态码)
        """
        with self._lock: # 获取锁
            if key in self._data:
                # dict.pop(key) 返回与 key 关联的值，并从字典中移除该键值对
                value = self._data.pop(key)
                # print(f"[TupleSpace] 移除: ({key}, {value})") # 可选调试
                return value, "OK_REMOVED" # 获取并移除成功
            else:
                # print(f"[TupleSpace] GET 失败: 键 '{key}' 不存在.") # 可选调试
                return None, "ERR_NOEXIST" # 键不存在

    def get_count(self):
        """
        返回当前元组空间中元组的数量 (线程安全).
        """
        with self._lock: # 获取锁
            return len(self._data)

    # --- 这是之前缺少的，现在已添加 ---
    def calculate_stats(self):
        """
        计算当前元组空间的统计信息 (线程安全).
        返回包含统计信息的字典.
        """
        with self._lock: # 获取锁来安全地访问数据
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
                # 假设 key 和 value 都是字符串
                total_key_len += len(key)
                total_value_len += len(value)

            # 使用浮点数除法确保结果准确
            avg_key_size = total_key_len / count
            avg_value_size = total_value_len / count
            avg_tuple_size = (total_key_len + total_value_len) / count

            return {
                'count': count,
                'avg_tuple_size': avg_tuple_size,
                'avg_key_size': avg_key_size,
                'avg_value_size': avg_value_size
            }