# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ddirgui import Ui_Form
import os,sys,time

class RowAdder(QtCore.QThread):
    def run(self, form, size, dirname, path):
	form.addRow(size, dirname, path)


class Form(QtGui.QDialog):
    def __init__(self):
	QtGui.QDialog.__init__(self)
	self.ui = Ui_Form()
	self.ui.setupUi(self)
	
	#self.ui.lineEdit.setText('test')
	# All the other stuff here or in other methods.
	self.connectSlots()

    def connectSlots(self):
	self.slotLoad()
	QtCore.QObject.connect(self.ui.buttonLocate, QtCore.SIGNAL("clicked()"), self.slotLocate)
	QtCore.QObject.connect(self.ui.buttonStart, QtCore.SIGNAL("clicked()"), self.slotStart)
	QtCore.QObject.connect(self.ui.table, QtCore.SIGNAL("cellDoubleClicked(int,int)"), self.slotCellDoubleClicked)

    def slotLoad(self):
	self.ui.lineDirectory.setText("/home/emre/deneme")
	self.ui.table.setColumnWidth(0,100)
	self.ui.table.setColumnWidth(1,150)
	self.ui.table.setColumnWidth(2,300)
	"""self.ui.table.setRowCount(1)
	print self.ui.table.item(0,0)
	
	item = QtGui.QTableWidgetItem()
	self.ui.table.setVerticalHeaderItem(0, item)
	item = QtGui.QTableWidgetItem()
	self.ui.table.setItem(0, 0, item)
	item = QtGui.QTableWidgetItem()
	self.ui.table.setItem(0, 1, item)
	item = QtGui.QTableWidgetItem()
	self.ui.table.setItem(0, 2, item)
	self.ui.table.item(0,0).setText("a")
	self.ui.table.item(0,1).setText("b")
	self.ui.table.item(0,2).setText("c")
	"""
	#self.ui.gridLayout.addWidget(self.ui.table, 1, 0, 1, 6)
	
    def slotLocate(self):
	newDirectory = QtGui.QFileDialog.getExistingDirectory (self, "Select Root Directory", "/", QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
	if newDirectory:
	    self.ui.lineDirectory.setText(newDirectory)

    def slotCellDoubleClicked(self, row, column):
	content = str(self.ui.table.item(row,column).text())
	if content.startswith("/"):
	    os.system("dolphin "+content)

    def addRow(self, size, dirname, path):
	rc = self.ui.table.rowCount()
	self.ui.table.setRowCount(rc+1)	
	
	item = QtGui.QTableWidgetItem()
	self.ui.table.setVerticalHeaderItem(rc, item)
	item = QtGui.QTableWidgetItem()
	self.ui.table.setItem(rc, 0, item)
	item = QtGui.QTableWidgetItem()
	self.ui.table.setItem(rc, 1, item)
	item = QtGui.QTableWidgetItem()
	self.ui.table.setItem(rc, 2, item)

	self.ui.table.verticalHeaderItem(rc).setText(str(rc+1))
	self.ui.table.item(rc, 0).setText(str(size))
	self.ui.table.item(rc, 1).setText(dirname)
	self.ui.table.item(rc, 2).setText(path)
	self.ui.table.item(rc, 2).setTextColor(0,0,255,255)
	
	"""
		self.ui.table.verticalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "1", None, QtGui.QApplication.UnicodeUTF8))
		self.ui.table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "Size", None, QtGui.QApplication.UnicodeUTF8))
		self.ui.table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "Dir Name", None, QtGui.QApplication.UnicodeUTF8))
		self.ui.table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "Path", None, QtGui.QApplication.UnicodeUTF8))
		__sortingEnabled = self.ui.table.isSortingEnabled()
		self.ui.table.setSortingEnabled(False)
		self.ui.table.item(0, 0).setText(QtGui.QApplication.translate("Form", "a", None, QtGui.QApplication.UnicodeUTF8))
		self.ui.table.item(0, 1).setText(QtGui.QApplication.translate("Form", "b", None, QtGui.QApplication.UnicodeUTF8))
		self.ui.table.item(0, 2).setText(QtGui.QApplication.translate("Form", "c", None, QtGui.QApplication.UnicodeUTF8))
		self.ui.table.setSortingEnabled(__sortingEnabled)
	"""
    def slotStart(self):
	rootFolder = str(self.ui.lineDirectory.text())
	minFolderSize = self.ui.spinSize.value()
	print "Root folder: ", rootFolder
	print "MinFolderSize:", minFolderSize
	folder_size = 0
	l = []
	for (path, dirs, files) in os.walk(rootFolder):
	    for directory in dirs:
		dir_path=path+"/"+directory
		#dir_path = dir_path.replace(" ", "\ ")
		dir_size=os.popen('du -B 1 -s "'+dir_path+'"').read().split("\t")[0]
		try:
		    dir_size = int(dir_size)
		except:
		    pass
		if dir_size >= minFolderSize:
		    l.append((dir_size, directory, dir_path))
	l.sort()
	l.reverse()
	#print l

	r = 0
	total_size=0
	while r < l.__len__():
	    x = r    
	    try:
		files1 = os.listdir(l[x][2])
		files2 = os.listdir(l[x+1][2])
		if l[x][0] == l[x+1][0] and len(files1) ==  len(files2):
		    print "%d\t%s" % (x, l[x])
		    
		    self.addRow(l[x][0], l[x][1], l[x][2])
		    time.sleep(1)
		    list1 = l[x]
		    list2 = l[x+1]
		    while (list1[0] == list2[0]):
			print "%d\t%s" % (x+1, list2)
			self.addRow(list2[0], list2[1], list2[2])
			time.sleep(1)
			total_size+=list2[0]
			x+=1
			list1 = l[x]
			list2 = l[x+1]
		    r = x+1
		    
		    print
		else:
		    r+=1
	    except:
		#print sys.exc_info()[1]
		r+=1
	    
	print total_size
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NewForm = Form()
    NewForm.show()
    sys.exit(app.exec_())