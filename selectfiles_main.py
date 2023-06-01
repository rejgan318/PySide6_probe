import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PySide6.QtGui import QIcon, QImage, QPixmap, QBrush
from PySide6 import QtCore
from selectfiles import Ui_MainWindow


class MyFiles(QtCore.QAbstractListModel):
    def __init__(self, *args, files=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.files = files or []
        # self.files.extend(["111", "222", "333"])

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            file_name = self.files[index.row()]
            return Path(file_name).name

        if role == QtCore.Qt.DecorationRole:
            file_name = self.files[index.row()]
            if Path(file_name).suffix in [".jpg", ".png"]:
                return QIcon(file_name)

    def rowCount(self, index):
        return len(self.files)


class SelectFiles:
    """
    Класс нужен только для того, чтобы при следующем вызове сохранялась директория и режим выбора файлов
    """
    def __init__(self, parent_widget):
        # self.parent_widget = parent_widget
        self.mask_files = ["'Image File (*.png *.jpg)",
                           "All Files (*.*)"]
        self.selectedFilter = self.mask_files[1]
        self.dir_files = str(Path.cwd())    # start directory

    def select_files(self):
        response = QFileDialog.getOpenFileNames(
            # parent=self.parent_widget,
            caption="Select images",
            dir=self.dir_files,
            filter=";;".join(self.mask_files),
            selectedFilter=self.selectedFilter)
        self.selectedFilter = response[1]
        if response[0]:
            self.dir_files = str(Path(response[0][0]).parent)   # save selected directory for next select
            return response[0]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.model = MyFiles()
        self.liv_2.setModel(self.model)

        self.select_files_dialog = SelectFiles(self)
        self.pbt_select.clicked.connect(self.add_files)

    def add_files(self):
        added_files = self.select_files_dialog.select_files()
        if added_files:
            self.model.files.extend(added_files)
            self.model.layoutChanged.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
