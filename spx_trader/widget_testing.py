from PySide6.QtWidgets import QApplication, QTableView, QStyledItemDelegate, QPushButton, QStyleOptionButton, QStyle
from PySide6.QtCore import Qt, QModelIndex, QRect, QAbstractTableModel
import sys

class PushButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons = {}

    def paint(self, painter, option, index):
        # Create and configure the button
        button = QStyleOptionButton()
        button.rect = option.rect
        button.text = "Action"
        button.state = QStyle.State_Enabled         

        # Draw the button in the cell
        QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)

    def editorEvent(self, event, model, option, index):
        # Detect button click
        if event.type() == event.MouseButtonRelease:
            if option.rect.contains(event.pos()):
                # Perform the action for the button
                print(f"Button clicked in row {index.row()}, column {index.column()}")
                return True
        return False


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

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            if orientation == Qt.Vertical:
                return str(section + 1)
        return None


if __name__ == "__main__":
    app = QApplication([])

    # Sample data
    headers = ["Name", "Age", "Action"]
    data = [
        ["Alice", 30, ""],
        ["Bob", 25, ""],
        ["Charlie", 35, ""],
    ]

    # Create the model and view
    model = CustomTableModel(data, headers)
    table_view = QTableView()
    table_view.setModel(model)

    # Assign the delegate to the "Action" column
    delegate = PushButtonDelegate(table_view)
    table_view.setItemDelegateForColumn(2, delegate)

    # Customize the table view
    table_view.setWindowTitle("Table with Push Buttons")
    table_view.resize(600, 300)
    table_view.show()

    app.exec()
    #sys.exit(app.exec())
