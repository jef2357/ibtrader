# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow
# from positions_table_ui import Ui_MainWindow  # Import the generated Python class

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)  # Set up the UI in the main window

#         # Example: Connect a button click to a function
#         #self.ui.pushButton.clicked.connect(self.handle_button_click)

#     #def handle_button_click(self):
#         #print("Button clicked!")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())



from PySide6.QtWidgets import QApplication, QTableView
from PySide6.QtCore import Qt, QAbstractTableModel


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:  # Column headers
                return self._headers[section]
            if orientation == Qt.Vertical:  # Row headers
                return str(section + 1)
        return None


if __name__ == "__main__":
    app = QApplication([])

    # Sample data
    headers = ["Name", "Age", "Occupation", "test1", "test2", "test3"]
    data = [
        ["Test 1","","","",""],
        ["Alice", 30, "Engineer", "test1", "test2", "test3"],
        ["Bob", 25, "Designer", "test1", "test2", "test3"],
        ["Charlie", 35, "Teacher", "test1", "test2", "test3"],
        ["David", 28, "Artist", "test1", "test2", "test3"],
        ["Eve", 22, "Scientist", "test1", "test2", "test3"],
        ["Frank", 40, "Manager", "test1", "test2", "test3"],
        ["Grace", 29, "Developer", "test1", "test2", "test3"],
        ["Heidi", 33, "Analyst", "test1", "test2", "test3"],
        ["Ivan", 27, "Consultant", "test1", "test2", "test3"],
        ["Judy", 31, "Architect", "test1", "test2", "test3"],
        ["Karl", 26, "Sales", "test1", "test2", "test3"],
        ["Leo", 34, "Marketing", "test1", "test2", "test3"],
        ["Mallory", 32, "HR", "test1", "test2", "test3"],
        ["Nina", 36, "Finance", "test1", "test2", "test3"],
        ["Oscar", 38, "Operations", "test1", "test2", "test3"],
        ["Peggy", 39, "Support", "test1", "test2", "test3"],
        ["Quentin", 41, "Researcher", "test1", "test2", "test3"],
        ["Rupert", 42, "Data Scientist", "test1", "test2", "test3"],
        ["Sybil", 43, "Product Manager", "test1", "test2", "test3"],
        ["Trent", 44, "Business Analyst", "test1", "test2", "test3"],
        ["Uma", 45, "Quality Assurance", "test1", "test2", "test3"],
        ["Victor", 46, "System Administrator", "test1", "test2", "test3"],
        ["Walter", 47, "Network Engineer", "test1", "test2", "test3"],
        ["Xena", 48, "Web Developer", "test1", "test2", "test3"]
    ]

    # Create a model and view
    model = CustomTableModel(data, headers)
    table_view = QTableView()
    table_view.setModel(model)

    # Customize the table view
    table_view.setWindowTitle("PySide6 Table Model and View Example")
    table_view.resize(600, 300)
    table_view.show()

    app.exec()