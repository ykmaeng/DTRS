# -*- coding: utf-8 -*-

'''
Created on 2011. 9. 14.

@author: Xeny
'''

import xlrd
from PySide.QtGui import *
from PySide.QtCore import *
import os, csv
import main_ui, widget_addr_ui, progress_import_ui

main = None
mainUi = None
dbConn = None
addr = None

class WidgetAddr(QWidget):
    _book = None            # 엑셀 핸들
    _sheet = None           # 엑셀 시트 핸들
    
    _fullFileName = ''      # 주소록 전체 파일명(경로포함)
    _baseFileName = ''      # 주소록 파일명
    
    _prog = None            # 프로그래스 위젯
    
    _tabIndex = 0           # 자신의 탭 인덱스
    
    _addrTitle = ''         # 주소록 제목
    _addrNo = 0             # DB의 Addr 키 값
    _addrSeq = 0            # Tab 순서
    _public = 0         # 공개주소록 여부
    _dataLoaded = False     # 데이터 적재 여부
    
    _title = ''
    _numCols = 0            # 주소록 컬럼 개수
    _numRows = 0            # 주소록 총 레코드 수
    _rowsCols = ()          # 컬럼명 (tutple)
    _rowsTree = ()
    _rowsTable = ()
    
    signal_import_finished = Signal(str)
    signal_create_pressed = Signal() 
    
    class FileType:
        TXT = 1; CSV = 2; XLS = 3; XLSX = 4
    
    def __init__(self, parent, no=0, seq=0, title=u'새주소록', public=False, numcols=0):
        super(WidgetAddr, self).__init__()
        
        global main, mainUi, dbConn
        main = parent
        mainUi = main.mainUi()
        dbConn = main.dbConn()
        
        self._addrNo = no
        self._addrSeq = seq
        self._addrTitle = title
        self._public = public
        self._numCols = numcols
        
        self.ui = widget_addr_ui.Ui_widgetAddr()
        self.ui.setupUi(self)
        
        self.ui.checkPublic.setChecked(public)
        
        self.ui.checkPublic.stateChanged.connect(self.on_checkPublic_stateChanged)        
        self.ui.treeAddr.currentItemChanged.connect(self.on_treeAddr_currentItemChanged)
        self.ui.tableAddr.cellClicked.connect(self.on_tableAddr_cellClicked)
        self.ui.tableAddr.cellDoubleClicked.connect(self.on_tableAddr_cellDoubleClicked)
        
        self.ui.textSearch.returnPressed.connect(self.on_textSearch_returnPressed)
        

    @Slot()
    def on_textSearch_returnPressed(self):
        print 'on_textSearch_returnPressed() called!'
        self.on_buttonSearch_clicked();
                
    @Slot()
    def on_buttonSearch_clicked(self):
        print 'on_buttonSearch_clicked() called!'
        self.ui.tableAddr.setFocus()
        
        text = self.ui.textSearch.text()
        if len(text) == 0: return
        
        items = self.ui.tableAddr.findItems(text, Qt.MatchContains)
        
        print 'len(items):', len(items)
        if len(items) > 0:
            self.ui.tableAddr.scrollToItem(items[0])
            for item in items:
#                self.ui.tableAddr.setCurrentItem(item);
                numColumns = self.ui.tableAddr.columnCount();
                numRow = item.row();
                selectionRange = QTableWidgetSelectionRange(numRow, 0, numRow, numColumns-1) 
                self.ui.tableAddr.setRangeSelected(selectionRange, True);            

        
    @Slot()
    def on_buttonImport_clicked(self):
        print 'on_buttonImport_clicked() called!'
        file = QFileDialog.getOpenFileName(main, 'Open Document', QDir.homePath(), 'Documents (*.txt *.csv *.xls)')
        
        # 전체파일명(경로+파일명) 저장
        fullFileName = unicode(file[0])
        
#        os.path.splitext(fullFileName)[0]
        baseFileName = os.path.basename(fullFileName)

        self._fullFileName = fullFileName
        self._baseFileName = baseFileName

        ok = self.checkDataValidation()
        if not ok:
            pass        
        else:
            self.showFileInfo()          
        
    @Slot()
    def on_buttonExport_clicked(self):
        print 'on_buttonExport_clicked() called!'


    @Slot()
    def on_buttonCreate_clicked(self):
        print 'on_buttonCreate_clicked() called!'
        self.signal_create_pressed.emit()
    
    def refreshTabIcon(self, index):
        file_normal_on = 'group.png' if self._public else 'user.png'
        file_normal_off = 'group_gray.png' if self._public else 'user_gray.png'
             
        icon = QIcon()
        icon.addPixmap(QPixmap("./resources/images/%s" % file_normal_on), QIcon.Normal, QIcon.On)
        icon.addPixmap(QPixmap("./resources/images/%s" % file_normal_off), QIcon.Normal, QIcon.Off)
        
        mainUi.tabAddress.setTabIcon(index, icon)
    
    def getAddrLabelsFromDB(self):
        query_head = 'select '
        query_body = ''
        query_tail = ' from addr_labels where no_addr_list=%d' % self._addrNo
        
        for n in range(self._numCols-3):
            if n > 0: query_body = query_body + ','
            query_body = query_body + 'label%d' % (n + 4)
        
        query = query_head + query_body + query_tail
