# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_import.ui'
#
# Created: Sat Sep 24 12:10:34 2011
#      by: pyside-uic 0.2.10 running on PySide 1.0.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(346, 118)
        Dialog.setModal(True)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(25, 40, 316, 21))
        self.progressBar.setProperty("value", 25)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.buttonStart = QtGui.QPushButton(Dialog)
        self.buttonStart.setGeometry(QtCore.QRect(85, 75, 81, 31))
        self.buttonStart.setCheckable(False)
        self.buttonStart.setChecked(False)
        self.buttonStart.setObjectName("buttonStart")
        self.buttonCancel = QtGui.QPushButton(Dialog)
        self.buttonCancel.setGeometry(QtCore.QRect(180, 75, 81, 31))
        self.buttonCancel.setObjectName("buttonCancel")
        self.checkRemoveOldData = QtGui.QCheckBox(Dialog)
        self.checkRemoveOldData.setGeometry(QtCore.QRect(30, 15, 291, 16))
        self.checkRemoveOldData.setObjectName("checkRemoveOldData")
        self.labelMessage = QtGui.QLabel(Dialog)
        self.labelMessage.setGeometry(QtCore.QRect(30, 38, 271, 26))
        self.labelMessage.setObjectName("labelMessage")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonStart.setText(QtGui.QApplication.translate("Dialog", "시작", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("Dialog", "취소", None, QtGui.QApplication.UnicodeUTF8))
        self.checkRemoveOldData.setText(QtGui.QApplication.translate("Dialog", "기존 자료를 삭제합니다.", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMessage.setText(QtGui.QApplication.translate("Dialog", "자료를 입력 중입니다..", None, QtGui.QApplication.UnicodeUTF8))

