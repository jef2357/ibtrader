# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'spx_trader_splitter_layoutLzIVJD.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QSplitter, QStatusBar, QTableView,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1735, 1675)
        self.actionSub_Menu_1 = QAction(MainWindow)
        self.actionSub_Menu_1.setObjectName(u"actionSub_Menu_1")
        self.accounts_action = QAction(MainWindow)
        self.accounts_action.setObjectName(u"accounts_action")
        self.connect_action = QAction(MainWindow)
        self.connect_action.setObjectName(u"connect_action")
        self.disconnect_action = QAction(MainWindow)
        self.disconnect_action.setObjectName(u"disconnect_action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.buttons_messages_frame = QFrame(self.layoutWidget)
        self.buttons_messages_frame.setObjectName(u"buttons_messages_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons_messages_frame.sizePolicy().hasHeightForWidth())
        self.buttons_messages_frame.setSizePolicy(sizePolicy)
        self.buttons_messages_frame.setMinimumSize(QSize(0, 50))
        self.buttons_messages_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.buttons_messages_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.buttons_messages_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.chain_pushbutton = QPushButton(self.buttons_messages_frame)
        self.chain_pushbutton.setObjectName(u"chain_pushbutton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chain_pushbutton.sizePolicy().hasHeightForWidth())
        self.chain_pushbutton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.chain_pushbutton)

        self.positions_pushButton = QPushButton(self.buttons_messages_frame)
        self.positions_pushButton.setObjectName(u"positions_pushButton")
        sizePolicy1.setHeightForWidth(self.positions_pushButton.sizePolicy().hasHeightForWidth())
        self.positions_pushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.positions_pushButton)

        self.buttons_spacer_2 = QSpacerItem(258, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.buttons_spacer_2)

        self.label = QLabel(self.buttons_messages_frame)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(80, 25))
        self.label.setMaximumSize(QSize(80, 25))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.buttons_messages_frame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(80, 25))
        self.label_2.setMaximumSize(QSize(80, 25))

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout_5.addWidget(self.buttons_messages_frame)

        self.splitter = QSplitter(self.layoutWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.tables_splitter = QSplitter(self.splitter)
        self.tables_splitter.setObjectName(u"tables_splitter")
        self.tables_splitter.setOrientation(Qt.Orientation.Horizontal)
        self.position_frame = QFrame(self.tables_splitter)
        self.position_frame.setObjectName(u"position_frame")
        self.position_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.position_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.position_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.positions_label_layout = QHBoxLayout()
        self.positions_label_layout.setObjectName(u"positions_label_layout")
        self.positions_label = QLabel(self.position_frame)
        self.positions_label.setObjectName(u"positions_label")

        self.positions_label_layout.addWidget(self.positions_label)

        self.positions_label_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.positions_label_layout.addItem(self.positions_label_spacer)


        self.verticalLayout.addLayout(self.positions_label_layout)

        self.positions_table = QTableView(self.position_frame)
        self.positions_table.setObjectName(u"positions_table")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.positions_table.sizePolicy().hasHeightForWidth())
        self.positions_table.setSizePolicy(sizePolicy2)
        self.positions_table.setMinimumSize(QSize(200, 0))
        self.positions_table.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.positions_table)

        self.tables_splitter.addWidget(self.position_frame)
        self.chain_frame = QFrame(self.tables_splitter)
        self.chain_frame.setObjectName(u"chain_frame")
        self.chain_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.chain_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.chain_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.chain_label_layout = QHBoxLayout()
        self.chain_label_layout.setObjectName(u"chain_label_layout")
        self.chain_label = QLabel(self.chain_frame)
        self.chain_label.setObjectName(u"chain_label")

        self.chain_label_layout.addWidget(self.chain_label)

        self.chain_label_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.chain_label_layout.addItem(self.chain_label_spacer)

        self.label_3 = QLabel(self.chain_frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(30, 20))
        self.label_3.setMaximumSize(QSize(30, 20))
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.chain_label_layout.addWidget(self.label_3)

        self.sd_comboBox = QComboBox(self.chain_frame)
        self.sd_comboBox.setObjectName(u"sd_comboBox")

        self.chain_label_layout.addWidget(self.sd_comboBox)


        self.verticalLayout_2.addLayout(self.chain_label_layout)

        self.chain_table = QTableView(self.chain_frame)
        self.chain_table.setObjectName(u"chain_table")
        sizePolicy2.setHeightForWidth(self.chain_table.sizePolicy().hasHeightForWidth())
        self.chain_table.setSizePolicy(sizePolicy2)
        self.chain_table.setMinimumSize(QSize(200, 0))
        self.chain_table.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.chain_table)

        self.tables_splitter.addWidget(self.chain_frame)
        self.splitter.addWidget(self.tables_splitter)
        self.actions_frame = QFrame(self.splitter)
        self.actions_frame.setObjectName(u"actions_frame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.actions_frame.sizePolicy().hasHeightForWidth())
        self.actions_frame.setSizePolicy(sizePolicy3)
        self.actions_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.actions_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.actions_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_9)

        self.call_frame = QFrame(self.actions_frame)
        self.call_frame.setObjectName(u"call_frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.call_frame.sizePolicy().hasHeightForWidth())
        self.call_frame.setSizePolicy(sizePolicy4)
        self.call_frame.setFrameShape(QFrame.Shape.Box)
        self.call_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.call_horizontalLayout = QHBoxLayout(self.call_frame)
        self.call_horizontalLayout.setObjectName(u"call_horizontalLayout")
        self.call_horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.call_loss_verticalLayout = QVBoxLayout()
        self.call_loss_verticalLayout.setObjectName(u"call_loss_verticalLayout")
        self.call_loss_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_loss_label = QLabel(self.call_frame)
        self.call_loss_label.setObjectName(u"call_loss_label")
        sizePolicy1.setHeightForWidth(self.call_loss_label.sizePolicy().hasHeightForWidth())
        self.call_loss_label.setSizePolicy(sizePolicy1)
        self.call_loss_label.setMinimumSize(QSize(40, 20))
        self.call_loss_label.setMaximumSize(QSize(40, 20))
        self.call_loss_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.call_loss_verticalLayout.addWidget(self.call_loss_label)

        self.call_loss_spinbox = QDoubleSpinBox(self.call_frame)
        self.call_loss_spinbox.setObjectName(u"call_loss_spinbox")
        sizePolicy1.setHeightForWidth(self.call_loss_spinbox.sizePolicy().hasHeightForWidth())
        self.call_loss_spinbox.setSizePolicy(sizePolicy1)
        self.call_loss_spinbox.setMinimumSize(QSize(50, 30))
        self.call_loss_spinbox.setMaximumSize(QSize(50, 30))
        self.call_loss_spinbox.setSingleStep(0.050000000000000)

        self.call_loss_verticalLayout.addWidget(self.call_loss_spinbox)


        self.call_horizontalLayout.addLayout(self.call_loss_verticalLayout)

        self.call_gain_verticalLayout = QVBoxLayout()
        self.call_gain_verticalLayout.setObjectName(u"call_gain_verticalLayout")
        self.call_gain_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_gain_label_horizontalLayout = QHBoxLayout()
        self.call_gain_label_horizontalLayout.setObjectName(u"call_gain_label_horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.call_gain_label_horizontalLayout.addItem(self.horizontalSpacer_2)

        self.call_gain_label = QLabel(self.call_frame)
        self.call_gain_label.setObjectName(u"call_gain_label")
        sizePolicy1.setHeightForWidth(self.call_gain_label.sizePolicy().hasHeightForWidth())
        self.call_gain_label.setSizePolicy(sizePolicy1)
        self.call_gain_label.setMinimumSize(QSize(40, 20))
        self.call_gain_label.setMaximumSize(QSize(40, 20))
        self.call_gain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.call_gain_label_horizontalLayout.addWidget(self.call_gain_label)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.call_gain_label_horizontalLayout.addItem(self.horizontalSpacer)


        self.call_gain_verticalLayout.addLayout(self.call_gain_label_horizontalLayout)

        self.call_gain_horizontalLayout = QHBoxLayout()
        self.call_gain_horizontalLayout.setObjectName(u"call_gain_horizontalLayout")
        self.call_gain_checkbox = QCheckBox(self.call_frame)
        self.call_gain_checkbox.setObjectName(u"call_gain_checkbox")
        sizePolicy1.setHeightForWidth(self.call_gain_checkbox.sizePolicy().hasHeightForWidth())
        self.call_gain_checkbox.setSizePolicy(sizePolicy1)
        self.call_gain_checkbox.setMinimumSize(QSize(50, 30))
        self.call_gain_checkbox.setMaximumSize(QSize(50, 30))

        self.call_gain_horizontalLayout.addWidget(self.call_gain_checkbox)

        self.call_gain_spinbox = QDoubleSpinBox(self.call_frame)
        self.call_gain_spinbox.setObjectName(u"call_gain_spinbox")
        sizePolicy1.setHeightForWidth(self.call_gain_spinbox.sizePolicy().hasHeightForWidth())
        self.call_gain_spinbox.setSizePolicy(sizePolicy1)
        self.call_gain_spinbox.setMinimumSize(QSize(50, 30))
        self.call_gain_spinbox.setMaximumSize(QSize(50, 30))
        self.call_gain_spinbox.setSingleStep(0.050000000000000)

        self.call_gain_horizontalLayout.addWidget(self.call_gain_spinbox)


        self.call_gain_verticalLayout.addLayout(self.call_gain_horizontalLayout)


        self.call_horizontalLayout.addLayout(self.call_gain_verticalLayout)

        self.call_strike_verticalLayout = QVBoxLayout()
        self.call_strike_verticalLayout.setObjectName(u"call_strike_verticalLayout")
        self.call_strike_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_strike_label = QLabel(self.call_frame)
        self.call_strike_label.setObjectName(u"call_strike_label")
        sizePolicy1.setHeightForWidth(self.call_strike_label.sizePolicy().hasHeightForWidth())
        self.call_strike_label.setSizePolicy(sizePolicy1)
        self.call_strike_label.setMinimumSize(QSize(40, 20))
        self.call_strike_label.setMaximumSize(QSize(40, 20))
        self.call_strike_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.call_strike_verticalLayout.addWidget(self.call_strike_label)

        self.call_strike = QLabel(self.call_frame)
        self.call_strike.setObjectName(u"call_strike")
        sizePolicy1.setHeightForWidth(self.call_strike.sizePolicy().hasHeightForWidth())
        self.call_strike.setSizePolicy(sizePolicy1)
        self.call_strike.setMinimumSize(QSize(40, 30))
        self.call_strike.setMaximumSize(QSize(40, 30))
        self.call_strike.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.call_strike_verticalLayout.addWidget(self.call_strike)


        self.call_horizontalLayout.addLayout(self.call_strike_verticalLayout)

        self.call_go_verticalLayout = QVBoxLayout()
        self.call_go_verticalLayout.setObjectName(u"call_go_verticalLayout")
        self.call_go_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_label = QLabel(self.call_frame)
        self.call_label.setObjectName(u"call_label")
        sizePolicy1.setHeightForWidth(self.call_label.sizePolicy().hasHeightForWidth())
        self.call_label.setSizePolicy(sizePolicy1)
        self.call_label.setMinimumSize(QSize(40, 20))
        self.call_label.setMaximumSize(QSize(40, 20))
        self.call_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.call_go_verticalLayout.addWidget(self.call_label)

        self.call_go_pushbutton = QPushButton(self.call_frame)
        self.call_go_pushbutton.setObjectName(u"call_go_pushbutton")
        sizePolicy1.setHeightForWidth(self.call_go_pushbutton.sizePolicy().hasHeightForWidth())
        self.call_go_pushbutton.setSizePolicy(sizePolicy1)
        self.call_go_pushbutton.setMinimumSize(QSize(40, 30))
        self.call_go_pushbutton.setMaximumSize(QSize(40, 30))

        self.call_go_verticalLayout.addWidget(self.call_go_pushbutton)


        self.call_horizontalLayout.addLayout(self.call_go_verticalLayout)


        self.horizontalLayout_2.addWidget(self.call_frame)

        self.qty_frame = QFrame(self.actions_frame)
        self.qty_frame.setObjectName(u"qty_frame")
        self.qty_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.qty_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.qty_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.call_strike_label_3 = QLabel(self.qty_frame)
        self.call_strike_label_3.setObjectName(u"call_strike_label_3")
        sizePolicy1.setHeightForWidth(self.call_strike_label_3.sizePolicy().hasHeightForWidth())
        self.call_strike_label_3.setSizePolicy(sizePolicy1)
        self.call_strike_label_3.setMinimumSize(QSize(50, 20))
        self.call_strike_label_3.setMaximumSize(QSize(50, 20))
        self.call_strike_label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.call_strike_label_3)

        self.spinBox = QSpinBox(self.qty_frame)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy1.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy1)
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMaximumSize(QSize(50, 30))

        self.verticalLayout_4.addWidget(self.spinBox)


        self.horizontalLayout_2.addWidget(self.qty_frame)

        self.put_frame = QFrame(self.actions_frame)
        self.put_frame.setObjectName(u"put_frame")
        sizePolicy4.setHeightForWidth(self.put_frame.sizePolicy().hasHeightForWidth())
        self.put_frame.setSizePolicy(sizePolicy4)
        self.put_frame.setFrameShape(QFrame.Shape.Box)
        self.put_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.call_horizontalLayout_2 = QHBoxLayout(self.put_frame)
        self.call_horizontalLayout_2.setObjectName(u"call_horizontalLayout_2")
        self.call_horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.put_go_verticalLayout = QVBoxLayout()
        self.put_go_verticalLayout.setObjectName(u"put_go_verticalLayout")
        self.put_go_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_label_2 = QLabel(self.put_frame)
        self.call_label_2.setObjectName(u"call_label_2")
        sizePolicy1.setHeightForWidth(self.call_label_2.sizePolicy().hasHeightForWidth())
        self.call_label_2.setSizePolicy(sizePolicy1)
        self.call_label_2.setMinimumSize(QSize(40, 20))
        self.call_label_2.setMaximumSize(QSize(40, 20))
        self.call_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.put_go_verticalLayout.addWidget(self.call_label_2)

        self.call_go_pushbutton_2 = QPushButton(self.put_frame)
        self.call_go_pushbutton_2.setObjectName(u"call_go_pushbutton_2")
        sizePolicy1.setHeightForWidth(self.call_go_pushbutton_2.sizePolicy().hasHeightForWidth())
        self.call_go_pushbutton_2.setSizePolicy(sizePolicy1)
        self.call_go_pushbutton_2.setMinimumSize(QSize(40, 30))
        self.call_go_pushbutton_2.setMaximumSize(QSize(40, 30))

        self.put_go_verticalLayout.addWidget(self.call_go_pushbutton_2)


        self.call_horizontalLayout_2.addLayout(self.put_go_verticalLayout)

        self.put_strike_verticalLayout = QVBoxLayout()
        self.put_strike_verticalLayout.setObjectName(u"put_strike_verticalLayout")
        self.put_strike_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_strike_label_2 = QLabel(self.put_frame)
        self.call_strike_label_2.setObjectName(u"call_strike_label_2")
        sizePolicy1.setHeightForWidth(self.call_strike_label_2.sizePolicy().hasHeightForWidth())
        self.call_strike_label_2.setSizePolicy(sizePolicy1)
        self.call_strike_label_2.setMinimumSize(QSize(40, 20))
        self.call_strike_label_2.setMaximumSize(QSize(40, 20))
        self.call_strike_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.put_strike_verticalLayout.addWidget(self.call_strike_label_2)

        self.call_strike_2 = QLabel(self.put_frame)
        self.call_strike_2.setObjectName(u"call_strike_2")
        sizePolicy1.setHeightForWidth(self.call_strike_2.sizePolicy().hasHeightForWidth())
        self.call_strike_2.setSizePolicy(sizePolicy1)
        self.call_strike_2.setMinimumSize(QSize(40, 30))
        self.call_strike_2.setMaximumSize(QSize(40, 30))
        self.call_strike_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.put_strike_verticalLayout.addWidget(self.call_strike_2)


        self.call_horizontalLayout_2.addLayout(self.put_strike_verticalLayout)

        self.put_gain_verticalLayout = QVBoxLayout()
        self.put_gain_verticalLayout.setObjectName(u"put_gain_verticalLayout")
        self.put_gain_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_gain_label_horizontalLayout_2 = QHBoxLayout()
        self.call_gain_label_horizontalLayout_2.setObjectName(u"call_gain_label_horizontalLayout_2")
        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.call_gain_label_horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.call_gain_label_2 = QLabel(self.put_frame)
        self.call_gain_label_2.setObjectName(u"call_gain_label_2")
        sizePolicy1.setHeightForWidth(self.call_gain_label_2.sizePolicy().hasHeightForWidth())
        self.call_gain_label_2.setSizePolicy(sizePolicy1)
        self.call_gain_label_2.setMinimumSize(QSize(40, 20))
        self.call_gain_label_2.setMaximumSize(QSize(40, 20))
        self.call_gain_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.call_gain_label_horizontalLayout_2.addWidget(self.call_gain_label_2)

        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.call_gain_label_horizontalLayout_2.addItem(self.horizontalSpacer_7)


        self.put_gain_verticalLayout.addLayout(self.call_gain_label_horizontalLayout_2)

        self.call_gain_horizontalLayout_2 = QHBoxLayout()
        self.call_gain_horizontalLayout_2.setObjectName(u"call_gain_horizontalLayout_2")
        self.call_gain_checkbox_2 = QCheckBox(self.put_frame)
        self.call_gain_checkbox_2.setObjectName(u"call_gain_checkbox_2")
        sizePolicy1.setHeightForWidth(self.call_gain_checkbox_2.sizePolicy().hasHeightForWidth())
        self.call_gain_checkbox_2.setSizePolicy(sizePolicy1)
        self.call_gain_checkbox_2.setMinimumSize(QSize(50, 30))
        self.call_gain_checkbox_2.setMaximumSize(QSize(50, 30))

        self.call_gain_horizontalLayout_2.addWidget(self.call_gain_checkbox_2)

        self.call_gain_spinbox_2 = QDoubleSpinBox(self.put_frame)
        self.call_gain_spinbox_2.setObjectName(u"call_gain_spinbox_2")
        sizePolicy1.setHeightForWidth(self.call_gain_spinbox_2.sizePolicy().hasHeightForWidth())
        self.call_gain_spinbox_2.setSizePolicy(sizePolicy1)
        self.call_gain_spinbox_2.setMinimumSize(QSize(50, 30))
        self.call_gain_spinbox_2.setMaximumSize(QSize(50, 30))
        self.call_gain_spinbox_2.setSingleStep(0.050000000000000)

        self.call_gain_horizontalLayout_2.addWidget(self.call_gain_spinbox_2)


        self.put_gain_verticalLayout.addLayout(self.call_gain_horizontalLayout_2)


        self.call_horizontalLayout_2.addLayout(self.put_gain_verticalLayout)

        self.put_loss_verticalLayout = QVBoxLayout()
        self.put_loss_verticalLayout.setObjectName(u"put_loss_verticalLayout")
        self.put_loss_verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.call_loss_label_2 = QLabel(self.put_frame)
        self.call_loss_label_2.setObjectName(u"call_loss_label_2")
        sizePolicy1.setHeightForWidth(self.call_loss_label_2.sizePolicy().hasHeightForWidth())
        self.call_loss_label_2.setSizePolicy(sizePolicy1)
        self.call_loss_label_2.setMinimumSize(QSize(40, 20))
        self.call_loss_label_2.setMaximumSize(QSize(40, 20))
        self.call_loss_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.put_loss_verticalLayout.addWidget(self.call_loss_label_2)

        self.call_loss_spinbox_2 = QDoubleSpinBox(self.put_frame)
        self.call_loss_spinbox_2.setObjectName(u"call_loss_spinbox_2")
        sizePolicy1.setHeightForWidth(self.call_loss_spinbox_2.sizePolicy().hasHeightForWidth())
        self.call_loss_spinbox_2.setSizePolicy(sizePolicy1)
        self.call_loss_spinbox_2.setMinimumSize(QSize(50, 30))
        self.call_loss_spinbox_2.setMaximumSize(QSize(50, 30))
        self.call_loss_spinbox_2.setSingleStep(0.050000000000000)

        self.put_loss_verticalLayout.addWidget(self.call_loss_spinbox_2)


        self.call_horizontalLayout_2.addLayout(self.put_loss_verticalLayout)


        self.horizontalLayout_2.addWidget(self.put_frame)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_8)

        self.splitter.addWidget(self.actions_frame)
        self.orders_frame = QFrame(self.splitter)
        self.orders_frame.setObjectName(u"orders_frame")
        self.orders_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.orders_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.orders_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.orders_label_layout = QHBoxLayout()
        self.orders_label_layout.setObjectName(u"orders_label_layout")
        self.orders_label_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.orders_label = QLabel(self.orders_frame)
        self.orders_label.setObjectName(u"orders_label")

        self.orders_label_layout.addWidget(self.orders_label)

        self.orders_label_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.orders_label_layout.addItem(self.orders_label_spacer)


        self.verticalLayout_3.addLayout(self.orders_label_layout)

        self.orders_table = QTableView(self.orders_frame)
        self.orders_table.setObjectName(u"orders_table")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.orders_table.sizePolicy().hasHeightForWidth())
        self.orders_table.setSizePolicy(sizePolicy5)
        self.orders_table.setMinimumSize(QSize(0, 200))
        self.orders_table.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_3.addWidget(self.orders_table)

        self.splitter.addWidget(self.orders_frame)

        self.verticalLayout_5.addWidget(self.splitter)

        self.splitter_2.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.plots_verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.plots_verticalLayout.setObjectName(u"plots_verticalLayout")
        self.plots_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.plot_1_frame = QFrame(self.layoutWidget1)
        self.plot_1_frame.setObjectName(u"plot_1_frame")
        self.plot_1_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_1_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.plot_1_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.plot_1_widget = QWidget(self.plot_1_frame)
        self.plot_1_widget.setObjectName(u"plot_1_widget")
        sizePolicy4.setHeightForWidth(self.plot_1_widget.sizePolicy().hasHeightForWidth())
        self.plot_1_widget.setSizePolicy(sizePolicy4)
        self.plot_1_widget.setMinimumSize(QSize(300, 0))

        self.gridLayout_3.addWidget(self.plot_1_widget, 0, 0, 1, 1)


        self.plots_verticalLayout.addWidget(self.plot_1_frame)

        self.plot_2_frame = QFrame(self.layoutWidget1)
        self.plot_2_frame.setObjectName(u"plot_2_frame")
        self.plot_2_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_2_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.plot_2_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.plot_2_widget = QWidget(self.plot_2_frame)
        self.plot_2_widget.setObjectName(u"plot_2_widget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.plot_2_widget.sizePolicy().hasHeightForWidth())
        self.plot_2_widget.setSizePolicy(sizePolicy6)

        self.gridLayout_2.addWidget(self.plot_2_widget, 0, 0, 1, 1)


        self.plots_verticalLayout.addWidget(self.plot_2_frame)

        self.plot_3_frame = QFrame(self.layoutWidget1)
        self.plot_3_frame.setObjectName(u"plot_3_frame")
        self.plot_3_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.plot_3_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.plot_3_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plot_3_widget = QWidget(self.plot_3_frame)
        self.plot_3_widget.setObjectName(u"plot_3_widget")
        sizePolicy6.setHeightForWidth(self.plot_3_widget.sizePolicy().hasHeightForWidth())
        self.plot_3_widget.setSizePolicy(sizePolicy6)

        self.gridLayout.addWidget(self.plot_3_widget, 0, 0, 1, 1)


        self.plots_verticalLayout.addWidget(self.plot_3_frame)

        self.splitter_2.addWidget(self.layoutWidget1)

        self.gridLayout_4.addWidget(self.splitter_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1735, 22))
        self.actions_menu = QMenu(self.menubar)
        self.actions_menu.setObjectName(u"actions_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.actions_menu.menuAction())
        self.actions_menu.addAction(self.accounts_action)
        self.actions_menu.addAction(self.connect_action)
        self.actions_menu.addAction(self.disconnect_action)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSub_Menu_1.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.accounts_action.setText(QCoreApplication.translate("MainWindow", u"Accounts", None))
        self.connect_action.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.disconnect_action.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.chain_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Chain", None))
        self.positions_pushButton.setText(QCoreApplication.translate("MainWindow", u"Positions", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"STREAMING", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"CONNECTED", None))
        self.positions_label.setText(QCoreApplication.translate("MainWindow", u"Positions", None))
        self.chain_label.setText(QCoreApplication.translate("MainWindow", u"Chain", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"SD", None))
        self.call_loss_label.setText(QCoreApplication.translate("MainWindow", u"LOSS", None))
        self.call_gain_label.setText(QCoreApplication.translate("MainWindow", u"GAIN", None))
        self.call_gain_checkbox.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.call_strike_label.setText(QCoreApplication.translate("MainWindow", u"STRIKE", None))
        self.call_strike.setText(QCoreApplication.translate("MainWindow", u"9999", None))
        self.call_label.setText(QCoreApplication.translate("MainWindow", u"CALL", None))
        self.call_go_pushbutton.setText(QCoreApplication.translate("MainWindow", u"GO", None))
        self.call_strike_label_3.setText(QCoreApplication.translate("MainWindow", u"QTY", None))
        self.call_label_2.setText(QCoreApplication.translate("MainWindow", u"PUT", None))
        self.call_go_pushbutton_2.setText(QCoreApplication.translate("MainWindow", u"GO", None))
        self.call_strike_label_2.setText(QCoreApplication.translate("MainWindow", u"STRIKE", None))
        self.call_strike_2.setText(QCoreApplication.translate("MainWindow", u"9999", None))
        self.call_gain_label_2.setText(QCoreApplication.translate("MainWindow", u"GAIN", None))
        self.call_gain_checkbox_2.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
        self.call_loss_label_2.setText(QCoreApplication.translate("MainWindow", u"LOSS", None))
        self.orders_label.setText(QCoreApplication.translate("MainWindow", u"Orders", None))
        self.actions_menu.setTitle(QCoreApplication.translate("MainWindow", u"Actions", None))
    # retranslateUi

