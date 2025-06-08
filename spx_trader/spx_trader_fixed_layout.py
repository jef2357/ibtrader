# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spx_trader_fixed_layoutMkgLwo.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_spx_trader_main_window(object):
    def setupUi(self, spx_trader_main_window):
        if not spx_trader_main_window.objectName():
            spx_trader_main_window.setObjectName(u"spx_trader_main_window")
        spx_trader_main_window.resize(1080, 917)
        self.connect_action = QAction(spx_trader_main_window)
        self.connect_action.setObjectName(u"connect_action")
        self.accounts_action = QAction(spx_trader_main_window)
        self.accounts_action.setObjectName(u"accounts_action")
        self.disconnect_action = QAction(spx_trader_main_window)
        self.disconnect_action.setObjectName(u"disconnect_action")
        self.centralwidget = QWidget(spx_trader_main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_7 = QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.data_layout = QVBoxLayout()
        self.data_layout.setObjectName(u"data_layout")
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.buttons_spacer_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(self.buttons_spacer_1)

        self.positions_button = QPushButton(self.centralwidget)
        self.positions_button.setObjectName(u"positions_button")

        self.buttons_layout.addWidget(self.positions_button)

        self.pushbutton_1 = QPushButton(self.centralwidget)
        self.pushbutton_1.setObjectName(u"pushbutton_1")

        self.buttons_layout.addWidget(self.pushbutton_1)

        self.buttons_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(self.buttons_spacer_2)


        self.data_layout.addLayout(self.buttons_layout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.data_layout.addWidget(self.line)

        self.tables_layout = QHBoxLayout()
        self.tables_layout.setObjectName(u"tables_layout")
        self.positions_layout = QVBoxLayout()
        self.positions_layout.setObjectName(u"positions_layout")
        self.positions_label_layout = QHBoxLayout()
        self.positions_label_layout.setObjectName(u"positions_label_layout")
        self.positions_label_spacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.positions_label_layout.addItem(self.positions_label_spacer_2)

        self.positions_label = QLabel(self.centralwidget)
        self.positions_label.setObjectName(u"positions_label")

        self.positions_label_layout.addWidget(self.positions_label)

        self.positions_label_spacer_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.positions_label_layout.addItem(self.positions_label_spacer_1)


        self.positions_layout.addLayout(self.positions_label_layout)

        self.positions_frame = QFrame(self.centralwidget)
        self.positions_frame.setObjectName(u"positions_frame")
        self.positions_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.positions_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.positions_frame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.positions_table = QTableView(self.positions_frame)
        self.positions_table.setObjectName(u"positions_table")

        self.gridLayout_5.addWidget(self.positions_table, 0, 0, 1, 1)


        self.positions_layout.addWidget(self.positions_frame)


        self.tables_layout.addLayout(self.positions_layout)

        self.tables_spacer = QSpacerItem(13, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.tables_layout.addItem(self.tables_spacer)

        self.chain_layout = QVBoxLayout()
        self.chain_layout.setObjectName(u"chain_layout")
        self.chain_label_layout = QHBoxLayout()
        self.chain_label_layout.setObjectName(u"chain_label_layout")
        self.chain_label_spacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.chain_label_layout.addItem(self.chain_label_spacer_2)

        self.chain_label = QLabel(self.centralwidget)
        self.chain_label.setObjectName(u"chain_label")

        self.chain_label_layout.addWidget(self.chain_label)

        self.chain_label_spacer_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.chain_label_layout.addItem(self.chain_label_spacer_1)


        self.chain_layout.addLayout(self.chain_label_layout)

        self.chain_frame = QFrame(self.centralwidget)
        self.chain_frame.setObjectName(u"chain_frame")
        self.chain_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.chain_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.chain_frame)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.chain_table = QTableView(self.chain_frame)
        self.chain_table.setObjectName(u"chain_table")

        self.gridLayout_6.addWidget(self.chain_table, 0, 0, 1, 1)


        self.chain_layout.addWidget(self.chain_frame)


        self.tables_layout.addLayout(self.chain_layout)


        self.data_layout.addLayout(self.tables_layout)

        self.trades_layout = QVBoxLayout()
        self.trades_layout.setObjectName(u"trades_layout")
        self.trades_label_layout = QHBoxLayout()
        self.trades_label_layout.setObjectName(u"trades_label_layout")
        self.trades_label_spacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.trades_label_layout.addItem(self.trades_label_spacer_2)

        self.trades_label = QLabel(self.centralwidget)
        self.trades_label.setObjectName(u"trades_label")

        self.trades_label_layout.addWidget(self.trades_label)

        self.trades_label_spacer_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.trades_label_layout.addItem(self.trades_label_spacer_1)


        self.trades_layout.addLayout(self.trades_label_layout)

        self.trades_frame = QFrame(self.centralwidget)
        self.trades_frame.setObjectName(u"trades_frame")
        self.trades_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.trades_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.trades_frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.trades_table = QTableView(self.trades_frame)
        self.trades_table.setObjectName(u"trades_table")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trades_table.sizePolicy().hasHeightForWidth())
        self.trades_table.setSizePolicy(sizePolicy)
        self.trades_table.setMinimumSize(QSize(0, 200))
        self.trades_table.setMaximumSize(QSize(16777215, 200))

        self.gridLayout_4.addWidget(self.trades_table, 0, 0, 1, 1)


        self.trades_layout.addWidget(self.trades_frame)


        self.data_layout.addLayout(self.trades_layout)


        self.horizontalLayout.addLayout(self.data_layout)

        self.plots_layout = QVBoxLayout()
        self.plots_layout.setObjectName(u"plots_layout")
        self.plot_1_frame = QFrame(self.centralwidget)
        self.plot_1_frame.setObjectName(u"plot_1_frame")
        self.plot_1_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_1_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.plot_1_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.plot_1_widget = QWidget(self.plot_1_frame)
        self.plot_1_widget.setObjectName(u"plot_1_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plot_1_widget.sizePolicy().hasHeightForWidth())
        self.plot_1_widget.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.plot_1_widget, 0, 0, 1, 1)


        self.plots_layout.addWidget(self.plot_1_frame)

        self.plot_2_frame = QFrame(self.centralwidget)
        self.plot_2_frame.setObjectName(u"plot_2_frame")
        self.plot_2_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_2_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.plot_2_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.plot_2_widget = QWidget(self.plot_2_frame)
        self.plot_2_widget.setObjectName(u"plot_2_widget")
        sizePolicy1.setHeightForWidth(self.plot_2_widget.sizePolicy().hasHeightForWidth())
        self.plot_2_widget.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.plot_2_widget, 0, 0, 1, 1)


        self.plots_layout.addWidget(self.plot_2_frame)

        self.plot_3_frame = QFrame(self.centralwidget)
        self.plot_3_frame.setObjectName(u"plot_3_frame")
        self.plot_3_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_3_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.plot_3_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plot_3_widget = QWidget(self.plot_3_frame)
        self.plot_3_widget.setObjectName(u"plot_3_widget")
        sizePolicy1.setHeightForWidth(self.plot_3_widget.sizePolicy().hasHeightForWidth())
        self.plot_3_widget.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.plot_3_widget, 0, 0, 1, 1)


        self.plots_layout.addWidget(self.plot_3_frame)


        self.horizontalLayout.addLayout(self.plots_layout)


        self.gridLayout_7.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        spx_trader_main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(spx_trader_main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1080, 22))
        self.menuMenu1 = QMenu(self.menubar)
        self.menuMenu1.setObjectName(u"menuMenu1")
        spx_trader_main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(spx_trader_main_window)
        self.statusbar.setObjectName(u"statusbar")
        spx_trader_main_window.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu1.menuAction())
        self.menuMenu1.addAction(self.connect_action)
        self.menuMenu1.addAction(self.disconnect_action)

        self.retranslateUi(spx_trader_main_window)

        QMetaObject.connectSlotsByName(spx_trader_main_window)
    # setupUi

    def retranslateUi(self, spx_trader_main_window):
        spx_trader_main_window.setWindowTitle(QCoreApplication.translate("spx_trader_main_window", u"MainWindow", None))
        self.connect_action.setText(QCoreApplication.translate("spx_trader_main_window", u"Connect", None))
        self.accounts_action.setText(QCoreApplication.translate("spx_trader_main_window", u"Accounts", None))
        self.disconnect_action.setText(QCoreApplication.translate("spx_trader_main_window", u"Disconnect", None))
        self.positions_button.setText(QCoreApplication.translate("spx_trader_main_window", u"Positions", None))
        self.pushbutton_1.setText(QCoreApplication.translate("spx_trader_main_window", u"PushButton", None))
        self.positions_label.setText(QCoreApplication.translate("spx_trader_main_window", u"Positions", None))
        self.chain_label.setText(QCoreApplication.translate("spx_trader_main_window", u"Chain", None))
        self.trades_label.setText(QCoreApplication.translate("spx_trader_main_window", u"Trades", None))
        self.menuMenu1.setTitle(QCoreApplication.translate("spx_trader_main_window", u"Actions", None))
    # retranslateUi

