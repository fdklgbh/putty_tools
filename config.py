# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: config.py
"""
    配置文件
"""

from os.path import dirname, abspath, expanduser, join

CRYPTO_KEY = 'fdklgbh'

PROJECT_PATH = abspath(dirname(__name__))

PROJECT_CONFIG_PATH = join(expanduser("~"), '.PuttyTools')

DB_FILE_NAME = 'puttyTools.db'

DB_FILE_PATH = join(PROJECT_CONFIG_PATH, DB_FILE_NAME)

PROJECT_INI_FILE = join(PROJECT_CONFIG_PATH, 'my_app.ini')

LOG_PATH = join(PROJECT_CONFIG_PATH, 'Log')


__all__ = ['CRYPTO_KEY', 'PROJECT_PATH', 'PROJECT_CONFIG_PATH', 'DB_FILE_PATH', 'PROJECT_INI_FILE', 'DB_FILE_NAME', 'LOG_PATH']