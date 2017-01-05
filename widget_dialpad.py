# -*- coding: utf-8 -*-

'''
Created on 2011. 9. 14.

@author: Xeny
'''

from PySide.QtGui import *
from PySide.QtCore import *
from sip_core import SipCore
import widget_dialpad_ui
import os, re

main = None
mainUi = None
selfUi = None
dbConn = None
sip = None

class WidgetDialpad(QWidget):
    
    _clearLabelNumber = False
    _incomingCall = False
    _msgBoxIncomingCall = None
    _soundRing = QSound("./resources/sounds/phone-ring.wav")
    _registered = False
    
    def __init__(self, parent):
        super(WidgetDialpad, self).__init__()
        
        global main, mainUi, dbConn, sip, selfUi
        main = parent
        mainUi = main.mainUi()
        dbConn = main.dbConn()
        sip = main.sip()
        
        sip.signal_reg_succeed[object].connect(self._on_sip_reg_succeed)
        sip.signal_reg_failed[object].connect(self._on_sip_reg_failed)
        sip.signal_call_incoming[object].connect(self._on_sip_call_incoming)
        sip.signal_call_connected[object].connect(self._on_sip_call_connected)
        sip.signal_call_disconnected[object].connect(self._on_sip_call_disconnected)
        sip.signal_rec_started[object].connect(self._on_sip_rec_started)
        sip.signal_rec_stoped[object].connect(self._on_sip_rec_stoped)

        selfUi = widget_dialpad_ui.Ui_Widget()
        selfUi.setupUi(self)

        # 라벨 초기화
        selfUi.labelStatus.clear()        
        selfUi.labelNumber.setText(main.sipId)
        self._clearLabelNumber = True
        
        # SIP Registration
        sip.regAccount(main.sipId, main.sipPw, main.sipAddr)
        
        
        
    @staticmethod
    def ui(): global selfUi; return selfUi
    
    @Slot(object)
    def _on_sip_reg_succeed(self, account):
        print '_on_sip_reg_succeed() called!'
        selfUi.labelStatus.setText(u'"%s" 전화가 등록되었습니다.' % main.sipId)
        self._registered = True
        
    @Slot(object)
    def _on_sip_reg_failed(self, account):
        print '_on_sip_reg_failed() called!'
        selfUi.labelStatus.setText(u'전화가 등록되지 않았습니다.')
        self._registered = False
        
        msgBox = QMessageBox(QMessageBox.Information, u'알림', u'')
        msgBox.setText(u'전화가 등록되지 않았습니다.')
        msgBox.setInformativeText(u'등록 후 사용해주세요.')
        msgBox.addButton(u'확인', QMessageBox.YesRole)
        msgBox.exec_()
        
    @Slot(object)
    def _on_sip_call_incoming(self, call):
        print '_on_sip_call_incoming() called'
        selfUi.labelStatus.setText(u'전화가 걸려왔습니다.')

        remote_uri = sip.current_call.info().remote_uri
        print 'current_call.remote_uri:', remote_uri
        
        print 'current_call.state:' \
        , sip.current_call.info().state_text \
        , str(sip.current_call.info().state)

        rx = QRegExp('(".*") <sip:(.*)@(.*)>')
        rx.indexIn(remote_uri)
        remote_name = rx.cap(1)
        remote_cid = rx.cap(2)
        
        self.__current_callee_num = main.sipId

        self._incomingCall = True
        self.appendToLabelNumber(remote_cid, True)
        self.showMaximized()
        self.playRing()
        self.alertIncomingCall(remote_name, remote_cid)
#        self._clearLabelNumber = True
        
    @Slot(object)
    def _on_sip_call_connected(self, call):
        print '_on_sip_call_connected() called'
        selfUi.labelStatus.setText(u'전화가 연결되었습니다.')
        self._incomingCall = False
        
    @Slot(object)
    def _on_sip_call_disconnected(self, call):
        print '_on_sip_call_disconnected() called'
        if self._incomingCall:
            self.closeMsgBoxIncomingCall()
            self._incomingCall = False
            
        self.stopRing()
        main.widgetDialpad.ui().labelStatus.setText(u'전화가 끊어졌습니다.')
        main.widgetHistory.refreshTableHistory()
        
    @Slot(object)
    def _on_sip_rec_started(self, call):
        print '_on_sip_rec_started() called'
        selfUi.labelStatus.setText(u'녹음을 시작합니다.')
#        self._clearLabelNumber = True
        
    @Slot(object)
    def _on_sip_rec_stoped(self, call):
        print '_on_sip_rec_stoped() called'
        selfUi.labelStatus.setText(u'녹음이 종료되었습니다.')
