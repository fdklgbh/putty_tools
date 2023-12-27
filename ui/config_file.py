# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_file.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(234, 171)
        widget.setAcceptDrops(False)
        self.gridLayout = QtWidgets.QGridLayout(widget)
        self.gridLayout.setObjectName("gridLayout")
        self.filename_lab = QtWidgets.QLabel(widget)
        self.filename_lab.setObjectName("filename_lab")
        self.gridLayout.addWidget(self.filename_lab, 0, 0, 1, 1)
        self.filename_edit = QtWidgets.QLineEdit(widget)
        self.filename_edit.setObjectName("filename_edit")
        self.gridLayout.addWidget(self.filename_edit, 0, 1, 1, 2)
        self.host_lab = QtWidgets.QLabel(widget)
        self.host_lab.setObjectName("host_lab")
        self.gridLayout.addWidget(self.host_lab, 1, 0, 1, 1)
        self.host_edit = QtWidgets.QLineEdit(widget)
        self.host_edit.setInputMask("")
        self.host_edit.setObjectName("host_edit")
        self.gridLayout.addWidget(self.host_edit, 1, 1, 1, 2)
        self.port_lab = QtWidgets.QLabel(widget)
        self.port_lab.setObjectName("port_lab")
        self.gridLayout.addWidget(self.port_lab, 2, 0, 1, 1)
        self.port_edit = QtWidgets.QLineEdit(widget)
        self.port_edit.setMaxLength(5)
        self.port_edit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.port_edit.setObjectName("port_edit")
        self.gridLayout.addWidget(self.port_edit, 2, 1, 1, 2)
        self.username_lab = QtWidgets.QLabel(widget)
        self.username_lab.setObjectName("username_lab")
        self.gridLayout.addWidget(self.username_lab, 3, 0, 1, 1)
        self.username_edit = QtWidgets.QLineEdit(widget)
        self.username_edit.setObjectName("username_edit")
        self.gridLayout.addWidget(self.username_edit, 3, 1, 1, 2)
        self.pwd_lab = QtWidgets.QLabel(widget)
        self.pwd_lab.setObjectName("pwd_lab")
        self.gridLayout.addWidget(self.pwd_lab, 4, 0, 1, 1)
        self.pwd_edit = QtWidgets.QLineEdit(widget)
        self.pwd_edit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.pwd_edit.setObjectName("pwd_edit")
        self.gridLayout.addWidget(self.pwd_edit, 4, 1, 1, 2)
        self.save_btn = QtWidgets.QPushButton(widget)
        self.save_btn.setAutoRepeatDelay(200)
        self.save_btn.setObjectName("save_btn")
        self.gridLayout.addWidget(self.save_btn, 5, 1, 1, 1)
        self.cancel_btn = QtWidgets.QPushButton(widget)
        self.cancel_btn.setObjectName("cancel_btn")
        self.gridLayout.addWidget(self.cancel_btn, 5, 2, 1, 1)

        self.retranslateUi(widget)
        self.save_btn.clicked.connect(widget.save_file)
        self.cancel_btn.clicked.connect(widget.close)
        self.port_edit.editingFinished.connect(widget.check_port)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "新建"))
        self.filename_lab.setText(_translate("widget", "文件名称:"))
        self.filename_edit.setPlaceholderText(_translate("widget", "保存文件名称"))
        self.host_lab.setText(_translate("widget", "host:"))
        self.host_edit.setPlaceholderText(_translate("widget", "远程IP"))
        self.port_lab.setText(_translate("widget", "port:"))
        self.port_edit.setText(_translate("widget", "22"))
        self.port_edit.setPlaceholderText(_translate("widget", "远程端口号，默认22"))
        self.username_lab.setText(_translate("widget", "userName:"))
        self.username_edit.setPlaceholderText(_translate("widget", "远程用户名"))
        self.pwd_lab.setText(_translate("widget", "passWord:"))
        self.pwd_edit.setPlaceholderText(_translate("widget", "远程密码"))
        self.save_btn.setText(_translate("widget", "保存"))
        self.save_btn.setShortcut(_translate("widget", "Return"))
        self.cancel_btn.setText(_translate("widget", "取消"))
