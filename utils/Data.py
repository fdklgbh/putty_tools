# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: Data.py
class Data:
    def __init__(self):
        self._data = {
            'type': '',
            'id': 0,
            'parentId': 0
        }

    def _setType(self, typeData: str):
        self._data['type'] = typeData

    def setId(self, idNumber: int):
        self._data['id'] = idNumber

    def getData(self):
        return self._data

    def _addKey(self, key, value):
        self._data[key] = str(value)


class FolderData(Data):
    def __init__(self):
        super(FolderData, self).__init__()
        self._setType('folder')

    def setParentId(self, parentId: int):
        self._data['parentId'] = parentId


class FileData(Data):
    def __init__(self):
        super(FileData, self).__init__()
        self._setType('file')

    def setFolderId(self, folderId):
        self._addKey("folderId", folderId)

    def setFileName(self, fileName):
        self._addKey('fileName', fileName)

    def setHost(self, host):
        self._addKey('host', host)

    def setPort(self, port):
        self._addKey('port', port)

    def setPwd(self, pwd):
        self._addKey('pwd', pwd)

    def setUserName(self, userName):
        self._addKey('userName', userName)
