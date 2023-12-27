# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: mainWindow.py
from os.path import abspath
from PyQt5.QtCore import Qt, QModelIndex, QObject, QEvent
import subprocess
from utils.LogModule import ShowLog
from utils.cryptoData import decrypt
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QMenu, QInputDialog, QLineEdit
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
from utils.SqlOption import Sqlite
from ui.main_ui import Ui_PuttyTools
from utils.Data import FolderData, FileData
from utils.mySignal import publicSignal
from utils.settingOption import SettingOption
from window.fileWindow import FileWindow
from threading import Thread


class MyFilter(QObject):
    def eventFilter(self, obj, event):
        event_type = event.type()
        try:
            text = obj.text()
        except AttributeError:
            text = ''
        if text:
            if event_type == QEvent.Leave:
                # 鼠标移出时取消焦点
                obj.clearFocus()
            elif event_type == QEvent.Enter:
                # 鼠标进入时,获取焦点
                obj.setFocus()
        return False


class PuttyThread(Thread):
    def __init__(self, host, port, username, pwd, puttyPath, show_msg):
        super(PuttyThread, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.puttyPath = puttyPath
        self.show_msg = show_msg

    def run(self) -> None:
        cmd = f"{self.puttyPath} -load PuttyTools -ssh {self.username}@{self.host} -P {self.port} -pw {self.pwd} -X"
        self.show_msg('执行命令 ===> ', cmd)
        subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class PuttyToolsWindow(QMainWindow, Ui_PuttyTools, SettingOption):
    def __init__(self):
        super().__init__()
        SettingOption.__init__(self)
        self.setupUi(self)
        self.showSettingUi()
        self.log = ShowLog()
        self.log.trigger.connect(self.update_msg)
        # self.treeView.setStyleSheet(style_sheet)
        self.model = QStandardItemModel()
        self.sqlite = Sqlite()
        self.folderPic = QIcon(":/icon/wenjianjia.svg")
        self.filePic = QIcon(":/icon/wenjian.svg")
        self.folderTable = 'folderTable'
        self.fileTable = 'fileTable'
        self.folderData = FolderData()
        self.fileData = FileData()
        self.root_item = self.model.invisibleRootItem()
        self.userRole = Qt.UserRole + 1
        self.node = None
        self.putty = abspath('./Putty/putty.exe')
        self.setup_ui()
        event_filter = MyFilter(self)
        self.pwd_edit.installEventFilter(event_filter)
        self.username_edit.installEventFilter(event_filter)
        self.port_edit.installEventFilter(event_filter)
        self.host_edit.installEventFilter(event_filter)

    def setup_ui(self):
        self.buildTree()
        self.connect_signals()
        self.treeView.setModel(self.model)
        self.treeView.expandAll()
        self.treeView.header().setSectionResizeMode(0)
        self.treeView.header().setHidden(True)

    def connect_signals(self):
        publicSignal.fileSaveDataSignal.connect(self.saveFileData)
        self.treeView.doubleClicked.connect(self.on_item_double_clicked)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def on_item_double_clicked(self, index):
        item = self.model.itemFromIndex(index)
        parent_text = item.data(Qt.UserRole + 1)
        self.show_msg("节点信息：", parent_text)
        if parent_text['type'] == 'file':
            putty = PuttyThread(parent_text["host"], parent_text["port"], parent_text["userName"],
                                decrypt(parent_text["pwd"]), self.putty, self.show_msg)
            putty.start()
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def saveFileData(self, data):
        nodeMsg, item = self.node
        self.show_msg('收到的数据', data)
        self.show_msg('原始数据', nodeMsg)
        self.fileData.setFileName(data[0])
        self.fileData.setHost(data[1])
        self.fileData.setPort(data[2])
        self.fileData.setUserName(data[3])
        self.fileData.setPwd(data[4])
        childFileItem = QStandardItem(data[0])
        if nodeMsg:
            # 有选项
            if data[-1] == 'creat':
                if nodeMsg['type'] == 'file':
                    folderId = nodeMsg['folderId']
                    item = item.parent()
                else:
                    folderId = nodeMsg['id']
                self.fileData.setFolderId(folderId)
                childFileId = self.sqlite.insert('file', self.fileTable, folderId, *data[:-1])
                self.fileData.setId(childFileId)
                childFileItem.setIcon(self.filePic)
                childFileItem.setData(self.fileData.getData(), self.userRole)
                item.appendRow(childFileItem)
            else:
                self.fileData.setId(nodeMsg['id'])
                self.fileData.setFolderId(nodeMsg['folderId'])
                self.sqlite.update('file', self.fileTable, *data[:-1], nodeMsg['id'])
                item.setData(self.fileData.getData(), self.userRole)
                item.setText(data[0])
                self.host_edit.setText(data[1])
                self.username_edit.setText(data[3])
                self.port_edit.setText(str(data[2]))
                self.pwd_edit.setText(decrypt(data[4]))
        else:
            # 空白部分 创建
            self.fileData.setFolderId(0)
            rootFileId = self.sqlite.insert('file', self.fileTable, 0, *data[:-1])
            self.fileData.setId(rootFileId)
            childFileItem.setIcon(self.filePic)
            childFileItem.setData(self.fileData.getData(), self.userRole)
            self.root_item.appendRow(childFileItem)

    def closeEvent(self, event) -> None:
        self.sqlite.close()
        self.saveSetting()
        self.log.close_log_file()
        super(PuttyToolsWindow, self).closeEvent(event)

    def getNodeMsg(self, pos) -> [dict, QStandardItem]:
        index = self.treeView.indexAt(pos)  # 获取右键点击的单元格的索引
        item = self.model.itemFromIndex(index)
        if item:
            parent_text = item.data(self.userRole)
            return parent_text, item
        else:
            return None, None

    def showMenu(self, pos):
        temp = self.getNodeMsg(pos)
        nodeMsg: dict = temp[0]
        item: QStandardItem = temp[1]
        self.node = nodeMsg, item
        menu = QMenu(self.treeView)

        if not nodeMsg:
            menu.addAction(self.actionAddFile)
            menu.addAction(self.actionAddFolder)
            self.actionAddFile.triggered.connect(self.addFile)
            self.show_msg(f'当前节点信息 =====> {nodeMsg}')
            # self.actionAddFolder.triggered.connect(partialmethod(self.addFolder, item=item, nodeMsg=nodeMsg))
            self.actionAddFolder.triggered.connect(self.addFolder)
        else:
            if nodeMsg['type'] == 'file':
                menu.addAction(self.actionRenameFile)
                menu.addAction(self.actionAddFile)
                menu.addAction(self.actionDelFile)
                self.actionAddFile.triggered.connect(self.addFile)
                self.actionDelFile.triggered.connect(self.delFile)
                self.actionRenameFile.triggered.connect(self.renameFile)
            else:
                menu.addAction(self.actionAddFile)
                menu.addAction(self.actionAddFolder)
                menu.addAction(self.actionDelFolder)
                menu.addAction(self.actionRenameFolder)
                self.actionAddFile.triggered.connect(self.addFile)
                self.actionAddFolder.triggered.connect(self.addFolder)
                self.actionDelFolder.triggered.connect(self.delFolder)
                self.actionRenameFolder.triggered.connect(self.renameFolder)

        menu.popup(self.treeView.viewport().mapToGlobal(pos))

    def getUserRole(self, item):
        if item:
            return item.data(self.userRole)
        else:
            return None

    def getItem(self) -> QStandardItem:
        """
        获取当前选中的
        :return:
        """
        index = self.treeView.currentIndex()
        return self.model.itemFromIndex(index)

    def addFile(self):
        nodeMsg, item = self.node
        index = self.treeView.currentIndex()
        item = self.model.itemFromIndex(index)
        self.show_msg(f'addFile = ====,{self.getUserRole(item)}')
        self.show_msg(nodeMsg)
        self.showFileWindow()
        self.actionAddFile.triggered.disconnect()

    def searchType(self, item: QStandardItem, target='folder'):
        def getData(index):
            temp = item.child(index)
            return item.child(index).data(Qt.UserRole + 1)

        low = 0
        # 数量转为下标
        item_sum = item.rowCount()
        high = item_sum - 1
        self.show_msg(f'当前层级数据总数 ===> {item_sum}')
        # self.show_msg('开始遍历数据:')
        # for i in range(item_sum):
        #     self.show_msg(f'下标{i} 文件/文件夹数据 ===> {getData(i)}')
        #     self.show_msg(f'名称 ===> {item.child(i).text()}')
        while low <= high:
            mid = (low + high) // 2
            self.show_msg(f'二分查找中间数 ==> {mid}')
            midData = getData(mid)
            if midData['type'] == target:
                if mid == 0 and high != 1:
                    return 0
                if getData(mid + 1)['type'] == target:
                    if mid + 1 == high:
                        return mid + 1
                    low = mid
                else:
                    return mid
            else:
                if mid == 0:
                    return None
                if getData(mid - 1)['type'] == target:
                    return mid - 1
                if mid == 0 and midData['type'] != target:
                    return None
                high = mid
        return None

    def addFolder(self):
        nodeMsg, item = self.node
        # if nodeMsg:
        try:
            self.show_msg(f'文件夹名称:{item.text()}')
        except AttributeError as e:
            if str(e) != "'NoneType' object has no attribute 'text'":
                self.show_msg(f'-----error: {e}')
        child_name, ok = QInputDialog.getText(self.treeView, "新建文件夹", "文件夹名称:")
        child_item = QStandardItem(child_name)
        if ok and child_name:
            self.show_msg('新建的文件夹名称:', child_name)
            if nodeMsg is None or item is None:
                lastFolderIndex = self.searchType(self.root_item)
                self.folderData.setParentId(0)
                addId = self.sqlite.insert('folder', self.folderTable, child_name, 0)
                self.folderData.setId(addId)
                child_item.setIcon(self.folderPic)
                child_item.setData(self.folderData.getData(), self.userRole)
                if lastFolderIndex is None:
                    index = 0
                else:
                    index = lastFolderIndex + 1
                self.root_item.insertRow(index, child_item)
            else:
                self.folderData.setParentId(nodeMsg['id'])
                addId = self.sqlite.insert('folder', self.folderTable, child_name, nodeMsg['id'])
                self.folderData.setId(addId)
                lastFolderIndex = self.searchType(item)
                if lastFolderIndex is None:
                    index = 0
                else:
                    index = lastFolderIndex + 1
                child_item.setIcon(self.folderPic)
                child_item.setData(self.folderData.getData(), self.userRole)
                item.insertRow(index, child_item)
            self.show_msg(f'最后一个文件夹下标: {lastFolderIndex}')

        self.actionAddFolder.triggered.disconnect()

    def renameFolder(self):
        nodeMsg, item = self.node
        if item:
            self.show_msg(f'文件夹信息:{nodeMsg}')
            data = item.data(self.userRole)
            if data['type'] == 'folder':
                oldName = item.text()
                newName, ok = QInputDialog.getText(self.treeView, '修改文件夹名称', '输入新的名称：', text=oldName)
                if ok and newName:
                    self.sqlite.update('folder', self.folderTable, newName, data['id'])
                    item.setText(newName)
                    self.show_msg(f'修改前文件夹名称:{oldName}, 修改后:{newName}')
        self.actionRenameFolder.disconnect()

    def renameFile(self):
        nodeMsg, item = self.node
        self.show_msg('文件信息 ===>', self.getUserRole(item))
        if item:
            data = item.data(self.userRole)
            self.showFileWindow(True)
            if data['type'] == 'file':
                publicSignal.fileChangeSignal.emit(
                    [data['fileName'],
                     data['host'],
                     data['port'],
                     data['userName'],
                     data['pwd']]
                )
        self.actionRenameFile.disconnect()

    def showFileWindow(self, change=False):
        self.fileWindow = FileWindow(self.show_msg)
        if change:
            self.fileWindow.setWindowTitle('修改文件')
        self.fileWindow.show()

    def delFolder(self):
        nodeMsg, item = self.node

        def delId(id_):
            self.sqlite.delete(self.folderTable, id_)
            dataList = self.sqlite.selectAll(f"SELECT * FROM {self.folderTable} WHERE parentFolderId = {id_}")
            for data in self.sqlite.select(f"SELECT * FROM {self.fileTable} WHERE folderId = {id_}"):
                self.show_msg(f'将要删除的子文件信息: {data}')
                self.sqlite.delete(self.fileTable, data[0])
            for i in dataList:
                self.show_msg(f'将要删除的子文件夹信息: {i}')
                delId(i[0])

        if nodeMsg and item:
            self.show_msg(f'选择的文件夹: {item.text()}')
            self.show_msg(f'选择文件夹信息: {nodeMsg}')
            delId(nodeMsg['id'])
            self.delItem(item)

        self.actionDelFolder.disconnect()

    def delFile(self):
        nodeMsg, item = self.node
        if nodeMsg and item:
            self.sqlite.delete(self.fileTable, nodeMsg['id'])
            self.delItem(item)
            self.clearText()
        self.actionDelFile.disconnect()

    def delItem(self, item: QModelIndex):
        self.model.removeRow(item.row(), self.model.indexFromItem(item.parent()))

    def treeOneClick(self, index: QModelIndex):
        msg = index.data(self.userRole)
        if msg['type'] == 'file':
            self.host_edit.setText(msg['host'])
            self.username_edit.setText(msg['userName'])
            self.port_edit.setText(str(msg['port']))
            self.pwd_edit.setText(decrypt(msg['pwd']))
        else:
            self.clearText()

    def clearText(self):
        self.host_edit.clear()
        self.port_edit.clear()
        self.username_edit.clear()
        self.pwd_edit.clear()

    def buildTree(self):
        def buildTreeRecursive(parent_node, folderData):
            item = QStandardItem(folderData[1])
            item.setData(folderData[0])
            self.folderData.setId(folderData[0])
            self.folderData.setParentId(folderData[2])
            item.setIcon(self.folderPic)
            item.setData(self.folderData.getData(), self.userRole)
            parent_node.appendRow(item)

            folderSql = f"SELECT * from {self.folderTable} where parentFolderId={folderData[0]}"
            # 次级目录
            for queryFolderData in self.sqlite.selectAll(folderSql):
                buildTreeRecursive(item, queryFolderData)
            fileSql = f"select * from {self.fileTable} where folderId={folderData[0]}"
            for queryFileData in self.sqlite.select(fileSql):
                self.addFileData(queryFileData)
                fileItem = QStandardItem(f'{queryFileData[2]}')
                fileItem.setData(queryFileData[0])
                fileItem.setIcon(self.filePic)
                fileItem.setData(self.fileData.getData(), self.userRole)
                item.appendRow(fileItem)

        sql = f'select * from {self.folderTable} where parentFolderId = 0'
        for data in self.sqlite.selectAll(sql):
            buildTreeRecursive(self.root_item, data)
        sql = f'select * from {self.fileTable} where folderId = 0'
        for data in self.sqlite.select(sql):
            self.addFileData(data)
            fileItem = QStandardItem(f'{data[2]}')
            fileItem.setIcon(self.filePic)
            fileItem.setData(data[0])
            fileItem.setData(self.fileData.getData(), self.userRole)
            self.root_item.appendRow(fileItem)

    def addFileData(self, data):
        self.fileData.setId(data[0])
        self.fileData.setFolderId(data[1])
        self.fileData.setFileName(data[2])
        self.fileData.setHost(data[3])
        self.fileData.setPort(data[4])
        self.fileData.setUserName(data[5])
        self.fileData.setPwd(data[6])

    def selected_text(self):
        edit = QObject().sender()
        selected_data = edit.selectedText()
        if selected_data:
            self.show_msg('选中的数据 ===>', selected_data)

    def show_msg(self, *args, save_log=True):
        text = ''
        if args:
            for i in args:
                text += f' {str(i)}'
        else:
            return
        self.log.show_msg(text)
        if save_log:
            self.log.write(text)

    def update_msg(self, text):
        self.showMsg.append(text)


# 去掉treeView 的线
style_sheet = """
               QTreeView::branch:has-siblings:!adjoins-item {
                   border-image: none;
               }
               QTreeView::branch:has-siblings:adjoins-item {
                   border-image: none;
               }
               QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                   border-image: none;
               }
               QTreeView::branch:has-children:!has-siblings:closed,
               QTreeView::branch:closed:has-children:has-siblings {
                   image: none;
                   border-image: none;
                   color: red;
               }
               QTreeView::branch:open:has-children:!has-siblings,
               QTreeView::branch:open:has-children:has-siblings {
                   image: none;
                   border-image: none;
               }
           """
