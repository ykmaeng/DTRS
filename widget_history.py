# -*- coding: utf-8 -*-

'''
Created on 2011. 9. 14.

@author: Xeny
'''

from PySide.QtGui import *
from PySide.QtCore import *
import widget_history_ui
import os

main = None
mainUi = None
selfUi = None
dbConn = None


class WidgetHistory(QWidget):
    
    _clearHistory = False
    _lastCellClicked = None
    _current_callee_num = ''
    _rowsHistory = None   # rows of tableHistory
    _phoneNumToShow = ''
    
    def __init__(self, parent):
        super(WidgetHistory, self).__init__()
        
        global main, selfUi, dbConn
        main = parent
        mainUi = main.mainUi()
        dbConn = main.dbConn()
        
        selfUi = widget_history_ui.Ui_Widget()
        selfUi.setupUi(self)
        
        self.initTableHistory()
        
    @staticmethod
    def ui(): global selfUi; return selfUi
    
    def initTableHistory(self):
        selfUi.tableHistory.setColumnCount(7)
        selfUi.tableHistory.setHorizontalHeaderLabels([u'발신번호',u'수신번호',u'방향',u'발신시각',u'종료시각',u'통화시간(초)',u'메모'])
        selfUi.tableHistory.setColumnWidth(0, 90)
        selfUi.tableHistory.setColumnWidth(1, 90)
        selfUi.tableHistory.setColumnWidth(2, 40)
        selfUi.tableHistory.setColumnWidth(3, 130)
        selfUi.tableHistory.setColumnWidth(4, 130)
        selfUi.tableHistory.setColumnWidth(5, 80)
        selfUi.tableHistory.setColumnWidth(6, 300)
        
        selfUi.tableHistory.sortByColumn(3, Qt.DescendingOrder)

    def refreshTableHistory(self, num=''):
        if num is not '':
            self._phoneNumToShow = num               
        
        self._clearHistory = True
        selfUi.tableHistory.setSortingEnabled(False)        
        selfUi.tableHistory.clearContents()
        self.showTableHistory(num)
        selfUi.tableHistory.setSortingEnabled(True)
        self._clearHistory = False
        
    def showTableHistory(self, num=''):
        query = """
            select no, rec_filename, rec_format, ifnull(from_num,''), ifnull(to_num,''), ifnull(direction,''),
            ifnull(dial_date,''), ifnull(disconnected_date,''), ifnull(duration,0), ifnull(note,'')
            from call_log where valid = '1' """
        
        if num is not '':
            query += " and (from_num in ({0}) or to_num in ({0}))".format(num)
#            print query            
        
        cursor = dbConn.cursor()
        cursor.execute(query)    
        self._rowsHistory = cursor.fetchall()
        
        selfUi.tableHistory.setRowCount(cursor.rowcount)
        
        rowIdx = 0
        for row in self._rowsHistory:
            colIdx = 0
            # row[0] ~ row[2] 까지는 내부적으로 사용하기 위한 것이므로 테이블에 표시 안함
            for item in row[3:]:
#                newItem = QTableWidgetItem(u'%s' % str(item).decode('utf-8'))
                newItem = QTableWidgetItem(unicode(item))
                newItem.setWhatsThis(unicode(rowIdx))
                
                if colIdx == 6:
                    newItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                    newItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                else:
                    newItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    newItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
#                if rowIdx % 2 == 1: newItem.setBackground(QColor(240, 240, 240))
                selfUi.tableHistory.setItem(rowIdx, colIdx, newItem)
                colIdx += 1
            
            rowIdx += 1
            
        print "Number of rows returned: %d" % cursor.rowcount
        cursor.close()
    
    @Slot()
    def on_textSearch_returnPressed(self):
        print 'on_textSearch_returnPressed() called!'
        self.on_buttonSearch_clicked();
        
    @Slot()
    def on_buttonSearch_clicked(self):
        print 'on_buttonSearch_clicked() called!'
        selfUi.tableHistory.setFocus()
        
        text = selfUi.textSearch.text()
        if len(text) == 0: return
        
        items = selfUi.tableHistory.findItems(text, Qt.MatchContains)
        
        print 'len(items):', len(items)
        if len(items) > 0:
            selfUi.tableHistory.scrollToItem(items[0])
            for item in items:
#                self.ui.tableAddr.setCurrentItem(item);
                numColumns = selfUi.tableHistory.columnCount()
                numRow = item.row()
                selectionRange = QTableWidgetSelectionRange(numRow, 0, numRow, numColumns-1) 
                selfUi.tableHistory.setRangeSelected(selectionRange, True)
    
    @Slot()
    def on_buttonRefresh_clicked(self):
        if selfUi.checkAllHistory.isChecked():
            self.refreshTableHistory()
        else:
            self.refreshTableHistory(self._phoneNumToShow)
        
    @Slot()
    def on_buttonPlay_clicked(self):
        print 'on_buttonPlay_clicked() called!'
        if self._lastCellClicked:
            row, column = self._lastCellClicked
            item = selfUi.tableHistory.item(row, column)
            
            realRowNum = int(item.whatsThis())
            fileName = self._rowsHistory[realRowNum][1]
            fileFormat = self._rowsHistory[realRowNum][2]
            self.playVoiceFile(fileName, fileFormat)

    @Slot(int, int)
    def on_tableHistory_cellChanged(self, row, column):
        if self._clearHistory: return
         
        print 'on_tableHistory_cellChanged() called! => row: %d, column: %d' % (row, column)
        item = selfUi.tableHistory.item(row, column)
        realRowNum = int(item.whatsThis())
        changedText = item.text()
        key = self._rowsHistory[realRowNum][0]
        query = "update call_log set note='%s' where no=%d" % (changedText.encode('utf-8'), key)
#        print query
        cursor = dbConn.cursor()
#        cursor.execute(query.encode('utf-8'))
        cursor.execute(query)
        
    @Slot(int, int)
    def on_tableHistory_cellClicked(self, row, column):
        print 'on_tableHistory_cellClicked() called!'
        self._lastCellClicked = row, column
        
        item = selfUi.tableHistory.item(row, column)
        rx = QRegExp('^0[1-9][0-9]{7,}')    # 전화번호 패턴
        if rx.indexIn(item.text()) == 0:
            main.widgetDialpad.ui().labelNumber.setText(item.text())
        
    @Slot(QTableWidgetItem)
    def on_tableHistory_itemDoubleClicked(self, item):
        print 'on_tableHistory_itemDoubleClicked() called!'
        ncol = item.column()
        if ncol == 0 or ncol == 1:
            realRowNum = int(item.whatsThis())
            fileName = self._rowsHistory[realRowNum][1]
            fileFormat = self._rowsHistory[realRowNum][2]
            self.playVoiceFile(fileName, fileFormat)

    @Slot(int)
    def on_checkAllHistory_stateChanged(self, state):
        print 'on_checkAllHistory_stateChanged() called! => state:', state
        print 'self._phoneNumToShow:', self._phoneNumToShow
        if state == 0:
            self.refreshTableHistory(self._phoneNumToShow)
        else:
            self.refreshTableHistory()

    def playVoiceFile(self, fileName, fileFormat='wav'):
        url = 'http://%s:8080/voice/dtrs/%s.%s' % (main.sipAddr, fileName, fileFormat)
        QDesktopServices.openUrl(url)