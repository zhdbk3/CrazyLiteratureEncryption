# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_decrypt.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Decrypt(object):
    def setupUi(self, Decrypt):
        Decrypt.setObjectName("Decrypt")
        Decrypt.resize(800, 600)
        self.gridLayout_2 = QtWidgets.QGridLayout(Decrypt)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TitleLabel = TitleLabel(Decrypt)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout_2.addWidget(self.TitleLabel, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.primaryPushButton_decrypt = PrimaryPushButton(Decrypt)
        self.primaryPushButton_decrypt.setObjectName("primaryPushButton_decrypt")
        self.gridLayout.addWidget(self.primaryPushButton_decrypt, 0, 1, 1, 1)
        self.plainTextEdit_cipher = PlainTextEdit(Decrypt)
        self.plainTextEdit_cipher.setObjectName("plainTextEdit_cipher")
        self.gridLayout.addWidget(self.plainTextEdit_cipher, 0, 0, 2, 1)
        self.indeterminateProgressRing = IndeterminateProgressRing(Decrypt)
        self.indeterminateProgressRing.setObjectName("indeterminateProgressRing")
        self.gridLayout.addWidget(self.indeterminateProgressRing, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.tableWidget_results = TableWidget(Decrypt)
        self.tableWidget_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_results.setObjectName("tableWidget_results")
        self.tableWidget_results.setColumnCount(3)
        self.tableWidget_results.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_results.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_results.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_results.setHorizontalHeaderItem(2, item)
        self.gridLayout_2.addWidget(self.tableWidget_results, 2, 0, 1, 1)

        self.retranslateUi(Decrypt)
        QtCore.QMetaObject.connectSlotsByName(Decrypt)

    def retranslateUi(self, Decrypt):
        _translate = QtCore.QCoreApplication.translate
        Decrypt.setWindowTitle(_translate("Decrypt", "Form"))
        self.TitleLabel.setText(_translate("Decrypt", "解密"))
        self.primaryPushButton_decrypt.setText(_translate("Decrypt", "解密"))
        self.plainTextEdit_cipher.setPlaceholderText(_translate("Decrypt", "密文"))
        item = self.tableWidget_results.horizontalHeaderItem(0)
        item.setText(_translate("Decrypt", "可能的明文"))
        item = self.tableWidget_results.horizontalHeaderItem(1)
        item.setText(_translate("Decrypt", "信息密度/bit·词^(-1)"))
        item = self.tableWidget_results.horizontalHeaderItem(2)
        item.setText(_translate("Decrypt", "偏移量"))
from qfluentwidgets import IndeterminateProgressRing, PlainTextEdit, PrimaryPushButton, TableWidget, TitleLabel