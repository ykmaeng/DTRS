# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Mon Sep 19 01:03:23 2011
#      by: pyside-uic 0.2.10 running on PySide 1.0.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(287, 142)
        Login.setModal(True)
        self.buttonLogin = QtGui.QPushButton(Login)
        self.buttonLogin.setGeometry(QtCore.QRect(64, 100, 75, 23))
        self.buttonLogin.setDefault(True)
        self.buttonLogin.setObjectName("buttonLogin")
        self.buttonCancel = QtGui.QPushButton(Login)
        self.buttonCancel.setGeometry(QtCore.QRect(145, 100, 75, 23))
        self.buttonCancel.setObjectName("buttonCancel")
        self.layoutWidget = QtGui.QWidget(Login)
        self.layoutWidget.setGeometry(QtCore.QRect(35, 30, 214, 48))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.inputId = QtGui.QLineEdit(self.layoutWidget)
        self.inputId.setObjectName("inputId")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.inputId)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.inputPw = QtGui.QLineEdit(self.layoutWidget)
        self.inputPw.setInputMask("")
        self.inputPw.setEchoMode(QtGui.QLineEdit.Password)
        self.inputPw.setObjectName("inputPw")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.inputPw)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)
        Login.setTabOrder(self.inputId, self.inputPw)
        Login.setTabOrder(self.inputPw, self.buttonLogin)
        Login.setTabOrder(self.buttonLogin, self.buttonCancel)

    def retranslateUi(self, Login):
        Login.setWindowTitle(QtGui.QApplication.translate("Login", "DTRS - 로그인", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonLogin.setText(QtGui.QApplication.translate("Login", "로그인", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("Login", "취소", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Login", "아이디", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Login", "비밀번호", None, QtGui.QApplication.UnicodeUTF8))

