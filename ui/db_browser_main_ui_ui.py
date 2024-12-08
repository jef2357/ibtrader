# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'db_browser_main_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_db_browser_main(object):
    def setupUi(self, db_browser_main):
        if not db_browser_main.objectName():
            db_browser_main.setObjectName(u"db_browser_main")
        db_browser_main.resize(1022, 1000)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(db_browser_main.sizePolicy().hasHeightForWidth())
        db_browser_main.setSizePolicy(sizePolicy)
        db_browser_main.setMinimumSize(QSize(800, 1000))
        self.centralwidget = QWidget(db_browser_main)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.data_info_layout = QHBoxLayout()
        self.data_info_layout.setObjectName(u"data_info_layout")
        self.data_selection_frame = QFrame(self.centralwidget)
        self.data_selection_frame.setObjectName(u"data_selection_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.data_selection_frame.sizePolicy().hasHeightForWidth())
        self.data_selection_frame.setSizePolicy(sizePolicy2)
        self.data_selection_frame.setFrameShape(QFrame.Shape.Box)
        self.data_selection_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout_5 = QVBoxLayout(self.data_selection_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.date_horizontalLayout = QHBoxLayout()
        self.date_horizontalLayout.setObjectName(u"date_horizontalLayout")
        self.date_label = QLabel(self.data_selection_frame)
        self.date_label.setObjectName(u"date_label")
        sizePolicy2.setHeightForWidth(self.date_label.sizePolicy().hasHeightForWidth())
        self.date_label.setSizePolicy(sizePolicy2)
        self.date_label.setMinimumSize(QSize(100, 30))

        self.date_horizontalLayout.addWidget(self.date_label)

        self.date_combobox = QComboBox(self.data_selection_frame)
        self.date_combobox.setObjectName(u"date_combobox")
        sizePolicy2.setHeightForWidth(self.date_combobox.sizePolicy().hasHeightForWidth())
        self.date_combobox.setSizePolicy(sizePolicy2)
        self.date_combobox.setMinimumSize(QSize(100, 30))

        self.date_horizontalLayout.addWidget(self.date_combobox)


        self.verticalLayout_5.addLayout(self.date_horizontalLayout)

        self.symbol_horizontalLayout_2 = QHBoxLayout()
        self.symbol_horizontalLayout_2.setObjectName(u"symbol_horizontalLayout_2")
        self.symbol_label = QLabel(self.data_selection_frame)
        self.symbol_label.setObjectName(u"symbol_label")
        sizePolicy2.setHeightForWidth(self.symbol_label.sizePolicy().hasHeightForWidth())
        self.symbol_label.setSizePolicy(sizePolicy2)
        self.symbol_label.setMinimumSize(QSize(100, 30))

        self.symbol_horizontalLayout_2.addWidget(self.symbol_label)

        self.symbol_combobox = QComboBox(self.data_selection_frame)
        self.symbol_combobox.setObjectName(u"symbol_combobox")
        sizePolicy2.setHeightForWidth(self.symbol_combobox.sizePolicy().hasHeightForWidth())
        self.symbol_combobox.setSizePolicy(sizePolicy2)
        self.symbol_combobox.setMinimumSize(QSize(100, 30))

        self.symbol_horizontalLayout_2.addWidget(self.symbol_combobox)


        self.verticalLayout_5.addLayout(self.symbol_horizontalLayout_2)

        self.requestid_horizontalLayout_3 = QHBoxLayout()
        self.requestid_horizontalLayout_3.setObjectName(u"requestid_horizontalLayout_3")
        self.requestid_label = QLabel(self.data_selection_frame)
        self.requestid_label.setObjectName(u"requestid_label")
        sizePolicy2.setHeightForWidth(self.requestid_label.sizePolicy().hasHeightForWidth())
        self.requestid_label.setSizePolicy(sizePolicy2)
        self.requestid_label.setMinimumSize(QSize(100, 30))

        self.requestid_horizontalLayout_3.addWidget(self.requestid_label)

        self.requestod_combobox = QComboBox(self.data_selection_frame)
        self.requestod_combobox.setObjectName(u"requestod_combobox")
        sizePolicy2.setHeightForWidth(self.requestod_combobox.sizePolicy().hasHeightForWidth())
        self.requestod_combobox.setSizePolicy(sizePolicy2)
        self.requestod_combobox.setMinimumSize(QSize(100, 30))

        self.requestid_horizontalLayout_3.addWidget(self.requestod_combobox)


        self.verticalLayout_5.addLayout(self.requestid_horizontalLayout_3)


        self.data_info_layout.addWidget(self.data_selection_frame)

        self.data_status_frame = QFrame(self.centralwidget)
        self.data_status_frame.setObjectName(u"data_status_frame")
        sizePolicy2.setHeightForWidth(self.data_status_frame.sizePolicy().hasHeightForWidth())
        self.data_status_frame.setSizePolicy(sizePolicy2)
        self.data_status_frame.setFrameShape(QFrame.Shape.Box)
        self.data_status_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout = QVBoxLayout(self.data_status_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.live_data_pushbutton = QPushButton(self.data_status_frame)
        self.live_data_pushbutton.setObjectName(u"live_data_pushbutton")
        sizePolicy2.setHeightForWidth(self.live_data_pushbutton.sizePolicy().hasHeightForWidth())
        self.live_data_pushbutton.setSizePolicy(sizePolicy2)
        self.live_data_pushbutton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_7.addWidget(self.live_data_pushbutton)

        self.live_data_label = QLabel(self.data_status_frame)
        self.live_data_label.setObjectName(u"live_data_label")
        sizePolicy2.setHeightForWidth(self.live_data_label.sizePolicy().hasHeightForWidth())
        self.live_data_label.setSizePolicy(sizePolicy2)
        self.live_data_label.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_7.addWidget(self.live_data_label)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.refresh_pushbutton = QPushButton(self.data_status_frame)
        self.refresh_pushbutton.setObjectName(u"refresh_pushbutton")
        sizePolicy2.setHeightForWidth(self.refresh_pushbutton.sizePolicy().hasHeightForWidth())
        self.refresh_pushbutton.setSizePolicy(sizePolicy2)
        self.refresh_pushbutton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_8.addWidget(self.refresh_pushbutton)

        self.refresh_label = QLabel(self.data_status_frame)
        self.refresh_label.setObjectName(u"refresh_label")
        sizePolicy2.setHeightForWidth(self.refresh_label.sizePolicy().hasHeightForWidth())
        self.refresh_label.setSizePolicy(sizePolicy2)
        self.refresh_label.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_8.addWidget(self.refresh_label)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_15 = QPushButton(self.data_status_frame)
        self.pushButton_15.setObjectName(u"pushButton_15")
        sizePolicy2.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy2)
        self.pushButton_15.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_9.addWidget(self.pushButton_15)

        self.label_10 = QLabel(self.data_status_frame)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_9.addWidget(self.label_10)


        self.verticalLayout.addLayout(self.horizontalLayout_9)


        self.data_info_layout.addWidget(self.data_status_frame)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.data_info_layout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.data_info_layout)

        self.data_view_layout = QHBoxLayout()
        self.data_view_layout.setObjectName(u"data_view_layout")
        self.data_layout = QVBoxLayout()
        self.data_layout.setObjectName(u"data_layout")
        self.data_label = QLabel(self.centralwidget)
        self.data_label.setObjectName(u"data_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.data_label.sizePolicy().hasHeightForWidth())
        self.data_label.setSizePolicy(sizePolicy3)
        self.data_label.setMinimumSize(QSize(0, 30))
        self.data_label.setMaximumSize(QSize(16777215, 30))
        self.data_label.setFrameShape(QFrame.Shape.Box)
        self.data_label.setFrameShadow(QFrame.Shadow.Raised)
        self.data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.data_layout.addWidget(self.data_label)

        self.data_tableView = QTableView(self.centralwidget)
        self.data_tableView.setObjectName(u"data_tableView")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.data_tableView.sizePolicy().hasHeightForWidth())
        self.data_tableView.setSizePolicy(sizePolicy4)
        self.data_tableView.setMinimumSize(QSize(200, 0))
        self.data_tableView.setMaximumSize(QSize(200, 16777215))
        self.data_tableView.setFrameShape(QFrame.Shape.Box)
        self.data_tableView.setFrameShadow(QFrame.Shadow.Raised)

        self.data_layout.addWidget(self.data_tableView)


        self.data_view_layout.addLayout(self.data_layout)

        self.data_plot_widget = QWidget(self.centralwidget)
        self.data_plot_widget.setObjectName(u"data_plot_widget")
        sizePolicy1.setHeightForWidth(self.data_plot_widget.sizePolicy().hasHeightForWidth())
        self.data_plot_widget.setSizePolicy(sizePolicy1)

        self.data_view_layout.addWidget(self.data_plot_widget)


        self.verticalLayout_2.addLayout(self.data_view_layout)

        db_browser_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(db_browser_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1022, 22))
        self.menuActions = QMenu(self.menubar)
        self.menuActions.setObjectName(u"menuActions")
        db_browser_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(db_browser_main)
        self.statusbar.setObjectName(u"statusbar")
        db_browser_main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(db_browser_main)

        QMetaObject.connectSlotsByName(db_browser_main)
    # setupUi

    def retranslateUi(self, db_browser_main):
        db_browser_main.setWindowTitle(QCoreApplication.translate("db_browser_main", u"DB Browser", None))
        self.date_label.setText(QCoreApplication.translate("db_browser_main", u"Date", None))
        self.symbol_label.setText(QCoreApplication.translate("db_browser_main", u"Symbol", None))
        self.requestid_label.setText(QCoreApplication.translate("db_browser_main", u"Request ID", None))
        self.live_data_pushbutton.setText(QCoreApplication.translate("db_browser_main", u"LIVE DATA", None))
        self.live_data_label.setText(QCoreApplication.translate("db_browser_main", u"live data status", None))
        self.refresh_pushbutton.setText(QCoreApplication.translate("db_browser_main", u"Refresh", None))
        self.refresh_label.setText(QCoreApplication.translate("db_browser_main", u"data availability", None))
        self.pushButton_15.setText(QCoreApplication.translate("db_browser_main", u"TBD", None))
        self.label_10.setText(QCoreApplication.translate("db_browser_main", u"tbd", None))
        self.data_label.setText(QCoreApplication.translate("db_browser_main", u"Data", None))
        self.menuActions.setTitle(QCoreApplication.translate("db_browser_main", u"Actions", None))
    # retranslateUi

