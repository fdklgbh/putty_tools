# -*- coding: utf-8 -*-
# @Author  : fdklgbh
# @FileName: SqlOption.py
import sys

from os.path import exists
from typing import Union

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from config import *
from os import remove
import sqlite3


class Sqlite:
    def __init__(self):
        self.__fileExist = False
        if exists(DB_FILE_PATH):
            self.__fileExist = True
        self.db = sqlite3.connect(DB_FILE_PATH)
        self.cur = self.db.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS folderTable ("
                         "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "folderName TEXT, parentFolderId INTEGER DEFAULT 0);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS fileTable ("
                         "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "folderId INTEGER, "
                         "fileName TEXT, "
                         "ipAddress TEXT, "
                         "port INTEGER, "
                         "userName TEXT, "
                         "password TEXT)")

    def execute(self, sql, args):
        self.cur.execute(sql, args)
        self.db.commit()

    def insert(self, type_, table, *args):
        if type_ == 'folder':
            data = "folderName, parentFolderId"
            values = "?, ?"
        else:
            data = "folderId, fileName, ipAddress, port, userName, password"
            values = "?, ?, ?, ?, ?, ?"
        self.execute(f'insert into {table} ({data}) values ({values})', args)
        return self.cur.lastrowid

    def select(self, sql):
        self.cur.execute(sql)
        while True:
            data = self.cur.fetchone()
            if data:
                yield data
            else:
                break

    def selectAll(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def update(self, type_, table, *args):
        if type_ == 'folder':
            setData = "folderName = ?"
        else:
            setData = "fileName = ?, ipAddress = ?, port = ?, userName = ?, password = ?"
        self.execute(f"UPDATE {table} SET {setData} WHERE id = ?;", args)

    def delete(self, table, tableId):
        self.execute(f'delete from {table} where id = ?', [tableId])

    def close(self):
        if self.cur:
            self.cur.close()
        if self.db:
            self.db.close()


# class Sqlite:
#     @staticmethod
#     def selectQueryData(sql) -> iter:
#         query = QSqlQuery()
#         query.exec(sql)
#         while query.next():
#             record = query.record()
#             temp = []
#             for i in range(record.count()):
#                 data = record.value(i)
#                 if data == '':
#                     break
#                 else:
#                     temp.append(data)
#             yield temp
#         query.clear()
#         query.finish()
#
#     @staticmethod
#     def upData(type_, table, *args):
#         query = QSqlQuery()
#         sql_start = f"UPDATE {table} "
#         if type_ == 'folder':
#             query.prepare(f"{sql_start}SET folderName = :folderName where folderId = :folderId")
#             query.bindValue(":folderName", args[0])
#             query.bindValue(':folderId', args[1])
#         elif type_ == 'file':
#             query.prepare(f'{sql_start}SET fileName = :fileName, ipAddress = :ipAddress, '
#                           f'port=:port, userName = :userName, password = :password where fileId = :fileId')
#             query.bindValue(":fileName", args[0])
#             query.bindValue(":ipAddress", args[1])
#             query.bindValue(":port", args[2])
#             query.bindValue(":userName", args[3])
#             query.bindValue(":password", args[4])
#             query.bindValue(":fileId", args[5])
#
#         query.exec()
#         query.clear()
#         query.finish()
#
#     def closeDb(self):
#         self.db.close()


if __name__ == '__main__':
    sql = Sqlite()
    data = sql.select("SELECT * FROM folderTable", True)
    print(data)
