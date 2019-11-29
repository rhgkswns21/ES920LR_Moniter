import serial
import time
import threading
import datetime
import sys
import os
import glob
import copy
import json

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,  QPushButton, QVBoxLayout, QHBoxLayout,QLabel,
QPushButton, QTextEdit,  QGridLayout, QRadioButton, QSlider,  QMessageBox,QTabWidget, QProgressBar, QAction, qApp, QApplication, QComboBox, QLineEdit)
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

f= open('config.json', 'r')
config = json.load(f)
f.close()
print(config)

lora_default_info = [config['Node'], config['BW'], config['CH'], config['PanID'], config['OwnID'], config['Ack'], config['TransMode'], config['RcvID'], config['RSSI'], config['SF']]

window = None
es920lr = None
COMPORT_List = None
mainThread = None

file_name = ''
img_flag = False
mainThread_Flag = False

class mainWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initmainWidgetUI()

    def initmainWidgetUI(self):
        print('initmainWidgetUI')

        ## Make Main Text box
        self.mainTesxBox = QTextEdit()
        self.mainTesxBox.append('Start Program...')

        ## Make Line Edit
        # self.destPanIDLineEdit = QLineEdit()
        # self.destAddressLineEdit = QLineEdit()
        # self.seqNoLineEdit = QLineEdit()
        # self.cmdLineEdit = QLineEdit()
        # self.dataLineEdit = QLineEdit()

        mainlayout = QGridLayout()

        # mainlayout.addWidget(QLabel('Dest.PanID'), 0, 0)
        # mainlayout.addWidget(QLabel('Dest.Address'), 0, 2)
        # mainlayout.addWidget(QLabel('Seq No.'), 1, 0)
        # mainlayout.addWidget(QLabel('Cmd No.'), 1, 2)
        # mainlayout.addWidget(QLabel('Data'), 1, 4)
        # mainlayout.addWidget(QLabel('\t\t\t\t\t'), 0, 5)

        # mainlayout.addWidget(self.destPanIDLineEdit, 0, 1, 1, 1)
        # mainlayout.addWidget(self.destAddressLineEdit, 0, 3, 1, 1)
        # mainlayout.addWidget(self.seqNoLineEdit, 1, 1, 1, 1)
        # mainlayout.addWidget(self.cmdLineEdit, 1, 3, 1, 1)
        # mainlayout.addWidget(self.dataLineEdit, 1, 5, 1, 1)

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
        Node_str = str(lora_default_info[0]).split(' ')[1]
        self.nodeDropDown.setCurrentIndex(int(Node_str) - 1)

        self.bwDropDown = QComboBox()
        self.bwDropDown.addItems(['31.25kHz', '41.7kHz', '62.5kHz', '125kHz', '250kHz', '500kHz'])
        BW_str = str(lora_default_info[1]).split(' ')[1]
        self.bwDropDown.setCurrentIndex(int(BW_str) - 1)

        self.chLineEdit = QLineEdit()
        CH_str = str(lora_default_info[2]).split(' ')[1]
        self.chLineEdit.setText(CH_str)

        self.panIDLineEdit = QLineEdit()
        PanID_str = str(lora_default_info[3]).split(' ')[1]
        self.panIDLineEdit.setText(PanID_str)

        self.dstIDLineEdit = QLineEdit()
        RcvID_str = str(lora_default_info[7]).split(' ')[1]
        self.dstIDLineEdit.setText(RcvID_str)

        self.ownIDLineEdit = QLineEdit()
        OwnID_str = str(lora_default_info[4]).split(' ')[1]
        self.ownIDLineEdit.setText(OwnID_str)

        self.sfDropDown = QComboBox()
        self.sfDropDown.addItems(['7', '8', '9', '10', '11', '12'])
        SF_str = str(lora_default_info[9]).split(' ')[1]
        self.sfDropDown.setCurrentText(str(SF_str))

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

    def save_json(self):
        global lora_default_info
        print('save_json')
        a = self.nodeDropDown.currentIndex() +1
        b = self.bwDropDown.currentIndex() + 1
        c = self.sfDropDown.currentText()
        d = self.chLineEdit.text()
        e = self.panIDLineEdit.text()
        f = self.ownIDLineEdit.text()
        o = self.dstIDLineEdit.text()

        new_config = {'Node': 'a ' + str(a), 'BW': 'b ' + str(b), 'CH' : 'd ' + str(d), 'PanID' : 'e ' + str(e),
                      'OwnID' : 'f ' + str(f), 'Ack' : 'l 1', 'TransMode' : 'n 2', 'RcvID' : 'o ' + str(o), 'RSSI' : 'p 1', 'SF' : 'c ' + str(c)}

        f = open('config.json', 'w')
        json.dump(new_config, f)
        f.close()

        f = open('config.json', 'r')
        new_config = json.load(f)
        f.close()

        lora_default_info = [new_config['Node'], new_config['BW'], new_config['CH'], new_config['PanID'], new_config['OwnID'],
                             new_config['Ack'], new_config['TransMode'], new_config['RcvID'], new_config['RSSI'], new_config['SF']]

    def saveBT_Push(self):
        print('saveBT_Push')
        self.save_json()
        self.hide()

    def saveRestartBT_Push(self):
        print('saveRestartBT_Push')
        self.save_json()

        restart()

        self.hide()

class COMPortSettingWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initComPortUI()

    def initComPortUI(self):
        global es920lr
        print('initComPortUI')
        self.setGeometry(400, 400, 300, 100)
        self.setWindowTitle('COM Port Setting')

        ## Make dropDownMenu
        self.comPortDropDown = QComboBox()
        if es920lr != None:
            self.comPortDropDown.addItem(es920lr._port)
        self.comPortDropDown.addItems(get_COMPort())

        ## Make Button
        self.okBT = QtWidgets.QPushButton('OK')
        self.okBT.clicked.connect(self.okBT_Push)

        self.cancelBT = QtWidgets.QPushButton('Cancel')
        self.cancelBT.clicked.connect(self.cancelBT_Push)

        comPortLayout = QGridLayout()
        comPortLayout.addWidget(self.comPortDropDown, 0, 0, 1, 0)
        comPortLayout.addWidget(self.okBT, 1, 0)
        comPortLayout.addWidget(self.cancelBT, 1, 1)

        self.setLayout(comPortLayout)

    def okBT_Push(self):
        global es920lr
        print('okBT_Push')
        print(self.comPortDropDown.currentText())

        COMPORT_List.clear()
        COMPORT_List.append(self.comPortDropDown.currentText())

        restart()
        self.hide()

    def cancelBT_Push(self):
        print('cancelBT_Push')
        self.hide()


class MainWindow(QMainWindow):
    # Global variables for the Program

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print('initUI')
        self.setGeometry(300, 300, 700, 300)
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

        self.mainWidgetUI = mainWidget()
        self.setCentralWidget(self.mainWidgetUI)

    def write_Data(self, value):
        # print('write_Data')
        self.mainWidgetUI.mainTesxBox.append(value)

    def LoRaConfig_window(self):
        print('LoRaConfig_Window')
        self.LoraConfig = LoRaConfigWindow()
        self.LoraConfig.show()

    def ComPortSetting(self):
        print('ComPortSetting')
        self.comportWindow = COMPortSettingWindow()
        self.comportWindow.show()


def restart():
    global mainThread_Flag
    global es920lr
    global COMPORT_List
    global mainThread

    mainThread_Flag = False

    if es920lr == None:
        COMPORT_List = get_COMPort()
        print(COMPORT_List)
        if COMPORT_List:
            print('Re Connect')
            es920lr = serial.Serial(COMPORT_List[0], 115200)
            mainThread = threading.Thread(target=test01TH, args=(es920lr,))
            mainThread_Flag = True
            mainThread.start()
    else:
        print('COM Port State = ', es920lr.is_open)
        if es920lr.is_open:
            print('COM Port Connect')
            print('mainThread Stat = ', mainThread.is_alive())
            # es920lr.write(bytes('\r\n', encoding='ascii'))

            print('main Thread wait...')
            while es920lr.is_open:
                time.sleep(0.1)
                es920lr.close()

            if mainThread.is_alive():
                print('main False')
                mainThread.join(3)

            es920lr = serial.Serial(COMPORT_List[0], 115200)
            mainThread = threading.Thread(target=test01TH, args=(es920lr,))
            mainThread_Flag = True
            mainThread.start()

        else:
            print('COM PORT DicConnect')
            es920lr = serial.Serial(COMPORT_List[0], 115200)
            mainThread = threading.Thread(target=test01TH, args=(es920lr,))
            mainThread_Flag = True
            mainThread.start()

def lora_init(ser):

    ok_flag = True
    ser.write(bytes('2\r\n', encoding='ascii'))
    while ok_flag:
        ok_flag = ok_check(ser)

    for i in lora_default_info:
        ok_flag = True
        ser.write(bytes(i + '\r\n', encoding='ascii'))
        while ok_flag:
            ok_flag = ok_check(ser)

    ok_flag = True
    ser.write(bytes('y\r\n', encoding='ascii'))
    time.sleep(1)
    ser.write(bytes('z\r\n', encoding='ascii'))
    while ok_flag:
        ok_flag = ok_check(ser)
    time.sleep(1)
    print(ser.readline())

    print("Config All Pass")

