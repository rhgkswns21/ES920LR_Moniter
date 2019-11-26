import serial
import time
import threading
import datetime
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,  QPushButton, QVBoxLayout, QHBoxLayout,QLabel,
QPushButton, QTextEdit,  QGridLayout, QRadioButton, QSlider,  QMessageBox,QTabWidget, QProgressBar, QAction, qApp, QApplication)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

class LoRaConfigWindow(QWidget):

    lorawindowStatus = True

    def __init__(self):
        super().__init__()
        self.initLoRaWindowUI()

    def initLoRaWindowUI(self):
        print('initLoRaWindowUI')
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('LoRa Info Configration')

class MainWindow(QMainWindow):
    # Global variables for the Program

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print('initUI')

        ##Menu Bar & Menu Bar Item
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit Application')

        exit_action.triggered.connect(qApp.quit)

        config_action = QAction('&Configration', self)
        config_action.setShortcut('Ctrl+C')
        config_action.setStatusTip('Lora Configration Info')

        config_action.triggered.connect(self.LoRaConfig_window)


        self.statusBar()

        menubar = self.menuBar()
        fielmenu = menubar.addMenu('&File')
        fielmenu.addAction(exit_action)
        fielmenu.addAction(config_action)

    def LoRaConfig_window(self):
        print('LoRaConfig_Window')
        self.LoraConfig = LoRaConfigWindow()
        self.LoraConfig.show()







def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.showMaximized()
    window.setWindowTitle("LS920LR_Moniter / HGW-3 USB")
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
