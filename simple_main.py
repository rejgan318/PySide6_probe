import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from simple import Ui_MainWindow
from simple_process import simple_go

import themes

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_process.clicked.connect(self.btn_process_clicked)
        self.ui.lbl_output.setProperty("qss_class", "yellow")

    def btn_process_clicked(self):
        text = self.ui.led_input.text()
        result = simple_go(text)
        print(f"Получено {result}")
        self.ui.lbl_output.setText(result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_qss = """
        *[qss_class="yellow"] { background-color: yellow; }
        """
    # Optional 1: Read qss from file

    with open("qss/AMOLED.qss", 'r') as file:
        qss = file.read()
        app.setStyleSheet(qss + my_qss)

    # Optional 2: Read qss from resource file

    qss_file = QFile(":temes/qss/AMOLED.qss")
    qss_file.open(QFile.ReadOnly | QFile.Text)
    qss = qss_file.readAll().data().decode("utf-8")
    app.setStyleSheet(qss + my_qss)

    # app.setStyleSheet("""
    #     # * {
    #     #     font-size: 20px;
    #     #     background-color: red;
    #     # }
    #     *[qss_class="yellow"] { background-color: yellow; }
    # """)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