def ok_check(ser) -> bool:
    global window
    time.sleep(0.1)
    str_data = ''

    if mainThread_Flag == False:
        return False

    try:
        data = ser.readline()
        str_data = bytes(data).decode('utf-8')
        print('OK_CHECK = ', str_data)
        log_str = str(datetime.datetime.now()) + '\t' + str_data
        window.write_Data(log_str)
    except UnicodeDecodeError or PermissionError or serial.serialutil.SerialException or WindowsError:
        print('UnicodeDecodeError')
        serial.Serial.readline()


    if 'OK' in str_data:
        print('pass')
        ok_flag = False
    else:
        print('not pass')
        ok_flag = True

    return ok_flag

def time_out_TH():
    global time_out_flag
    global img_flag
    global file_name

    print('Time Out...')
    img_flag = False
    now_path = os.getcwd()
    print(now_path + file_name + '.jpg')
    os.remove(file_name + '.jpg')

def test01TH(ser):
    global loraRxData
    global loraInitFlag
    global passFlag
    global rxPanID
    global srcid
    global dstid
    global length
    global rssi
    global data
    global window
    global img_flag
    global file_name
    global mainThread_Flag

    try:
        lora_init(ser)
        mainThread_Flag = True
    except AttributeError or PermissionError or serial.serialutil.SerialException:
        print('AttributeError or PermissionError or serial.serialutil.SerialException')
        mainThread_Flag = False

    print('main flag = ', mainThread_Flag)

    while True and mainThread_Flag:
        print('in Loop')
        pre_raw_data = []
        time.sleep(1)
        while ser.readable():
            try:
                head_data = []
                raw_data = []
                time_out = threading.Timer(5, time_out_TH)

                if img_flag:
                    time_out.start()

                for i in range(8):
                    loraRxData = ser.read()
                    head_data.append(loraRxData.hex())

                for i in range(int(head_data[0], 16) - 7):
                    loraRxData = ser.read()
                    raw_data.append(loraRxData)

                log_data = str(datetime.datetime.now()) + '\t' + head_data[0] + '-' + head_data[1] + head_data[2] + '-' + head_data[3] + head_data[4] + '-' + head_data[5] + head_data[6] + head_data[7] + '-'
                for i in raw_data:
                    log_data = log_data + i.hex()

                if (raw_data[0] == b's') and (raw_data[1] == b't') and (raw_data[2] == b'a') and (raw_data[3] == b'r') and (raw_data[4] == b't') and (img_flag == False):
                    img_flag = True
                    now = datetime.datetime.now()
                    file_name = now.strftime('%Y-%m-%d %H%M%S')
                    print('Save Start...')
                elif (raw_data[0] == b'e') and (raw_data[1] == b'n') and (raw_data[2] == b'd') and (img_flag == True):
                    time_out.cancel()
                    img_flag = False
                    print('Save End...')
                elif (pre_raw_data == raw_data) and (img_flag == True):
                    time_out.cancel()
                    print('same Data...')
                elif img_flag:
                    time_out.cancel()
                    f = open(file_name + '.jpg', 'ab')
                    for i in raw_data:
                        f.write(i)
                    f.close()

                pre_raw_data = copy.copy(raw_data)
                print(raw_data)
                head_data.clear()
                raw_data.clear()
                window.write_Data(log_data)
                if mainThread_Flag == False:
                    print('Stop Main Thread...')
                    break
            except TypeError or AttributeError or serial.serialutil.SerialException or PermissionError:
                print('TypeError / serial.serialutil.SerialException / AttributeError')
                mainThread_Flag = False
        break
    ser.close()
    print('Main Thread Out')

def get_COMPort():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def main():
    global COMPORT_List
    global mainThread
    global es920lr
    global window
    global mainThread_Flag

    COMPORT_List = get_COMPort()
    print(COMPORT_List)

    app = QApplication(sys.argv)
    window = MainWindow()
    # window.showMaximized()
    window.setWindowTitle("LS920LR_Moniter / HGW-3 USB")
    window.show()

    if COMPORT_List:
        es920lr = serial.Serial(COMPORT_List[0], 115200)
        mainThread = threading.Thread(target=test01TH, args=(es920lr,))
        mainThread_Flag = True
        mainThread.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