#        self._clearLabelNumber = True
    
    
    @Slot()
    def on_buttonDial_clicked(self):
        print 'on_buttonDial_clicked() called!'
        
        if self._incomingCall:
            self.stopRing()
            sip.answerCall()
            return
            
        # 전화가 등록되어 있지 않으면 경고 띄움
        if not self._registered:
            msgBox = QMessageBox(QMessageBox.Information, u'알림', u'')
            msgBox.setText(u'전화를 걸 수 없습니다.')
            msgBox.setInformativeText(u'등록 후 사용해주세요.')
            msgBox.addButton(u'확인', QMessageBox.YesRole)
            msgBox.exec_()
            return
        
        # 전화번호 패턴을 검사한다.
        labelText = selfUi.labelNumber.text()
        if re.match('^0[1-9][0-9]{7,}', labelText) == None:
            return
        
        self.__current_callee_num = labelText
        
        selfUi.labelStatus.setText(u'전화를 걸고 있습니다.')
        sip.makeCall(sip.current_acc, 'sip:{}@{}'.format(labelText, main.dbAddr))
    
    @Slot()
    def on_buttonHangup_clicked(self):
        print 'on_buttonHangup_clicked() called!'
        self.stopRing()
        sip.hangupAllCall()
        selfUi.labelNumber.clear()
    
            
    @Slot()
    def on_dtmf1_clicked(self):
        print 'on_dtmf1_clicked() called!'
        self.handleDtmf('1')
        
    @Slot()
    def on_dtmf2_clicked(self):
        print 'on_dtmf2_clicked() called!'
        self.handleDtmf('2')
        
    @Slot()
    def on_dtmf3_clicked(self):
        print 'on_dtmf3_clicked() called!'
        self.handleDtmf('3')

    @Slot()
    def on_dtmf4_clicked(self):
        print 'on_dtmf4_clicked() called!'
        self.handleDtmf('4')
        
    @Slot()
    def on_dtmf5_clicked(self):
        print 'on_dtmf5_clicked() called!'
        self.handleDtmf('5')
        
    @Slot()
    def on_dtmf6_clicked(self):
        print 'on_dtmf6_clicked() called!'
        self.handleDtmf('6')
        
    @Slot()
    def on_dtmf7_clicked(self):
        print 'on_dtmf7_clicked() called!'
        self.handleDtmf('7')
        
    @Slot()
    def on_dtmf8_clicked(self):
        print 'on_dtmf8_clicked() called!'
        self.handleDtmf('8')
        
    @Slot()
    def on_dtmf9_clicked(self):
        print 'on_dtmf9_clicked() called!'
        self.handleDtmf('9')
        
    @Slot()
    def on_dtmf0_clicked(self):
        print 'on_dtmf0_clicked() called!'
        self.handleDtmf('0')
        
    @Slot()
    def on_dtmfStar_clicked(self):
        print 'on_dtmfStar_clicked() called!'
        self.handleDtmf('*')
        
    @Slot()
    def on_dtmfPound_clicked(self):
        print 'on_dtmfPound_clicked() called!'
        self.handleDtmf('#')
        
         
    def playDtmf(self, dtmf):  
        # play the dtmf sound
        if dtmf == '*': dtmf = 'star'
        elif dtmf == '#': dtmf = 'pound'
        QSound.play("./resources/sounds/dtmf-{}.wav".format(dtmf))    
        
    def playRing(self):
        self._soundRing.setLoops(30)
        self._soundRing.play()
        
    def stopRing(self):
        self._soundRing.stop()
        
    def alertIncomingCall(self, name='', cid=''):
        self._msgBoxIncomingCall = msgBox = QMessageBox(QMessageBox.Information, u'알림', u'')
        msgBox.setText(u'전화가 걸려왔습니다.')
        msgBox.setInformativeText(u'번호: %s' % cid)
        buttonConnet = msgBox.addButton(u'연결', QMessageBox.YesRole)
        msgBox.addButton(u'무시', QMessageBox.NoRole)
#        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
#        msgBox.setDefaultButton(QMessageBox.Save)

        msgBox.exec_(); self.stopRing()        
        if msgBox.clickedButton() == buttonConnet:
            sip.answerCall()
        else:
            sip.hangupAllCall()
    
    def closeMsgBoxIncomingCall(self):
        if self._msgBoxIncomingCall:
            self._msgBoxIncomingCall.close()
            self._msgBoxIncomingCall = None
        
    def handleDtmf(self, dtmf):
        self.appendToLabelNumber(dtmf)
    
        # play the dtmf sound
        self.playDtmf(dtmf)
        
        if sip.current_call: #and sip.current_call.info().state == pj.CallState.CONFIRMED:
            sip.current_call.dial_dtmf(dtmf)
    
    def appendToLabelNumber(self, str, clear=False):
        if self._clearLabelNumber or clear:
            selfUi.labelNumber.clear()
            self._clearLabelNumber = False
            
        labelNumber = selfUi.labelNumber
        labelNumberText = labelNumber.text() + str
        labelNumber.setText(labelNumberText)

    def deleteOneLabelNumber(self):
        labelNumber = selfUi.labelNumber
        labelNumber.setText(labelNumber.text()[0:-1])
        
    def keyPressEvent(self, event):
        key = event.key()
                
        if key >= Qt.Key_0 and key <= Qt.Key_9:
            dtmf = (key - Qt.Key_0).__str__()
            
            print dtmf, 'pressed!'
            self.handleDtmf(dtmf)
        elif key == Qt.Key_Asterisk:
            print '* pressed!'
            self.handleDtmf('*')
        elif key == Qt.Key_NumberSign:
            print '# pressed!'
            self.handleDtmf('#')
        elif key == Qt.Key_Backspace:
            print 'Back-space pressed!'
            self.deleteOneLabelNumber()
        elif key == Qt.Key_Escape:
            print 'ESC pressed!'
            self._clearLabelNumber = True
            self.appendToLabelNumber('')
            self.setFocus() # Key(digits) 입력을 받기 위해 메인윈도우로 포커싱
        elif key == Qt.Key_Return:
            print 'Return pressed!'
            self.on_buttonDial_clicked()
        else:
            QWidget.keyPressEvent(self, event)
