# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.main_new.ui'
#
# Created: Tue Nov 29 23:26:30 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.7
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1062, 768)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.widgetMain = QtGui.QWidget(MainWindow)
        self.widgetMain.setObjectName("widgetMain")
        self.gridLayoutMain = QtGui.QGridLayout(self.widgetMain)
        self.gridLayoutMain.setObjectName("gridLayoutMain")
        self.tabAddress = QtGui.QTabWidget(self.widgetMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabAddress.sizePolicy().hasHeightForWidth())
        self.tabAddress.setSizePolicy(sizePolicy)
        self.tabAddress.setToolTip("")
        self.tabAddress.setDocumentMode(False)
        self.tabAddress.setTabsClosable(True)
        self.tabAddress.setMovable(True)
        self.tabAddress.setObjectName("tabAddress")
        self.gridLayoutMain.addWidget(self.tabAddress, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.widgetMain)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1062, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.dockDialpad = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockDialpad.sizePolicy().hasHeightForWidth())
        self.dockDialpad.setSizePolicy(sizePolicy)
        self.dockDialpad.setMinimumSize(QtCore.QSize(60, 38))
        self.dockDialpad.setFloating(True)
        self.dockDialpad.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockDialpad.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockDialpad.setObjectName("dockDialpad")
        self.dockDialpadContainer = QtGui.QWidget()
        self.dockDialpadContainer.setObjectName("dockDialpadContainer")
        self.gridLayoutDialpad = QtGui.QGridLayout(self.dockDialpadContainer)
        self.gridLayoutDialpad.setContentsMargins(0, 1, 0, 1)
        self.gridLayoutDialpad.setObjectName("gridLayoutDialpad")
        self.dockDialpad.setWidget(self.dockDialpadContainer)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockDialpad)
        self.dockHistory = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockHistory.sizePolicy().hasHeightForWidth())
        self.dockHistory.setSizePolicy(sizePolicy)
        self.dockHistory.setMinimumSize(QtCore.QSize(60, 38))
        self.dockHistory.setBaseSize(QtCore.QSize(0, 0))
        self.dockHistory.setFloating(False)
        self.dockHistory.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockHistory.setObjectName("dockHistory")
        self.dockHistoryContainer = QtGui.QWidget()
        self.dockHistoryContainer.setObjectName("dockHistoryContainer")
        self.gridLayoutHistory = QtGui.QGridLayout(self.dockHistoryContainer)
        self.gridLayoutHistory.setContentsMargins(0, 1, 0, 1)
        self.gridLayoutHistory.setObjectName("gridLayoutHistory")
        self.dockHistory.setWidget(self.dockHistoryContainer)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockHistory)

        self.retranslateUi(MainWindow)
        self.tabAddress.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DTRS", None, QtGui.QApplication.UnicodeUTF8))
        self.dockDialpad.setWindowTitle(QtGui.QApplication.translate("MainWindow", "다이얼패드", None, QtGui.QApplication.UnicodeUTF8))
        self.dockHistory.setWindowTitle(QtGui.QApplication.translate("MainWindow", "상세통화기록", None, QtGui.QApplication.UnicodeUTF8))

