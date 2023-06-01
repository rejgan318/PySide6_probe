"""
[Using QProcess to run external programs](https://www.pythonguis.com/tutorials/pyqt6-qprocess-external-programs/)
"""
import sys

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                               QVBoxLayout, QWidget)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.btn_exec = QPushButton("Execute")
        self.btn_exec.pressed.connect(self.start_process)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        lav = QVBoxLayout()
        lav.addWidget(self.btn_exec)
        lav.addWidget(self.text)

        main_widget = QWidget()
        main_widget.setLayout(lav)
        self.setCentralWidget(main_widget)

    def write_message(self, text):
        self.text.appendPlainText(text)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        self.write_message(data.data().decode("utf-8"))

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        self.write_message(data.data().decode("utf-8"))

    def handle_state(self, state):
        states = {
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running',
        }
        state_name = states[state]
        self.write_message(f"State changed: {state_name}")

    def start_process(self):
        self.process = QProcess()
        self.write_message("Process started")
        self.process.finished.connect(self.process_finished)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.stateChanged.connect(self.handle_state)
        self.process.start("python", ['process_probe_dummy.py'])

    def process_finished(self):
        self.write_message("Process finished")
        # self.process.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
