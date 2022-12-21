import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from_dialog = uic.loadUiType("dlg_MotionSelect.ui")[0]


class dialog_window(QDialog, from_dialog):
    def __init__(self, data):
        super(dialog_window, self).__init__()
        self.motionData = []
        self.motionData = data
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        if self.motionData[0] != 'None':
            self.comboInit()

        self.Btn_OK.clicked.connect(self.onOKButtonClicked)
        self.Btn_Cancel.clicked.connect(self.onCancelButtonClicked)

    def comboInit(self):
        self.comboBox_1.setCurrentText(self.motionData[0])
        self.comboBox_2.setCurrentText(self.motionData[1])
        self.comboBox_3.setCurrentText(self.motionData[2])
        self.comboBox_4.setCurrentText(self.motionData[3])
        self.comboBox_5.setCurrentText(self.motionData[4])
        self.comboBox_6.setCurrentText(self.motionData[5])

    def onOKButtonClicked(self):
        self.motionData = []
        self.motionData.append(self.comboBox_1.currentText())
        self.motionData.append(self.comboBox_2.currentText())
        self.motionData.append(self.comboBox_3.currentText())
        self.motionData.append(self.comboBox_4.currentText())
        self.motionData.append(self.comboBox_5.currentText())
        self.motionData.append(self.comboBox_6.currentText())
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()
