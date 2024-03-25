import sys
import download
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)


class LogsCls(QtWidgets.QDockWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.LogEdit = QtWidgets.QTextEdit(readOnly=True)
        self.setWidget(self.LogEdit)

    def log(self, s, color='black'):
        self.LogEdit.append(f'<div style="color:{color}">{s}</div>')

class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        iconName = 'icon.png'
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.resize(900, 600)
        self.infoGroupBox = QtWidgets.QGroupBox("Pirate Bocuse")
        self.usernameEdit = QtWidgets.QLineEdit()
        self.passwordEdit = QtWidgets.QLineEdit()
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.urlsEdit = QtWidgets.QPlainTextEdit()
        self.createForm()
        self.button = QtWidgets.QPushButton('Start download', self)
        self.button.clicked.connect(self.startDownload)
        self.button1 = QtWidgets.QPushButton('Download in process', self)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.infoGroupBox)
        self.mainLayout.addWidget(self.button)
        self.centralWidget.setLayout(self.mainLayout)
        self.Logs = LogsCls('Bocuse Logs')
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.Logs)
        self.Threadpool = QThreadPool()

    def threadDownload(self, login, password, urls, Logs):
        self.mainLayout.removeWidget(self.button)
        self.mainLayout.addWidget(self.button1)
        download.download(login, password, urls, Logs)
        self.mainLayout.removeWidget(self.button1)
        self.mainLayout.addWidget(self.button)



    def startDownload(self):
        login = self.usernameEdit.text()
        password = self.passwordEdit.text()
        urls = self.urlsEdit.toPlainText().split('\n')
        if not login or not password:
            self.Logs.log("Login or Password is empty.\n Make sure all fields"\
                    " are filled and try again", 'red')
            return
        empty = True
        for url in urls:
            if url:
                empty = False
        if empty:
            self.Logs.log("No video links provided. Nothing to do.")
            return
        worker = Worker(self.threadDownload, login, password, urls, self.Logs)
        self.Threadpool.start(worker)



    def createForm(self):
        # creating a form layout
        layout = QtWidgets.QFormLayout()
        # adding rows
        layout.addRow(QtWidgets.QLabel("Login"), self.usernameEdit)
        layout.addRow(QtWidgets.QLabel("Password"), self.passwordEdit)
        layout.addRow(QtWidgets.QLabel("Video URLs"), self.urlsEdit)
        # setting layout
        self.infoGroupBox.setLayout(layout)




if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    w.Logs.log("""This is a paragraph.""", 'brown')
    w.Logs.log('asdasdf', 'green')
    print(w.Logs)
    sys.exit(app.exec_())

