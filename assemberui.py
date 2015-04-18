# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assemBer.ui'
#
# Created: Sun Apr 19 00:24:51 2015
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
        AssemBER.resize(831, 579)
        self.centralwidget = QtGui.QWidget(AssemBER)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.consoletext = QtGui.QTextEdit(self.centralwidget)
        self.consoletext.setGeometry(QtCore.QRect(20, 430, 791, 78))
        self.consoletext.setObjectName(_fromUtf8("consoletext"))
        self.consolelabel = QtGui.QLabel(self.centralwidget)
        self.consolelabel.setGeometry(QtCore.QRect(20, 410, 66, 17))
        self.consolelabel.setObjectName(_fromUtf8("consolelabel"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 10, 801, 391))
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
        AssemBER.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AssemBER)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 22))
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