#        print 'getAddrLabelsFromDB() => query:', query
        
        cursor = dbConn.cursor()
        cursor.execute(query)
        self._rowsCols = cursor.fetchone()
        print self._rowsCols
        
    def setAddrLabelsToTable(self):
        self.ui.tableAddr.setColumnCount(self._numCols - 3)
        self.ui.tableAddr.setHorizontalHeaderLabels(self._rowsCols)
        
    def getTreeDataFromDB(self):
        query = """
            select no, data1, data2, data3
            from addr_data where no_addr_list=%d
            group by data1, data2, data3
            order by data1, data2, data3
            """ % self._addrNo
        
#        print 'getTreeDataFromDB() => query:', query
        
        cursor = dbConn.cursor()
        cursor.execute(query)
        self._rowsTree = cursor.fetchall()
    
    def setDataToTree(self):
        tree = self.ui.treeAddr
        
        tree.setColumnCount(1)
        tree.setHeaderLabels([self._addrTitle])
        
        prev_data1 = prev_data2 = ''
        item_data1 = item_data2 = item_data3 = None

        rowNum = 0
        for row in self._rowsTree:
            if prev_data1 != row[1]:
                item_data1 = QTreeWidgetItem(tree, [row[1]])
                item_data2 = QTreeWidgetItem(item_data1, [row[2]])
                item_data3 = QTreeWidgetItem(item_data2, [row[3]])

                item_data1.setExpanded(True)
                item_data2.setExpanded(True)
                prev_data1 = row[1]
                prev_data2 = row[2]
                
            elif prev_data2 != row[2]:
                item_data2 = QTreeWidgetItem(item_data1, [row[2]])
                item_data3 = QTreeWidgetItem(item_data2, [row[3]])
                
                item_data2.setExpanded(True)
                prev_data2 = row[2]
                
            else:
                item_data3 = QTreeWidgetItem(item_data2, [row[3]])

            # 주소록  데이터를 가져오기 위해 마지막 노드에는 키 값을 저장한다. 
            item_data3.setWhatsThis(0, unicode(rowNum))            
            rowNum += 1
            

    
    def getAddrDataFromDB(self, rowNum):
        print 'getAddrDataFromDB() => rowNum:', rowNum
        row = self._rowsTree[rowNum]
        query_head = 'select '
        query_body = 'no'
        query_tail = """
            from addr_data 
            where no_addr_list=%d and data1='%s' and data2='%s' and data3='%s'
            """ % (self._addrNo, row[1], row[2], row[3]) 
        
        for n in range(self._numCols-3):
            query_body += ',data%d' % (n + 4)
        
        query = query_head + query_body + query_tail
#        print 'getAddrDataFromDB() => query:', query
        
        cursor = dbConn.cursor()
        cursor.execute(query)
        self._rowsTable = cursor.fetchall()
        print "Number of rows returned: %d" % cursor.rowcount
        cursor.close()
                
    def showAddrDataOnTable(self):
        self.ui.tableAddr.setRowCount(len(self._rowsTable))
        rowIdx = 0
        for row in self._rowsTable:
            colIdx = 0
            # row[0] ~ row[2] 까지는 내부적으로 사용하기 위한 것이므로 테이블에 표시 안함
            for item in row[1:]:
                newItem = QTableWidgetItem(unicode(item))
                newItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                newItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
#                if rowIdx % 2 == 1: newItem.setBackground(QColor(250, 250, 250))
                self.ui.tableAddr.setItem(rowIdx, colIdx, newItem)
                colIdx += 1
            rowIdx += 1

    def showData(self, tab_index):
        self._tabIndex = tab_index
        
        if self._dataLoaded: return
        if self._numCols == 0: return
        
        self.ui.treeAddr.clear()
        self.ui.tableAddr.clear()
        
        self.getAddrLabelsFromDB()
        self.setAddrLabelsToTable()
        
        self.getTreeDataFromDB()
        self.setDataToTree()
