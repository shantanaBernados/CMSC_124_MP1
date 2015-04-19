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
        self.convertasm.clicked.connect(self.convertasmcode)
        self.executemle.clicked.connect(self.executemlacode)
        self.asmtextedit.installEventFilter(QAsmEditDropHandler(self))
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
            print val
            queue.put(val)
        # pass


class QAsmEditDropHandler(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.DragEnter:
            # we need to accept this event explicitly to be able to receive QDropEvents!
            data = event.mimeData()
            urls = data.urls()
            print urls[0].scheme()
            if (urls and urls[0].scheme() == 'file'):
                event.accept()
                return True
                # e.accept()

        if event.type() == QtCore.QEvent.DragMove:
            data = event.mimeData()
            urls = data.urls()
            if (urls and urls[0].scheme() == 'file'):
                event.accept()
                return True

        if event.type() == QtCore.QEvent.Drop:
            print "drop"
            data = event.mimeData()
            urls = data.urls()
            if (urls and urls[0].scheme() == 'file'):
                # for some reason, this doubles up the intro slash
                # filepath = urls[0].toString()
                path = urls[0].toLocalFile().toLocal8Bit().data()
                # if os.path.isfile(path):
                print "path", path
                obj.setText(path)
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
        print code

    def run(self):
        assember = AssemBER.Instance()
        result = assember.convert(self.code)
        mla = ""
        for line in result:
            mla += line+'\n'
        self.mlaSignal.emit(mla)


class ExecuteThread(QtCore.QThread):
    getinput = QtCore.pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(ExecuteThread, self).__init__(parent)
        self.initcode(*args, **kwargs)

    def initcode(self, code):
        self.code = code
        print code

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
