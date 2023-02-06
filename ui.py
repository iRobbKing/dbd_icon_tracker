import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

import bot


class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(list)

    def run(self):
        hud_tracker = bot.match_survivors_state()

        while True:
            self.progress.emit(hud_tracker())

        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )

        self.setGeometry(0, 0, 300, 80)

        self.label = QLabel()
        self.setCentralWidget(self.label)

        self.runTrakerTask()

    def runTrakerTask(self):
        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()

    def reportProgress(self, survivors_info):
        self.label.setText(str(survivors_info)
                           .replace('], ', '\n')
                           .replace('[', '')
                           .replace(']', '')
                           .replace('None', ' '*50))

    def mousePressEvent(self, _):
        QApplication.quit()


def run_ui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
