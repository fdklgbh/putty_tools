# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: eventFilter.py
from PyQt5.QtCore import QObject, QEvent


class MyEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverMove:
            print("捕获到鼠标点击事件")
            return True  # 返回 True 表示已经处理该事件
        return super().eventFilter(obj, event)
