from spx_trader_fixed_layout import Ui_spx_trader_main_window
from PySide6.QtWidgets import QMessageBox, QLabel
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QAbstractTableModel, QRunnable, QThreadPool

from client_spx_trader import spxTraderClient
from wrapper_spx_trader import spxTraderWrapper
from database_spx_trader import spxTraderDBConn
from ibapi.client import EClient
import psycopg          





class PositionsTableModel(QAbstractTableModel):
    def __init__(self, db_conn=None):
        super().__init__()
        self.db_conn = db_conn
        self._data = [["", "", "", "", "", "", "", ""]]
        self._headers = ["qty", "symbol", "exp", "P/C", "strike", "cost", "price", "+/-"]


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
    
class positionsWorker(QRunnable):
    def __init__(self):
        self.model = PositionsTableModel()
        self.updated_flag = None

    def run(self):
        pass
        

class spxTraderMainWindow(QMainWindow, Ui_spx_trader_main_window): 
    def __init__(self, trader: spxTraderClient):
        super().__init__()
        self.trader = trader
        self.positions = positionsWorker()
        
        self.db_config = {'user':'jeffrey',
                 'password':'strawberries',
                 'host':'127.0.0.1',
                 'port':'5432',
                 'dbname':'trader_today',
                 'autocommit':True} #this resolve the problem "InternalError: CREATE DATABASE cannot run inside a transaction block"
        self.db_conn = psycopg.connect(**self.db_config)
        self.db_cur = self.db_conn.cursor()

        self.threadpool = QThreadPool()

        self.setupUi(self)      
        self.add_cfg()

    def add_cfg(self):
        #self.statusBar().showMessage("Ready")
        self.connect_action.triggered.connect(self.connect)
        self.disconnect_action.triggered.connect(self.disconnect)

        self.status_label = QLabel("SPX Trader")
        self.statusBar().addWidget(self.status_label)

        self.positions_button.clicked.connect(self.get_positions)

        self.positions_table.setModel(self.positions.model)
    
    def connect(self):
        if self.trader.connState is not EClient.CONNECTED:
            self.trader.connect("127.0.0.1", 7496, clientId=1)

        while self.trader.connState is not EClient.CONNECTED:
            pass
        

        #self.statusBar().showMessage("Connected")
        self.status_label.setText("Connected")

    def disconnect(self):
        # QMessageBox.information(
        #     self,
        #     "Disconnection Status",
        #     "Successfully disconnected from the trader!",
        #     QMessageBox.Ok
        # )
        
        self.status_label.setText("Disconnecting")
        self.trader.disconnect()
        self.status_label.setText("Disconnected")

    def get_positions(self):
        # Example: Fetch positions from the trader and update the UI
        req_id = self.trader.get_req_id()
        self.trader.reqPositions(req_id)

        self.positions_table.resizeColumnsToContents()

        # TODO:
        #    add a connection check before sending the request


    def closeEvent(self, event):
        # Code to execute before the window closes
        
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            print("Window is closing...")
            # Accept the event to proceed with closing
            self.status_label.setText("Disconnecting")
            self.disconnect()
            self.status_label.setText("Disconnected")

            while self.trader.connState is not EClient.DISCONNECTED:
                pass

            event.accept()
        else:
            print("Window close canceled.")
            # Ignore the event to prevent closing
            event.ignore()
