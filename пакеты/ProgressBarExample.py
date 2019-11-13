from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time


class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)

    def run(self):
        cnt = 0
        for i in range(11):
            cnt = i
            time.sleep(0.3)
            self.change_value.emit(cnt)


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 ProgressBar"
        self.top = 200
        self.left = 500
        self.width = 300
        self.height = 100
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(10)
        # self.progressbar.setMaximum(100)
        self.progressbar.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}"
                                       "QProgressBar::chunk {background:yellow}")
        vbox.addWidget(self.progressbar)
        self.button = QPushButton("Start Progressbar")
        self.button.clicked.connect(self.startProgressBar)
        self.button.setStyleSheet('background-color:yellow')
        vbox.addWidget(self.button)
        self.setLayout(vbox)
        self.show()

    def startProgressBar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()

    def setProgressVal(self, val):
        self.progressbar.setValue(val)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())