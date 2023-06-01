import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from simple import Ui_MainWindow
from simple_process import simple_go

# Import compiled qrc file (themes.qrc -> themes.py for example)
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

    # My custom stylesheet for special widgets with qss_class property "yellow". WIll be added to qss file
    my_qss = """
        *[qss_class="yellow"] { background-color: yellow; }
        """
    # Demo two variants for adding extra stylesheet to app. Setup True or False in next line
    READ_FROM_FILE = True
    if READ_FROM_FILE:
        # Read qss from file os
        with open("qss/AMOLED.qss", 'r') as file:
            qss = file.read()
    else:
        # Read qss from resource qrc file. Must be import compiled qrc file (themes.qrc -> themes.py for example)
        qss_file = QFile(":temes/qss/AMOLED.qss")
        qss_file.open(QFile.ReadOnly | QFile.Text)
        qss = qss_file.readAll().data().decode("utf-8")

    app.setStyleSheet(qss + my_qss) # my_qss second!

    window = MainWindow()
    window.show()
    app.exec()
