import serial
import time
import threading
import datetime
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,  QPushButton, QVBoxLayout, QHBoxLayout,QLabel,
QPushButton, QTextEdit,  QGridLayout, QRadioButton, QSlider,  QMessageBox,QTabWidget, QProgressBar, QAction, qApp, QApplication, QComboBox, QLineEdit)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

class mainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initmainWidgetUI()

    def initmainWidgetUI(self):
        print('initmainWidgetUI')

        ## Make Main Text box
        self.mainTesxBox = QTextEdit()

        ## Make Line Edit
        self.destPanIDLineEdit = QLineEdit()
        self.destAddressLineEdit = QLineEdit()
        self.seqNoLineEdit = QLineEdit()
        self.cmdLineEdit = QLineEdit()
        self.dataLineEdit = QLineEdit()

        mainlayout = QGridLayout()

        mainlayout.addWidget(QLabel('Dest.PanID'), 0, 0)
        mainlayout.addWidget(QLabel('Dest.Address'), 0, 2)
        mainlayout.addWidget(QLabel('Seq No.'), 1, 0)
        mainlayout.addWidget(QLabel('Cmd No.'), 1, 2)
        mainlayout.addWidget(QLabel('Data'), 1, 4)
        mainlayout.addWidget(QLabel('\t\t\t\t\t'), 0, 5)

        mainlayout.addWidget(self.destPanIDLineEdit, 0, 1, 1, 1)
        mainlayout.addWidget(self.destAddressLineEdit, 0, 3, 1, 1)
        mainlayout.addWidget(self.seqNoLineEdit, 1, 1, 1, 1)
        mainlayout.addWidget(self.cmdLineEdit, 1, 3, 1, 1)
        mainlayout.addWidget(self.dataLineEdit, 1, 5, 1, 1)

        mainlayout.addWidget(self.mainTesxBox, 2, 0, 1, 0)

        self.setLayout(mainlayout)

class LoRaConfigWindow(QWidget):

    lorawindowStatus = True

    def __init__(self):
        super().__init__()
        self.initLoRaWindowUI()

    def initLoRaWindowUI(self):
        print('initLoRaWindowUI')
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('LoRa Info Configration')

        ## Make Button
        self.cancelBT = QtWidgets.QPushButton('Cancel')
        self.cancelBT.clicked.connect(self.cancelBT_Push)

        self.saveBT = QtWidgets.QPushButton('Save')
        self.saveBT.clicked.connect(self.saveBT_Push)

        self.saveRestartBT = QtWidgets.QPushButton('Save/Restart')
        self.saveRestartBT.clicked.connect(self.saveRestartBT_Push)

        ## Make dropDownMenu / LineEdit
        self.nodeDropDown = QComboBox()
        self.nodeDropDown.addItems(['Coordinator', 'EndDevice'])

        self.bwDropDown = QComboBox()
        self.bwDropDown.addItems(['31.25kHz', '41.7kHz', '62.5kHz', '125kHz', '250kHz', '500kHz'])

        self.panIDLineEdit = QLineEdit()

        self.chLineEdit = QLineEdit()

        self.dstIDLineEdit = QLineEdit()

        self.ownIDLineEdit = QLineEdit()

        self.sfDropDown = QComboBox()
        self.sfDropDown.addItems(['7', '8', '9', '10', '11', '12'])



        loraLayout = QGridLayout()

        loraLayout.addWidget(QLabel('node'), 0, 0)
        loraLayout.addWidget(QLabel('bw'), 0, 2)
        loraLayout.addWidget(QLabel('panID'), 1, 0)
        loraLayout.addWidget(QLabel('ch'), 1, 2)
        loraLayout.addWidget(QLabel('dstID'), 2, 0)
        loraLayout.addWidget(QLabel('ownID'), 2, 2)
        loraLayout.addWidget(QLabel('sf'), 3, 0)

        loraLayout.addWidget(self.nodeDropDown, 0, 1)
        loraLayout.addWidget(self.bwDropDown, 0, 3)
        loraLayout.addWidget(self.panIDLineEdit, 1, 1)
        loraLayout.addWidget(self.chLineEdit, 1, 3)
        loraLayout.addWidget(self.dstIDLineEdit, 2, 1)
        loraLayout.addWidget(self.ownIDLineEdit, 2, 3)
        loraLayout.addWidget(self.sfDropDown, 3, 1)

        loraLayout.addWidget(self.cancelBT, 4, 0)
        loraLayout.addWidget(self.saveBT, 4, 2)
        loraLayout.addWidget(self.saveRestartBT, 4, 3)

        self.setLayout(loraLayout)

    def cancelBT_Push(self):
        print('cancelBT_Push')
        self.hide()

    def saveBT_Push(self):
        print('saveBT_Push')
        print(self.nodeDropDown.currentText())
        print(self.nodeDropDown.currentIndex())
        print(self.panIDText.text())


    def saveRestartBT_Push(self):
        print('saveRestartBT_Push')

    def nodeDropDown_Select(self):
        print('nodeDropDown_Select')

class COMPortSettingWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initComPortUI()

    def initComPortUI(self):
        print('initComPortUI')

class MainWindow(QMainWindow):
    # Global variables for the Program

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print('initUI')
        self.setGeometry(300, 300, 500, 300)
        self.statusBar()

        ##Menu Bar & Menu Bar Item
        config_action = QAction('&Configration', self)
        config_action.setShortcut('Ctrl+C')
        config_action.setStatusTip('Lora Configration Info')

        config_action.triggered.connect(self.LoRaConfig_window)

        exit_action = QAction("&Exit", self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit Application')

        exit_action.triggered.connect(qApp.quit)

        com_action = QAction("&ComPort", self)
        com_action.setShortcut('Ctrl+P')
        com_action.setStatusTip('Setting COM Port')

        com_action.triggered.connect(self.ComPortSetting)

        menubar = self.menuBar()
        fielmenu = menubar.addMenu('&File')
        fielmenu.addAction(config_action)
        fielmenu.addAction(com_action)
        fielmenu.addAction(exit_action)

        mainWidgetUI = mainWidget()
        self.setCentralWidget(mainWidgetUI)


    def LoRaConfig_window(self):
        print('LoRaConfig_Window')
        self.LoraConfig = LoRaConfigWindow()
        self.LoraConfig.show()

    def ComPortSetting(self):
        print('ComPortSetting')
        self.comportWindow = COMPortSettingWindow()
        self.comportWindow.show()



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.showMaximized()
    window.setWindowTitle("LS920LR_Moniter / HGW-3 USB")
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
