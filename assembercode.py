import sys
import os
from PyQt4 import QtCore, QtGui
import ExecuteThread
import assemberui
from assember import AssemBER
from AppQueue import queue


class AssemberWindow(QtGui.QMainWindow, assemberui.Ui_AssemBER):
    def __init__(self, parent=None):
        super(AssemberWindow, self).__init__(parent)
        self.setupUi(self)
        self.consoletext.setReadOnly(True)
        self.consoletext.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse |
            QtCore.Qt.TextSelectableByKeyboard)
        self.convertasm.clicked.connect(self.convertasmcode)
        self.executemle.clicked.connect(self.executemlacode)
        self.executestepbtn.clicked.connect(self.executestepcode)
        self.stepbtn.clicked.connect(self.dostep)
        self.startover.clicked.connect(self.restartexecute)
        self.currentline = 0
        self.asmtextedit.viewport().installEventFilter(
            QAsmEditDropHandler(self, self.asmtextedit))
        self.format = QtGui.QTextBlockFormat()
        self.format.setBackground(QtCore.Qt.yellow)
        self.clearformat = QtGui.QTextBlockFormat()
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def normalOutputWritten(self, text):
        cursor = self.consoletext.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.consoletext.setTextCursor(cursor)
        self.consoletext.ensureCursorVisible()

    def convertasmcode(self):
        code = self.asmtextedit.toPlainText()
        if code:
            code = unicode(code)
            code = code.encode('utf_8')
            code = code.split('\n')
            self.converterThread = ConverterThread(self, code)
            self.converterThread.mlaSignal.connect(self.mlecode.setText)
            self.converterThread.start()
        else:
            print "empty"

    def executemlacode(self):
        code = self.mlecode.toPlainText()
        if code:
            code = unicode(code)
            code = code.encode('utf_8')
            code = code.split('\n')
            self.executeThread = ExecuteThread(self, code)
            self.executeThread.getinput.connect(self.getinput)
            self.executeThread.start()
        else:
            print "empty"

    def getinput(self):
        val, ok = QtGui.QInputDialog.getInt(self, 'Input Dialog',
                                            'What is the value of N?')
        if ok:
            queue.put(val)

    def executestepcode(self):
        code = self.mlecode.toPlainText()
        if code:
            code = unicode(code)
            code = code.encode('utf_8')
            code = code.split('\n')
            self.assember = AssemBER.Instance()
            self.assember.clear()
            self.assember.loadcodetomem(code)
            self.stepbtn.setEnabled(True)
            self.startover.setEnabled(True)
        else:
            print "empty"

    def dostep(self):
        self.setLineFormat(self.currentline)
        line = self.assember.execute_line(self.currentline, self)
        if line:
            if type(line) is int:
                self.currentline = line
            self.currentline += 1
        else:
            self.stepbtn.setEnabled(False)

    def restartexecute(self):
        endline = self.currentline
        self.currentline = 0

        for x in range(0, endline+1):
            cursor = QtGui.QTextCursor(self.mlecode.document().findBlockByNumber(x))
            cursor.setBlockFormat(self.clearformat)
        self.stepbtn.setEnabled(False)

    def setLineFormat(self, lineNumber):
        cursor = QtGui.QTextCursor(self.mlecode.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(self.format)


class QAsmEditDropHandler(QtCore.QObject):
    def __init__(self, parent=None, *args, **kwargs):
        QtCore.QObject.__init__(self, parent)
        self.initcode(*args, **kwargs)

    def initcode(self, asmtextedit):
        self.asmtextedit = asmtextedit

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.DragEnter:
            data = event.mimeData()
            urls = data.urls()
            if (urls and urls[0].scheme() == 'file'):
                event.accept()
                return True

        if event.type() == QtCore.QEvent.DragMove:
            data = event.mimeData()
            urls = data.urls()
            if (urls and urls[0].scheme() == 'file'):
                event.accept()
                return True

        if event.type() == QtCore.QEvent.Drop:
            data = event.mimeData()
            urls = data.urls()
            if (urls and urls[0].scheme() == 'file'):
                # for some reason, this doubles up the intro slash
                # filepath = urls[0].toString()
                path = urls[0].toLocalFile().toLocal8Bit().data()
                if os.path.isfile(path):
                    print path
                    f = open(path, 'r')
                    lines = f.read()
                    self.asmtextedit.setText(lines)
                else:
                    print "Not a file"
                return True
        return False


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

    def run(self):
        assember = AssemBER.Instance()
        result = assember.convert(self.code)
        if result:
            mla = ""
            for line in result:
                mla += line+'\n'
            self.mlaSignal.emit(mla)
        else:
            self.mlaSignal.emit("")
            print "Convertion failed"


class ExecuteThread(QtCore.QThread):
    getinput = QtCore.pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(ExecuteThread, self).__init__(parent)
        self.initcode(*args, **kwargs)

    def initcode(self, code):
        self.code = code

    def run(self):
        assember = AssemBER.Instance()
        assember.execute(self.code, self)
        # mla = ""
        # for line in result:
        #     mla += line+'\n'
        # self.mlaSignal.emit(mla)

app = QtGui.QApplication(sys.argv)
form = AssemberWindow()
form.show()
app.exec_()
