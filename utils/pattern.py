# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: pattern.py

class Singleton(type):
    """
    单例 metaclass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
