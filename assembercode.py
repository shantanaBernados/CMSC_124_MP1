import sys
from PyQt4 import QtCore, QtGui
import assemberui
from assember import AssemBER


class AssemberWindow(QtGui.QMainWindow, assemberui.Ui_AssemBER):
    def __init__(self, parent=None):
        super(AssemberWindow, self).__init__(parent)
        self.setupUi(self)
        self.connect(self.convertasm, QtCore.SIGNAL("clicked()"), self.convertasmcode)

    def convertasmcode(self):
        code = self.asmtextedit.toPlainText()
        print code
        self.mlecode.setText(code)


class ConverterThread():
	pass

app = QtGui.QApplication(sys.argv)
form = AssemberWindow()
form.show()
app.exec_()
