import sys
import os
from PyQt4 import QtCore, QtGui
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
        self.errorformat = QtGui.QTextBlockFormat()
        self.errorformat.setBackground(QtCore.Qt.red)
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
        self.clearlineformat(30)
        self.consoletext.setText("")
        code = self.asmtextedit.toPlainText()
        if code:
            code = unicode(code)
            code = code.encode('utf_8')
            code = code.split('\n')
            self.converterThread = ConverterThread(self, code)
            self.converterThread.mlaSignal.connect(self.mlecode.setText)
            self.converterThread.error.connect(self.setErrorConvFormat)
            self.converterThread.start()
        else:
            print "Empty"

    def executemlacode(self):
        self.clearlineformat(30)
        self.consoletext.setText("")
        code = self.mlecode.toPlainText()
        if code:
            code = unicode(code)
            code = code.encode('utf_8')
            code = code.split('\n')
            self.executeThread = ExecuteThread(self, code)
            self.executeThread.getinput.connect(self.getinput)
            self.executeThread.lists.connect(self.showlists)
            self.executeThread.error.connect(self.setErrorLineFormat)
            self.executeThread.start()
        else:
            print "Empty"

    def getinput(self):
        val, ok = QtGui.QInputDialog.getInt(self, 'Input Dialog',
                                            'What is the value of N?')
        if ok:
            queue.put(val)
        else:
            queue.put(False)


    def showlists(self, memlist, stacklist):
        self.showmemlist(memlist)
        self.showstacklist(stacklist)

    def showmemlist(self, stack):
        self.memlist.clear()
        for x, item in enumerate(stack):
            self.memlist.addItem(str(x) + ": " + str(item))

    def showstacklist(self, stack):
        self.stacklist.clear()
        for x, item in enumerate(stack):
            self.stacklist.addItem(str(x) + ": " + str(item))

    def executestepcode(self):
        self.clearlineformat(30)
        code = self.mlecode.toPlainText()
        if code:
            code = unicode(code)
            code = code.encode('utf_8')
            code = code.split('\n')
            self.assember = AssemBER.Instance()
            self.assember.clear()
            self.assember.loadcodetomem(code)
            self.showmemlist(self.assember.memory_stack)
            self.showstacklist(self.assember.stack_register)
            self.stepbtn.setEnabled(True)
            self.startover.setEnabled(True)
            self.executestepbtn.setEnabled(False)
        else:
            print "empty"

    def dostep(self):
        self.clearlineformat(30)
        self.setLineFormat(self.currentline)
        line = self.assember.execute_line(self.currentline, self)
        if line:
            if type(line) is int:
                self.currentline = line
            self.currentline += 1
        elif line is None:
            self.stepbtn.setEnabled(False)
        else:
            print "at line", self.currentline + 1
            self.setErrorLineFormat(self.currentline)
            self.stepbtn.setEnabled(False)
        self.showmemlist(self.assember.memory_stack)
        self.showstacklist(self.assember.stack_register)

    def restartexecute(self):
        self.clearlineformat(self.currentline)
        self.currentline = 0
        self.stepbtn.setEnabled(False)
        self.executestepbtn.setEnabled(True)
        self.startover.setEnabled(False)

    def clearlineformat(self, endline):
        for x in range(0, endline+1):
            cursor = QtGui.QTextCursor(self.mlecode.document().findBlockByNumber(x))
            cursor.setBlockFormat(self.clearformat)
            cursor = QtGui.QTextCursor(self.asmtextedit.document().findBlockByNumber(x))
            cursor.setBlockFormat(self.clearformat)

    def setLineFormat(self, lineNumber):
        cursor = QtGui.QTextCursor(self.mlecode.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(self.format)
        cursor = QtGui.QTextCursor(self.asmtextedit.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(self.format)

    def setErrorConvFormat(self, lineNumber):
        cursor = QtGui.QTextCursor(self.asmtextedit.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(self.errorformat)

    def setErrorLineFormat(self, lineNumber):
        cursor = QtGui.QTextCursor(self.mlecode.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(self.errorformat)
        cursor = QtGui.QTextCursor(self.asmtextedit.document().findBlockByNumber(lineNumber))
        cursor.setBlockFormat(self.errorformat)


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
                    print "Loaded file from", path
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
    error = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, *args, **kwargs):
        super(ConverterThread, self).__init__(parent)
        self.initcode(*args, **kwargs)

    def initcode(self, code):
        self.code = code

    def run(self):
        assember = AssemBER.Instance()
        result, error = assember.convert(self.code)
        if error:
            self.mlaSignal.emit("")
            self.error.emit(result)
            print "Convertion failed at line", result+1
        else:
            mla = ""
            for x in range(0, len(result)):
                if x == len(result) - 1:
                    mla += result[x]
                else:
                    mla += result[x]+'\n'
            self.mlaSignal.emit(mla)


class ExecuteThread(QtCore.QThread):
    getinput = QtCore.pyqtSignal()
    lists = QtCore.pyqtSignal(list, list)
    error = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, *args, **kwargs):
        super(ExecuteThread, self).__init__(parent)
        self.initcode(*args, **kwargs)

    def initcode(self, code):
        self.code = code

    def run(self):
        assember = AssemBER.Instance()
        error = assember.execute(self.code, self)
        if error:
            self.error.emit(error)
        self.lists.emit(assember.memory_stack, assember.stack_register)

app = QtGui.QApplication(sys.argv)
form = AssemberWindow()
form.show()
app.exec_()
