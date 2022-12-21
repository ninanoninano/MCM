import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys, cv2, numpy, time
from PyQt5 import QtGui
from PyQt5 import QtCore
import datetime
import io
import pyautogui
import numpy as np


# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]
from_secondwindow = uic.loadUiType("untitled2.ui")[0]

out = cv2.VideoWriter('3.mp4', cv2.VideoWriter_fourcc(*'XVID'), 15, (1920, 1080))

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.running = False
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # 파일
        self.FileOpen.clicked.connect(self.fileOpen)
        self.FileOpen_2.clicked.connect(self.fileOpen)
        self.pushButton_3.clicked.connect(self.button_Second)
        self.pushButton.clicked.connect(self.camStart)
        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_5.clicked.connect(self.camStart2)
        self.pushButton_8.clicked.connect(self.stop2)
        self.pushButton_6.clicked.connect(self.button_Second)


    def fileOpen(self):
        fliename = QFileDialog.getOpenFileName(self, '파일 불러오기', '', ' PowerPoint(*.pptx *ppt);; All File(*)')

        if fliename[0]:
            self.lineEdit.setText(fliename[0])
        else:
            print("파일 안 골랐음")

    def camStart(self):
        self.running = True
        self.videocam()

    def videocam(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret == True:
                self.displayImage(frame, 1)
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
                cv2.waitKey()

    def displayImage(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8

        if len(img.shape) == 3:
            if(img.shape[2]) == 4:
                qformat = QtGui.QImage.Format_RGBA888
            else:
                qformat = QtGui.QImage.Format_RGB888
        img = QtGui.QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.label_10.setPixmap(QtGui.QPixmap.fromImage(img))
        self.label_10.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHCenter)

    def stop(self):
        out.release()
        self.running = False
        self.label_10.clear()

    def button_Second(self):
        self.hide()
        self.second = secondwindow()
        self.second.exec()
        self.show()



    def camStart2(self):
        self.running = True
        self.videocam2()

    def videocam2(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret == True:
                self.displayImage2(frame, 1)
                out.write(frame)
                cv2.waitKey()

    def displayImage2(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8

        if len(img.shape) == 3:
            if(img.shape[2]) == 4:
                qformat = QtGui.QImage.Format_RGBA888
            else:
                qformat = QtGui.QImage.Format_RGB888
        img = QtGui.QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.label_12.setPixmap(QtGui.QPixmap.fromImage(img))
        self.label_12.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHCenter)

    def stop2(self):
        self.running = False
        self.label_12.clear()


class secondwindow(QDialog, QWidget, from_secondwindow):
    def __init__(self):
        super(secondwindow, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.Home)

    def Home(self):
        self.close()



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()