#        self.getAddrDataFromDB()
#        self.setAddrData()

        self._dataLoaded = True
        
        
    def on_treeAddr_currentItemChanged(self, curr, prev):
        print 'currentItemChanged() called!'
        curr_key = prev_key = None
        if curr: curr_key = curr.whatsThis(0)
        if prev: prev_key = prev.whatsThis(0)
        print 'curr_key:', curr_key, 'prev_key:', prev_key
        
        text = curr.text(0)
        parent = curr.parent()
        if parent:
            text = parent.text(0) + ' - ' + text
            if parent.parent():
                text = parent.parent().text(0) + ' - ' + text
            
        self.ui.labelTitle.setText(text)
        
        if len(curr_key) > 0:
            self._rowsTable = ()
            self.getAddrDataFromDB(int(curr_key))
            self.ui.tableAddr.clearContents()
            self.ui.tableAddr.setSortingEnabled(False)
            self.showAddrDataOnTable()
            self.ui.tableAddr.setSortingEnabled(True)
            
    def on_tableAddr_cellClicked(self, row, column):
        table = self.ui.tableAddr
        
        item = table.item(row, column)
        rx = QRegExp('^0[1-9][0-9]{7,}')    # 전화번호 패턴
        if rx.indexIn(item.text()) == 0:
            main.widgetDialpad.ui().labelNumber.setText(item.text())
        
        nums = ''
        colcnt = table.columnCount()
        for colnum in range(colcnt):
            itemText = table.item(row, colnum).text()
            if rx.indexIn(itemText) == 0:   # matched
                if len(nums) > 0: nums = nums + ','
                nums += "'" + itemText + "'"
                
        if len(nums) > 0:
            if not main.widgetHistory.ui().checkAllHistory.isChecked():
                main.widgetHistory.refreshTableHistory('%s' % nums)
            
    def on_tableAddr_cellDoubleClicked(self, row, column):
        pass
        
    def on_checkPublic_stateChanged(self, state):
        print 'on_checkPublic_stateChanged() called! => state:', state
        
        if self._public == (1 if state == 2 else 0):
            print 'self._public == state.'
            return
        
        msgBox = QMessageBox(QMessageBox.Question, u'주소록 변경', u'')
        buttonYes = msgBox.addButton(u'예', QMessageBox.YesRole)
        msgBox.addButton(u'아니오', QMessageBox.NoRole)

        if state == 0:      # 개인주소록
            msgBox.setText(u'개인주소록으로 바꾸시겠습니까?')
        else:               # 공개주소록
            msgBox.setText(u'공개주소록으로 바꾸시겠습니까?')
            
        msgBox.exec_()        
        if msgBox.clickedButton() == buttonYes:
            self.changeAddrType()
        else:
            checkState = Qt.Unchecked if state == 2 else Qt.Checked
            self.ui.checkPublic.setCheckState(checkState)

    def changeAddrType(self):
#        public = 0 if self._public else 1
        public = 1 if self.ui.checkPublic.isChecked() else 0
        query = """
            update addr_list set public=%d where no=%d
            """ % (public, self._addrNo)
            
        print query
        
        dbConn.cursor().execute(query)
        self._public = public
        self.refreshTabIcon(self._tabIndex)
    
    def startImport(self):
        self._prog.ui.buttonStart.setDisabled(True)
        
        if self._prog.ui.checkRemoveOldData.isChecked():
            self.deleteAndInsertAddr()
        else:
            # TODO: self.updateAndInsertAddr()
            return
        
        self._addrTitle = os.path.splitext(self._baseFileName)[0]
        
