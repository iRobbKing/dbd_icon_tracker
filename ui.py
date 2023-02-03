import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel

import bot


class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(tuple)

    def run(self):
        statuses = bot.prepare_templates()

        while True:
            self.progress.emit(tuple(bot.get_survivors_statuses(statuses)))

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

    def reportProgress(self, survivors_info):
        def format_state(state):
            return state.replace('_', ' ') if state is not None else 'unknown'

        def format_action(action):
            return action.replace('_', ' ') if action is not None else 'doing nothing'

        formatted_state = [format_state(survivor_info['state']) for survivor_info in survivors_info]
        formatted_action = [format_action(survivor_info['action']) for survivor_info in survivors_info]
        formatted_info = '\n'.join(
            (f'"{state}", is {action}' for state, action in  zip(formatted_state, formatted_action))
        )
        self.label.setText(formatted_info)

    def mousePressEvent(self, _):
        QApplication.quit()


def run_ui():
    app = QApplication(sys.argv)
    mywindow = MainWindow()
    mywindow.show()
    app.exec()
