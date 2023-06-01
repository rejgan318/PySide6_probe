"""
from [pythonGUIs: The ModelView Architecture](https://www.pythonguis.com/tutorials/pyqt6-modelview-architecture/)
"""
import sys
import time
import traceback

from PySide6.QtCore import QObject, QRunnable, Signal, Slot, QThreadPool, QTimer
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QVBoxLayout, QWidget


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished No data
    error tuple (exctype, value, traceback.format_exc() )
    result object data returned from processing, anything
    progress int indicating % progress
    """
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    """
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        """ Initialise the runner function with passed args, kwargs """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        layout = QVBoxLayout()

        self.lbl_timer_demo = QLabel("Timer timer has not started yet yed")
        btn_RunLongTask = QPushButton("Run long task")
        btn_RunLongTask.pressed.connect(self.prepare_and_start_task)

        layout.addWidget(self.lbl_timer_demo)
        layout.addWidget(btn_RunLongTask)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.show()

        self.threadpool = QThreadPool()
        print(f"Multithreading with maximum {self.threadpool.maxThreadCount()} threads")

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def my_long_task(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n * 100 / 4)

        return "Done."

    def fn_signal_result(self, s):
        print(s)

    def fn_signal_finished(self):
        print("THREAD COMPLETE!")

    def fn_signal_progress(self, n):
        print("%d%% done" % n)

    def prepare_and_start_task(self):
        # Pass the function to execute
        worker = Worker(self.my_long_task)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.fn_signal_result)
        worker.signals.finished.connect(self.fn_signal_finished)
        worker.signals.progress.connect(self.fn_signal_progress)

        # Execute
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.lbl_timer_demo.setText("Counter: %d" % self.counter)


app = QApplication([])
window = MainWindow()
app.exec()