#        self._numCols = self._sheet.ncols
        self._dataLoaded = False
        self.showData(self._tabIndex)
        self.signal_import_finished.emit(self._addrTitle)
        
    def deleteAndInsertAddr(self):
        # 기존 공개주소록은 비활성화시킨다.
        self._prog.ui.labelMessage.setText(u'기존 자료를 비활성화합니다.')
        ok = self.disableCurrentAddr()
        
        self._prog.ui.labelMessage.setText(u'새로운 주소록을 생성합니다.')
        ok = self.insertNewAddr(self._baseFileName, self._sheet.name)
        if not ok:
            pass
        else:
            self._addrNo = ok
            print 'self.insertNewAddr():', self._addrNo
        
        self._prog.ui.labelMessage.setText(u'주소록 라벨을 생성합니다.')
        ok = self.insertAddrLabelIntoDB()
        print 'self.insertAddrLabelIntoDB():', self._addrNo
        
        self._prog.ui.labelMessage.setText(u'조소록을 입력합니다.')
        ok = self.insertDataIntoDB()
    
                
    def checkDataValidation(self):
        self._fileExt = os.path.splitext(self._baseFileName)[1].lower()[1:]
        if self._fileExt == "txt":
            with open(self._fullFileName, 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    print row
        elif self._fileExt == "csv":
            with open(self._fullFileName, 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    print row
        elif self._fileExt == "xls":
            try:
                self._book = xlrd.open_workbook(self._fullFileName)
                self._sheet = self._book.sheet_by_index(0)    # 첫 번째 시트
                
                self._title = self._sheet.name
                self._numRows = self._sheet.nrows
                self._numCols = self._sheet.ncols
                
                print self._title
                print self._numRows
                print self._numCols
                
                labels = self._sheet.row_values(0)
                idx = 0
                for value in labels:
                    labels[idx] = unicode(value)
                    idx += 1
                self._labels = labels
#                print 'labels:', labels
            except:
                print 'Error in loading from a file', self._fullFileName
        else:
            return False

        return True
    
    
    def showFileInfo(self):
        self._prog = ProgressImport()
        self._prog.ui.buttonStart.clicked.connect(self.startImport)
        self._prog.ui.labelMessage.setText(u'파일명: %s, 데이터수: %d' % (self._baseFileName, self._numRows))
        start = self._prog.exec_()
        if not start:
            self._prog.close()
            return False
    
    def disableCurrentAddr(self):
        query = "update addr_list set valid='0' where no=%d" % self._addrNo
        dbConn.cursor().execute(query)
        
    def insertNewAddr(self, filename='', title=''):
        cursor = dbConn.cursor()
        cursor.execute(u"""
            insert into addr_list
                (no_user_list, addr_filename, addr_title, column_count, create_date, public, valid)
            values
                (%s, %s, %s, %s, now(), '0', '1')
            """,
            (main.sipId, filename.encode('utf8'), title.encode('utf8'), self._numCols))
        
        return dbConn.insert_id()
        

    def insertAddrLabelIntoDB(self):
        query_sub1 = "no_addr_list"
        query_sub2 = "%d" % self._addrNo
        
        for n in range(self._numCols):
            query_sub1 += ',label' + str(n+1)
            query_sub2 += ',%s'
        
        query_full = "insert into addr_labels (%s) values (%s)" % (query_sub1, query_sub2)
#        print query_full
        
        dbConn.cursor().execute(query_full, tuple(self._labels))
        return dbConn.insert_id()
        
        return True
        
        
    def insertDataIntoDB(self):
        cursor = dbConn.cursor()
        query_sub1 = "no_addr_list"
        query_sub2 = "%d" % self._addrNo
        
        for n in range(self._numCols):
            query_sub1 += ',data' + str(n+1)
            query_sub2 += ",%s"
            
        query_full = "insert into addr_data (%s) values (%s)" % (query_sub1, query_sub2)
#        print query_full
        
        totalRows = self._numRows
        self._prog.ui.progressBar.setRange(0, totalRows)
        self._prog.ui.progressBar.reset()
        
        for rownum in range(totalRows):
            if rownum == 0: continue
            row_values = self._sheet.row_values(rownum)
#            print row_values
            
            idx = 0
            temp = ''
            for value in row_values:
                temp = unicode(value)
                if temp[-2:] == '.0': temp = temp[:-2]
                row_values[idx] = temp
                idx += 1
        
            cursor.execute(query_full, tuple(row_values))
            
            self._prog.ui.labelMessage.setText(u'자료를 입력 중입니다.. (%d/%d)' % (rownum+1, totalRows))
            self._prog.ui.progressBar.setValue(rownum+1)
#            self._prog.ui.progressBar.update()

        self._prog.ui.labelMessage.setText(u'작업을 완료하였습니다. (%d/%d)' % (rownum+1, totalRows))
        self._prog.ui.buttonCancel.setText(u'닫기')
                
        return True
        
#        cursor = dbConn.cursor()
#        cursor.execute(query)  

class ProgressImport(QDialog):
    def __init__(self):
        super(ProgressImport, self).__init__()
        
        self.ui = progress_import_ui.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setWindowTitle(u'자료 입력')
        self.ui.progressBar.setValue(0)
        self.ui.checkRemoveOldData.setText(u'기존 자료를 삭제하고 새로 입력합니다.')
        self.ui.checkRemoveOldData.setChecked(True)


#    @Slot()
#    def on_buttonStart_clicked(self):
#        print 'on_buttonStart_clicked() called!'
#        self.accept()
        
    @Slot()
    def on_buttonCancel_clicked(self):
        print 'on_buttonCancel_clicked() called!'
        self.reject()
        
    def closeEvent(self, event):
        print 'closeEvent() called!'