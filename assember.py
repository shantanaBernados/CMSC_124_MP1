# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assemBer.ui'
#
# Created: Sat Apr 18 18:32:55 2015
#      by: PyQt4 UI code generator 4.10.4
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
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 430, 791, 78))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 410, 66, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(9, 10, 801, 391))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.convertasm = QtGui.QPushButton(self.widget)
        self.convertasm.setObjectName(_fromUtf8("convertasm"))
        self.gridLayout.addWidget(self.convertasm, 2, 0, 1, 1)
        self.executemle = QtGui.QPushButton(self.widget)
        self.executemle.setObjectName(_fromUtf8("executemle"))
        self.gridLayout.addWidget(self.executemle, 2, 1, 1, 1)
        self.asmlabel = QtGui.QLabel(self.widget)
        self.asmlabel.setObjectName(_fromUtf8("asmlabel"))
        self.gridLayout.addWidget(self.asmlabel, 0, 0, 1, 1)
        self.asmtextedit = QtGui.QTextEdit(self.widget)
        self.asmtextedit.setObjectName(_fromUtf8("asmtextedit"))
        self.gridLayout.addWidget(self.asmtextedit, 1, 0, 1, 1)
        self.mlecode = QtGui.QTextEdit(self.widget)
        self.mlecode.setObjectName(_fromUtf8("mlecode"))
        self.gridLayout.addWidget(self.mlecode, 1, 1, 1, 1)
        AssemBER.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AssemBER)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        AssemBER.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AssemBER)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AssemBER.setStatusBar(self.statusbar)

        self.retranslateUi(AssemBER)
        QtCore.QMetaObject.connectSlotsByName(AssemBER)

    def retranslateUi(self, AssemBER):
        AssemBER.setWindowTitle(_translate("AssemBER", "AssemBER", None))
        self.label_2.setText(_translate("AssemBER", "Console", None))
        self.label.setText(_translate("AssemBER", "Machine Code", None))
        self.convertasm.setText(_translate("AssemBER", "Convert", None))
        self.executemle.setText(_translate("AssemBER", "Execute", None))
        self.asmlabel.setText(_translate("AssemBER", "Assembly Code", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AssemBER = QtGui.QMainWindow()
    ui = Ui_AssemBER()
    ui.setupUi(AssemBER)
    AssemBER.show()
    sys.exit(app.exec_())

