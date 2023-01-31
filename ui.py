import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

import bot


class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(tuple)

    def run(self):
        states, actions = bot.prepair_templates()

        while True:
            self.progress.emit(tuple(bot.read_survivor_statuses(states, actions)))

        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.X11BypassWindowManagerHint
        )

        self.setGeometry(0, 0, 160, 80)

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

    def reportProgress(self, result):
        def map_state(state):
            return state.replace('_', ' ') if state != None else 'healthy'

        def map_action(action):
            return action.replace('_', ' ') if action != None else 'doing nothing'

        def format_status(status):
            state, action = status
            return f'"{map_state(state)}", is {map_action(action)}'

        formatted_statuses = map(format_status, result)
        formatted_result = '\n'.join(formatted_statuses)
        self.label.setText(formatted_result)

    def mousePressEvent(self, _):
        QApplication.quit()


def run_ui():
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec()
