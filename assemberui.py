# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assemBer.ui'
#
# Created: Fri Apr 24 23:59:06 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AssemBER(object):
    def setupUi(self, AssemBER):
        AssemBER.setObjectName(_fromUtf8("AssemBER"))
        AssemBER.resize(865, 752)
        self.centralwidget = QtGui.QWidget(AssemBER)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.consoletext = QtGui.QTextEdit(self.centralwidget)
        self.consoletext.setGeometry(QtCore.QRect(20, 620, 821, 78))
        self.consoletext.setObjectName(_fromUtf8("consoletext"))
        self.consolelabel = QtGui.QLabel(self.centralwidget)
        self.consolelabel.setGeometry(QtCore.QRect(20, 600, 66, 17))
        self.consolelabel.setObjectName(_fromUtf8("consolelabel"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 10, 651, 581))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.mlalabel = QtGui.QLabel(self.layoutWidget)
        self.mlalabel.setObjectName(_fromUtf8("mlalabel"))
        self.gridLayout.addWidget(self.mlalabel, 0, 1, 1, 1)
        self.convertasm = QtGui.QPushButton(self.layoutWidget)
        self.convertasm.setObjectName(_fromUtf8("convertasm"))
        self.gridLayout.addWidget(self.convertasm, 2, 0, 1, 1)
        self.executemle = QtGui.QPushButton(self.layoutWidget)
        self.executemle.setObjectName(_fromUtf8("executemle"))
        self.gridLayout.addWidget(self.executemle, 2, 1, 1, 1)
        self.asmlabel = QtGui.QLabel(self.layoutWidget)
        self.asmlabel.setObjectName(_fromUtf8("asmlabel"))
        self.gridLayout.addWidget(self.asmlabel, 0, 0, 1, 1)
        self.asmtextedit = QtGui.QTextEdit(self.layoutWidget)
        self.asmtextedit.setObjectName(_fromUtf8("asmtextedit"))
        self.gridLayout.addWidget(self.asmtextedit, 1, 0, 1, 1)
        self.mlecode = QtGui.QTextEdit(self.layoutWidget)
        self.mlecode.setObjectName(_fromUtf8("mlecode"))
        self.gridLayout.addWidget(self.mlecode, 1, 1, 1, 1)
        self.layoutWidget1 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(670, 10, 181, 481))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.memlabel = QtGui.QLabel(self.layoutWidget1)
        self.memlabel.setObjectName(_fromUtf8("memlabel"))
        self.gridLayout_2.addWidget(self.memlabel, 0, 0, 1, 1)
        self.stacklabel = QtGui.QLabel(self.layoutWidget1)
        self.stacklabel.setObjectName(_fromUtf8("stacklabel"))
        self.gridLayout_2.addWidget(self.stacklabel, 0, 1, 1, 1)
        self.memlist = QtGui.QListWidget(self.layoutWidget1)
        self.memlist.setObjectName(_fromUtf8("memlist"))
        self.gridLayout_2.addWidget(self.memlist, 2, 0, 1, 1)
        self.stacklist = QtGui.QListWidget(self.layoutWidget1)
        self.stacklist.setObjectName(_fromUtf8("stacklist"))
        self.gridLayout_2.addWidget(self.stacklist, 2, 1, 1, 1)
        self.executestepbtn = QtGui.QPushButton(self.centralwidget)
        self.executestepbtn.setGeometry(QtCore.QRect(690, 500, 141, 27))
        self.executestepbtn.setObjectName(_fromUtf8("executestepbtn"))
        self.startover = QtGui.QPushButton(self.centralwidget)
        self.startover.setEnabled(False)
        self.startover.setGeometry(QtCore.QRect(690, 560, 141, 27))
        self.startover.setCheckable(False)
        self.startover.setObjectName(_fromUtf8("startover"))
        self.stepbtn = QtGui.QPushButton(self.centralwidget)
        self.stepbtn.setEnabled(False)
        self.stepbtn.setGeometry(QtCore.QRect(690, 530, 141, 27))
        self.stepbtn.setObjectName(_fromUtf8("stepbtn"))
        AssemBER.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AssemBER)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 865, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        AssemBER.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AssemBER)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AssemBER.setStatusBar(self.statusbar)

        self.retranslateUi(AssemBER)
        QtCore.QMetaObject.connectSlotsByName(AssemBER)

    def retranslateUi(self, AssemBER):
        AssemBER.setWindowTitle(_translate("AssemBER", "AssemBER", None))
        self.consolelabel.setText(_translate("AssemBER", "Console", None))
        self.mlalabel.setText(_translate("AssemBER", "Machine Code", None))
        self.convertasm.setText(_translate("AssemBER", "Convert", None))
        self.executemle.setText(_translate("AssemBER", "Execute", None))
        self.asmlabel.setText(_translate("AssemBER", "Assembly Code", None))
        self.memlabel.setText(_translate("AssemBER", "Memory", None))
        self.stacklabel.setText(_translate("AssemBER", "Stack", None))
        self.executestepbtn.setText(_translate("AssemBER", "Execute Step by Step", None))
        self.startover.setText(_translate("AssemBER", "Start Over", None))
        self.stepbtn.setText(_translate("AssemBER", "Do Step", None))

