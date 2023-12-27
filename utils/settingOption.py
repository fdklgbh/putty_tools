# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: settingOption.py
import os
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication
from config import *
__all__ = ['SettingOption']


class SettingOption:
    def __init__(self):
        self.toolFolder = PROJECT_CONFIG_PATH
        self.__ini_path = PROJECT_INI_FILE
        self.__prefix_key = self.__class__.__name__
        os.makedirs(self.toolFolder, exist_ok=True)
        self.__desktop = QApplication.desktop()
        self.__deskName = f"{self.__prefix_key}_geometry_{self.__desktop.screenCount()}"
        self.__settings = QSettings(self.__ini_path, QSettings.IniFormat)

    def showSettingUi(self):
        if self.__settings.contains(self.__prefix_key + self.__deskName):
            self.setGeometry(self.getValue(self.__deskName))
        else:
            self.__center()

    def __center(self):
        # 计算窗口居中时的位置
        screen_geometry = self.__desktop.availableGeometry()
        window_geometry = self.frameGeometry()
        x = (screen_geometry.width() - window_geometry.width()) / 2
        y = (screen_geometry.height() - window_geometry.height()) / 2
        self.move(x, y)

    def saveSetting(self):
        # 保存配置
        self.setValue(self.__deskName, self.geometry())

    def setValue(self, key, value):
        self.__settings.setValue(self.__prefix_key + key, value)

    def getValue(self, key):
        return self.__settings.value(self.__prefix_key + key, defaultValue=None)
