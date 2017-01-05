# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.widget_history.ui'
#
# Created: Thu Nov 10 17:46:26 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.7
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(753, 660)
        self.gridLayout = QtGui.QGridLayout(Widget)
        self.gridLayout.setObjectName("gridLayout")
        self.tableHistory = QtGui.QTableWidget(Widget)
        self.tableHistory.setColumnCount(0)
        self.tableHistory.setObjectName("tableHistory")
        self.tableHistory.setColumnCount(0)
        self.tableHistory.setRowCount(0)
        self.gridLayout.addWidget(self.tableHistory, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textSearch = QtGui.QLineEdit(Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textSearch.sizePolicy().hasHeightForWidth())
        self.textSearch.setSizePolicy(sizePolicy)
        self.textSearch.setObjectName("textSearch")
        self.horizontalLayout_2.addWidget(self.textSearch)
        self.buttonSearch = QtGui.QPushButton(Widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSearch.sizePolicy().hasHeightForWidth())
        self.buttonSearch.setSizePolicy(sizePolicy)
        self.buttonSearch.setMinimumSize(QtCore.QSize(0, 0))
        self.buttonSearch.setMaximumSize(QtCore.QSize(60, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/images/magnifier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonSearch.setIcon(icon)
        self.buttonSearch.setObjectName("buttonSearch")
        self.horizontalLayout_2.addWidget(self.buttonSearch)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.checkAllHistory = QtGui.QCheckBox(Widget)
        self.checkAllHistory.setObjectName("checkAllHistory")
        self.horizontalLayout_2.addWidget(self.checkAllHistory)
        self.buttonRefresh = QtGui.QPushButton(Widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/images/arrow_refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonRefresh.setIcon(icon1)
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.horizontalLayout_2.addWidget(self.buttonRefresh)
        self.buttonPlay = QtGui.QPushButton(Widget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/images/resultset_next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonPlay.setIcon(icon2)
        self.buttonPlay.setObjectName("buttonPlay")
        self.horizontalLayout_2.addWidget(self.buttonPlay)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 1)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QtGui.QApplication.translate("Widget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHistory.setToolTip(QtGui.QApplication.translate("Widget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">모든 전화 기록이 남겨집니다.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">번호를 더블클릭 하면 통화내용을 들을 수 있습니다. ^^</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tableHistory.setSortingEnabled(True)
        self.buttonSearch.setText(QtGui.QApplication.translate("Widget", "찾기", None, QtGui.QApplication.UnicodeUTF8))
        self.checkAllHistory.setText(QtGui.QApplication.translate("Widget", "전체통화기록", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRefresh.setText(QtGui.QApplication.translate("Widget", "새로고침", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonPlay.setText(QtGui.QApplication.translate("Widget", "음성듣기", None, QtGui.QApplication.UnicodeUTF8))

