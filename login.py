# -*- coding: utf8 -*-
'''
Created on 2011. 9. 17.

@author: Xeny
'''
from PySide.QtGui import QDialog
from PySide.QtCore import Slot
import login_ui

loginUi = None

class Login(QDialog):
    
    userId = ''
    userPw = ''
    
    def __init__(self, parent=None):
        super(Login, self).__init__()
        
        global loginUi
        loginUi = login_ui.Ui_Login()
        loginUi.setupUi(self)
        
    
    @Slot()
    def on_buttonLogin_clicked(self):
        print 'Login'
        self.userId = loginUi.inputId.text()
        self.userPw = loginUi.inputPw.text()
        
        if len(self.userId) == 0: return
        if len(self.userPw) == 0: return
        
        self.accept()
                
    @Slot()
    def on_buttonCancel_clicked(self):
        print 'Cancel'
        self.reject()
        
    def closeEvent(self, event):
        print 'closeEvent() called!'
        