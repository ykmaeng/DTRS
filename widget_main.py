# -*- coding: utf-8 -*-

'''
Created on 2011. 9. 14.

@author: Xeny
'''

import os, re
from PySide.QtGui import *
from PySide.QtCore import *
from sip_core import SipCore
#from widget_addr import WidgetAddr
from widget_addr_r2 import WidgetAddr as WidgetAddrR2
from widget_dialpad import WidgetDialpad

main = None
mainUi = None
dbConn = None
sip = None

class WidgetMain:
    
    def __init__(self, parent):
#        super(WidgetMain, self).__init__()
        
        global main, mainUi, dbConn, sip, selfUi
        main = parent
        mainUi = main.mainUi()
        dbConn = main.dbConn()
        sip = main.sip()
        
#        mainUi.widgetMain.setVisible(False)
        
#        self.dialpad = WidgetDialpad(main)
#        mainUi.gridLayoutMain.addWidget(self.dialpad)
#        main.setCentralWidget(self.dialpad)

        self.initTabAddress()
        
    def initTabAddress(self):        
        ok = self.getAddrListFromDB()
        of = self.showAddrTab()
        
        mainUi.tabAddress.currentChanged.connect(self.on_tabAddress_currentChanged)
        mainUi.tabAddress.tabCloseRequested.connect(self.on_tabAddress_tabCloseRequested)
        
        if len(self._rowsAddr) == 0:
            self.createNewAddrTab()
            
    def createNewAddrTab(self):
        widgetAddr = WidgetAddrR2(main)
        
        index = mainUi.tabAddress.addTab(widgetAddr, u'새주소록')
        mainUi.tabAddress.setTabWhatsThis(index, 'addr')
        mainUi.tabAddress.setCurrentIndex(index)
        
        widgetAddr.signal_create_pressed.connect(self._on_widgetAddr_createPressed)
        widgetAddr.signal_import_finished.connect(self._on_widgetAddr_importFinished)
        
        widgetAddr.refreshTabIcon(index)
    
    def getAddrListFromDB(self):
        query = """
            select no, 0, addr_filename, public, column_count from addr_list
            where valid='1' and (public='1' or no_user_list=%s)
            """ % main.sipId
            
        cursor = dbConn.cursor()
        cursor.execute(query)
        
        self._rowsAddr = cursor.fetchall()
        print 'count of _rowsAddr:', len(self._rowsAddr)
        print self._rowsAddr
    
    def showAddrTab(self):
        for row in self._rowsAddr:
            title = unicode(os.path.splitext(row[2])[0])
            public = 1 if row[3] == '1' else 0 
            
            file_normal_on = 'group.png' if public else 'user.png'
            file_normal_off = 'group_gray.png' if public else 'user_gray.png'
            icon = QIcon()
            icon.addPixmap(QPixmap("./resources/images/%s" % file_normal_on), QIcon.Normal, QIcon.On)
            icon.addPixmap(QPixmap("./resources/images/%s" % file_normal_off), QIcon.Normal, QIcon.Off)
            
            addr = WidgetAddrR2(main, no=row[0], seq=row[1], title=title, public=public, numcols=row[4])
            index = mainUi.tabAddress.addTab(addr, icon, title)
#            self._dictAddrTab[unicode(row[0])] = tabAddr
            mainUi.tabAddress.setTabWhatsThis(index, 'addr')
            
            addr.signal_create_pressed.connect(self._on_widgetAddr_createPressed)
            addr.signal_import_finished.connect(self._on_widgetAddr_importFinished)
            
        currTabIndex = mainUi.tabAddress.currentIndex()
        print 'currTabIndex:', currTabIndex
        if currTabIndex >= 0:
            mainUi.tabAddress.currentWidget().showData(currTabIndex)

    @Slot()
    def _on_widgetAddr_createPressed(self):
        print '_on_widgetAddr_createPressed() called!'
        self.createNewAddrTab()
    
    @Slot(str)
    def _on_widgetAddr_importFinished(self, title):
        print '_on_widgetAddr_importFinished() called!'
        mainUi.tabAddress.setTabText(mainUi.tabAddress.currentIndex(), title)
        
    @Slot(int)
    def on_tabAddress_currentChanged(self, index):
        whatsThis = mainUi.tabAddress.tabWhatsThis(index)
        print 'on_tabAddress_currentChanged() called! => index:', index, 'type:', whatsThis  
        if whatsThis == 'addr':
            addr = mainUi.tabAddress.widget(index)
            addr.showData(index)
    
    @Slot(int)
    def on_tabAddress_tabCloseRequested(self, index):
        if mainUi.tabAddress.tabWhatsThis(index) != 'addr': return
            
        msgBox = QMessageBox(QMessageBox.Question, u'주소록 삭제', u'')
        buttonYes = msgBox.addButton(u'예', QMessageBox.YesRole)
        msgBox.addButton(u'아니오', QMessageBox.NoRole)
        msgBox.setText(u'주소록을 삭제하시겠습니까?')
            
        msgBox.exec_()        
        if msgBox.clickedButton() == buttonYes:
            mainUi.tabAddress.widget(index).disableCurrentAddr()
            mainUi.tabAddress.removeTab(index)
            
            if mainUi.tabAddress.count() == 0:
                self.createNewAddrTab()
    
  
