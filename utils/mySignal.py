# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: mySignal.py
"""
    信号
"""
from PyQt5.QtCore import QObject, pyqtSignal


class MySignal(QObject):
    fileChangeSignal = pyqtSignal(list)
    fileCreatSignal = pyqtSignal(dict)
    fileSaveDataSignal = pyqtSignal(list)


publicSignal = MySignal()

__all__ = ['publicSignal']
