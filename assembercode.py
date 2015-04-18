import sys
from PyQt4 import QtCore, QtGui
import assemberui
from assember import AssemBER
import time


class AssemberWindow(QtGui.QMainWindow, assemberui.Ui_AssemBER):
    def __init__(self, parent=None):
        super(AssemberWindow, self).__init__(parent)
        self.setupUi(self)
        self.convertasm.clicked.connect(self.convertasmcode)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.consoletext.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.consoletext.setTextCursor(cursor)
        self.consoletext.ensureCursorVisible()

    def convertasmcode(self):
        code = self.asmtextedit.toPlainText()
        code = unicode(code)
        code = code.encode('utf_8')
        code = code.split('\n')
        self.converterThread = ConverterThread(self, code)
        # self.converterThread.mlaSignal.connect(QtGui.QMessageBox.information)
        self.converterThread.mlaSignal.connect(self.mlecode.setText)
        self.converterThread.start()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class ConverterThread(QtCore.QThread):
    mlaSignal = QtCore.pyqtSignal(QtCore.QString)

    def __init__(self, parent=None, *args, **kwargs):
        super(ConverterThread, self).__init__(parent)
        self.initcode(*args, **kwargs)

    def initcode(self, code):
        self.code = code
        print code

    def run(self):
        assember = AssemBER.Instance()
        result = assember.convert(self.code)
        mla = ""
        for line in result:
            mla += line+'\n'
        self.mlaSignal.emit(mla)

app = QtGui.QApplication(sys.argv)
form = AssemberWindow()
form.show()
app.exec_()
