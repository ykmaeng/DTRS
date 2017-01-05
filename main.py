# coding=utf-8

'''
Created on 2011. 7. 8.

@author: Xeny
'''

import unittest
import sys, time, os, re
import main_ui
import ConfigParser
import MySQLdb as mysql
from sip_core import SipCore
from login import Login
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSql import *
from widget_dialpad import WidgetDialpad
from widget_history import WidgetHistory
from widget_main import WidgetMain


main = None
mainUi = None
sip = None
dbConn = None

class Main(QMainWindow):
    _rowsAddr = ()    
    sipId = ''
    
    signal_main_key_pressed = Signal(object)
    
    def __init__(self, sipId, sipPw):
        
        self.sipId = sipId
        
        # 한경설정 읽기
        ok = self.getConfig()
        if not ok: return
        
        # DB에 연결
        ok = self.connectToDB()
        if not ok: return
        
        # SIP 서비스 시작
        self.initSipCore(sipId, sipPw)

        # 메인윈도우 초기화
        ok = self.initMainWindow(None)
        if not ok: return
        
        
    @staticmethod
    def main(): global main; return main
    
    @staticmethod
    def mainUi(): global mainUi; return mainUi
    
    @staticmethod
    def sip(): global sip; return sip
    
    @staticmethod
    def dbConn(): global dbConn; return dbConn
    
    def getConfig(self):
        config = ConfigParser.RawConfigParser()
        config.read('.setting')
        
        # [INFO] Section
        self.infoClient = config.get('INFO', 'client').decode('cp949')
        self.infoVersion = config.get('INFO', 'version')
        
        # [DB] Section
        self.dbAddr = config.get('DB', 'addr')
        self.dbPort = config.getint('DB', 'port')
        self.dbUsername = config.get('DB', 'username')
        self.dbSecret = config.get('DB', 'secret')
        self.dbDatabase = config.get('DB', 'database')
        
        # [SIP] Section
        self.sipAddr = config.get('SIP', 'addr')
        
        return True
            
    def connectToDB(self):
        global dbConn
        dbConn = mysql.connect(host= self.dbAddr,
                             port = self.dbPort,
                             user = self.dbUsername,
                             passwd = self.dbSecret,
                             db = self.dbDatabase,
                             charset = 'utf8')          # 한글출력을 위해 필 사용 (그렇지 않으면 결과값에 대해 일일이 변환해줘야 함)
#                             use_unicode=True)

        return True
    
    def initMainWindow(self, parent):
        global mainUi
        print 'Main.__init__() called!'
        
        # 메인윈도우 생성
        super(Main, self).__init__(parent)
        mainUi = main_ui.Ui_MainWindow()
        mainUi.setupUi(self)
        
        # 타이틀바 이름 지정
        windowTitle = u'DTRS - %s 일반녹취 프로그램 V%s :: (주)인투바이 제공' % (self.infoClient, self.infoVersion)
        self.setWindowTitle(windowTitle)
    
        # 다이얼패드
        self.widgetDialpad = WidgetDialpad(self)
#        mainUi.gridLayoutDialpad.addWidget(self.widgetDialpad)
        mainUi.dockDialpad.setWidget(self.widgetDialpad)
        
        # 통화내역
        self.widgetHistory = WidgetHistory(self)
#        mainUi.gridLayoutHistory.addWidget(self.widgetHistory)
        mainUi.dockHistory.setWidget(self.widgetHistory)
        
        self.widgetMain = WidgetMain(self)
    
        # 프로그램 창 최대화
        self.showMaximized()
                
        return True
                
    def initSipCore(self, sipId, sipPw):
        global sip
        sip = SipCore()
        sip.initPjsua()
        self.sipId = sipId
        self.sipPw = sipPw
#        sip.regAccount(sipId, sipPw, self.sipAddr)
        return True
    
    def keyPressEvent(self, event):
        self.signal_main_key_pressed.emit(event)
        
    def closeEvent(self, event):
        print 'closeEvent() called!'
        sip.destroySip()
        
        
        
        
if __name__ == '__main__':
    app = QApplication('PJSUA')
#    app.setStyle('plastique')
    
    # 사용자 인증 및 기본정보 가져오기
    login = Login()
    ret = login.exec_()
    if ret == 0: 
        login.close()
        sys.exit(0)
    
    id = login.userId.encode('utf8')
    pw = login.userPw.encode('utf8')
    login.close()
        
    main = Main(id, pw)
    main.show()
    app.exec_()  

#    unittest.main()   
