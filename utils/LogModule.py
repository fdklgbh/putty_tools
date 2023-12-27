# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: LogModule.py
from os.path import join

from PyQt5.QtCore import *
import time

from typing import TextIO
from os import makedirs
from config import LOG_PATH


class ShowLog(QThread):
    # 设置线程变量
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.today = self._get_today
        makedirs(LOG_PATH, exist_ok=True)
        self._f: TextIO = self._open_log_file()

    def show_msg(self, message):
        """
        向信号trigger发送消息
        """
        self.trigger.emit(message)

    def _open_log_file(self, today=None):
        if today is None:
            today = self.today

        return open(join(LOG_PATH, f'{today}.txt'), 'a', encoding='utf8')

    @property
    def _get_today(self):
        return time.strftime("%F")

    def write(self, msg):
        today = self._get_today
        if today != self.today:
            self._f.close()
            self._f = self._open_log_file(today)
        self._f.write(f'[{time.strftime("%F %T")}] {msg}\n')

    def close_log_file(self):
        self._f.close()
    

__all__ = ['ShowLog']
