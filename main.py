# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: main.py
import time
from os.path import abspath, join
import sys
from config import PROJECT_PATH, LOG_PATH
from window.mainWindow import PuttyToolsWindow
import traceback

sys.path.append(abspath(PROJECT_PATH))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
import qdarkstyle


def custom_exception_handler(type_, value, trace: traceback):
    traceback_format = traceback.format_exception(type_, value, trace)
    error_msg = "".join(traceback_format)
    file_name = f'error_{int(time.time())}.log'
    QMessageBox.critical(None, "错误", str(error_msg) + f'日志文件保存在Log文件夹下\n文件名：{file_name}')
    with open(join(LOG_PATH, file_name), 'w', encoding='utf8') as f:
        f.write(error_msg)
    sys.exit(-1)


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication([])
    sys.excepthook = custom_exception_handler

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main_window = PuttyToolsWindow()
    main_window.show()
    app.exec_()
