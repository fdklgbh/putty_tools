# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: main.py

from os.path import abspath
import sys
from config import PROJECT_PATH
from window.mainWindow import PuttyToolsWindow

sys.path.append(abspath(PROJECT_PATH))
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication
import qdarkstyle

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    main_window = PuttyToolsWindow()
    main_window.show()
    app.exec_()
