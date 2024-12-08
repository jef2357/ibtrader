# using pyside 6, create a qt main winodow from a .ui file


import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        file = QFile("db_browser_main_ui.ui")
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
