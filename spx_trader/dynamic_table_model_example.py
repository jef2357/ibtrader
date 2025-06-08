import sys
from PySide6.QtCore import Qt, QAbstractTableModel, QTimer
from PySide6.QtWidgets import QApplication, QTableView, QMainWindow
import random


class DynamicTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data  # 2D list to hold table data

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

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole])
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def updateData(self, row, col, new_value):
        """Custom method to update data dynamically."""
        index = self.index(row, col)
        self.setData(index, new_value, Qt.EditRole)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Data Updates Example")

        # Initial data
        self.data = [
            [random.randint(1, 100) for _ in range(5)]
            for _ in range(5)
        ]

        # Create the model
        self.model = DynamicTableModel(self.data)

        # Create the table view
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.setCentralWidget(self.table_view)

        # Set up a timer to update data dynamically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_random_cell)
        self.timer.start(1000)  # Update every 1000 ms (1 second)

    def update_random_cell(self):
        """Randomly update a cell in the table."""
        row = random.randint(0, len(self.data) - 1)
        col = random.randint(0, len(self.data[0]) - 1)
        new_value = random.randint(1, 100)

        self.model.updateData(row, col, new_value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


"""
Here’s an example of a QAbstractItemModel implementation for a QTableView that supports dynamic data updates. This example demonstrates how data in the model can be dynamically updated and reflected in the QTableView in real time.
Key Features of This Example:

    Dynamic Data Updates:
        The updateData method in the DynamicTableModel class is used to update a specific cell in the model dynamically.
        When data is updated, the dataChanged signal is emitted, ensuring the QTableView reflects the changes in real time.

    Editable Table:
        The flags method allows cells to be editable, enabling manual changes to the data through the UI.

    Real-Time Updates with QTimer:
        A QTimer is set up to periodically update a random cell in the table with a new random value every second.

    Random Data Generation:
        Random integers are used to populate the table initially and to update cells dynamically.

How It Works:

    When the application starts, the table is populated with random integers.
    Every second, a random cell is selected and updated with a new random value.
    The QTableView reflects these updates in real time because the dataChanged signal is emitted.

You can extend this example to handle more complex dynamic updates, such as fetching data from an API or responding to user actions.
"""