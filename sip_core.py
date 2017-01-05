# -*- coding: utf-8 -*-

'''
Created on 2011. 9. 14.

@author: Xeny
'''

import sys
import threading
import pjsua as pj
from PySide.QtCore import Signal, QObject

sipCore = None

class SipCore(QObject):
    
    current_acc = None
    current_call = None
    sip = None
    
    proxyAddr = None
#    proxyPort = None
    userId = None
    userPw = None
    
    signal_reg_succeed = Signal(object)
    signal_reg_failed = Signal(object)
    signal_call_incoming = Signal(object)
    signal_call_connected = Signal(object)
    signal_call_disconnected = Signal(object)
    signal_call_placing = Signal(object)
    signal_rec_started = Signal(object)
    signal_rec_stoped = Signal(object)
    
    def __init__(self):
        global sipCore
        sipCore = self
        super(SipCore, self).__init__()
    
    # Logging callback
    def log_cb(self, level, str, len):
        print str
    
    def initPjsua(self):
        try:
            # Create lbrary instance
            self.sip = pj.Lib()
            
            # Init library with default config
            '''
            The  init() method takes three optional arguments to specify various core settings:
            - UAConfig, to specify core SIP user agent settings
            - MediaConfig, to specify various media settings, including ICE and TURN.
            - LogConfig, to customize logging settings.
            '''
            self.sip.init(log_cfg=pj.LogConfig(level=3, callback=self.log_cb))
            
            # Create UDP transport which listeners to any avaliable port
            self.sip.create_transport(pj.TransportType.UDP)
            
            # Start the library
            self.sip.start()
            
#            # Create local/user-less account
#            acc = sipCore.sip.create_account_for_transport(transport)
#            sipCore.current_acc = acc
            
            
            # Wait for click to 
        except pj.Error, e:
            print 'Exception: ' + str(e)
            self.destroySip()
            sys.exit(1)
    
    def regAccount(self, id, pw, domain):
        
        try:
            self.proxyAddr = domain
            self.userId = id
            self.userPw = pw
            
            acc = self.sip.create_account(pj.AccountConfig(domain, id, pw))    
            acc_cb = self.AccountCallback(acc)
            acc.set_callback(acc_cb)
            acc_cb.wait()
        
            print "\n"
            print "Registration complete, status=", acc.info().reg_status, \
                "(" + acc.info().reg_reason + ")"

        except pj.Error, err:
            print 'Error creating account:', err
    
    def makeCall(self, acc, sip_uri):
        if acc is None: return 0
        return acc.make_call(sip_uri, self.CallCallback())
    
    def answerCall(self):
        self.current_call.answer()
    
    def hangupCurrCall(self):
        if (self.current_call != None):
            self.current_call.hangup()
            
    def hangupAllCall(self):
        self.sip.hangup_all()
    
    def recordCall(self):
        pass
    
    def destroySip(self):
        self.sip.destroy()
        self.sip = None
    
    # Callback to receive events fro Call
    class CallCallback(pj.CallCallback):
        def __init__(self, call=None, parent=None):
            pj.CallCallback.__init__(self, call)
            sipCore.current_call = call
            
        # Notification when call state has changed
        def on_state(self):
            print 'Call with', self.call.info().remote_uri,
            print 'is', self.call.info().state_text,
            print 'last code = ', self.call.info().last_code,
            print '(' + self.call.info().last_reason + ')'
            
            sipCore.current_call = self.call
            
            if self.call.info().state == pj.CallState.DISCONNECTED:
                sipCore.current_call = None
                sipCore.signal_call_disconnected.emit(self.call)
                print 'Current call is', sipCore.current_call
            elif self.call.info().state == pj.CallState.CONFIRMED:
                sipCore.signal_call_connected.emit(self.call)
            else:
                pass
            
        # Notification when call's media state has changed
        def on_media_state(self):
            if self.call.info().media_state == pj.MediaState.ACTIVE:
                # Connect the call to sound device
                call_slot = self.call.info().conf_slot
                sipCore.sip.conf_connect(call_slot, 0)
                sipCore.sip.conf_connect(0, call_slot)
                print "Media is now active"
            else:
                print "Media is inactive"

    class AccountCallback(pj.AccountCallback):
        def __init__(self, account=None):
            pj.AccountCallback.__init__(self, account)
            self._sem = None
    
        def on_incoming_call(self, call):
            print 'on_incoming_call() called!'
            
            if sipCore.current_call:
                call.answer(486, 'Busy')
                return
            
            print 'Incoming call from ', call.info().remote_uri
            
            sipCore.current_call = call
            call_cb = sipCore.CallCallback(sipCore.current_call)
            sipCore.current_call.set_callback(call_cb)
            sipCore.current_call.answer(180)
#            call.hangup(501, "Sorry, not ready to accept calls yet")

            sipCore.signal_call_incoming.emit(call)
     
        def wait(self):
            self._sem = threading.Semaphore(0)
            self._sem.acquire()

        def on_reg_state(self):            
            if self._sem:
                self._sem.release()
                if self.account.info().reg_status == 200:
                    sipCore.current_acc = self.account
                    sipCore.signal_reg_succeed.emit(self.account)
                else:
                    sipCore.signal_reg_failed.emit(self.account)
