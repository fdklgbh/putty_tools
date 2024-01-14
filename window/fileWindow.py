# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: fileWindow.py
from utils.cryptoData import *
from PyQt5.QtCore import QCoreApplication, Qt, QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from ui.config_file import Ui_widget
from utils.mySignal import publicSignal
from utils.settingOption import SettingOption
import re


class FileWindow(QWidget, Ui_widget, SettingOption):
    def __init__(self, show_msg):
        super().__init__()
        SettingOption.__init__(self)
        self.setGeometry(100, 100, 400, 300)
        self.setupUi(self)
        publicSignal.fileChangeSignal.connect(self.changeFile)
        self.showSettingUi()
        self.show_msg = show_msg
        portValidator = QIntValidator(self)
        regex = QRegExp(r'^((2[0-4]\d|25[0-5]|\d?\d|1\d{2})\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
        validator = QRegExpValidator(regex)
        self.host_edit.setValidator(validator)
        self.port_edit.setValidator(portValidator)
        self.setWindowModality(Qt.ApplicationModal)
        self.userName = ''
        self.host = ''
        self.port = ''
        self.fileName = ''
        self.passWord = ''

    def save_file(self, *args):
        self.fileName = self.filename_edit.text()
        self.host = self.host_edit.text()
        self.port = self.port_edit.text() or '22'
        self.userName = self.username_edit.text()
        self.passWord = self.pwd_edit.text()
        if any(_ == '' for _ in [self.fileName, self.host, self.userName, self.passWord]):
            self.show_alert('错误', '除端口外，数据中有未填项')
            return
        res = re.search(r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}", self.host)
        if res is None:
            self.show_alert('错误', '远程IP输入错误')
            return
        else:
            self.host = res.group()
        publicSignal.fileSaveDataSignal.emit([
            self.fileName,
            self.host,
            self.port,
            self.userName,
            encrypt(self.passWord),
            "creat" if self.windowTitle() == '新建' else "update"
        ])
        self.close()

    def check_port(self):
        if int(self.port_edit.text()) > 65535:
            self.port_edit.setText('65535')

    def show_alert(self, title, msg):
        QMessageBox.critical(self, title, msg)

    def closeEvent(self, event) -> None:
        self.saveSetting()
        super(FileWindow, self).closeEvent(event)

    def changeFile(self, oldData):
        self.fileName, self.host, self.port, self.userName, self.passWord = oldData
        self.show_msg('接收到的数据: ', oldData)
        # self.setWindowTitle(title)
        self.filename_edit.setText(self.fileName)
        self.host_edit.setText(self.host)
        self.port_edit.setText(self.port)
        self.username_edit.setText(self.userName)
        self.pwd_edit.setText(decrypt(self.passWord))

