import os
import sys
import multiprocessing
import csv
import signal
from PyQt5.QtCore import QRect, Qt, qAbs, QUrl, QSize, QIODevice, QBuffer, QByteArray, QCoreApplication
from PyQt5.QtGui import QColor, QGuiApplication, QPainter, QPen, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextBrowser, QVBoxLayout,QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
import time
import base64
import io
import requests
import json
from PIL.ImageQt import ImageQt

data = list(csv.reader(open('data.csv')))
search_dic = {}
for n, i in enumerate(data[0]):
    search_dic[i] = data[1][n]
translate_dic = {}
for n, i in enumerate(data[2]):
    translate_dic[i] = data[3][n]

base64_str = None


class windows():
    # 截屏
    def clip(q):
        photo = None

        class CaptureScreen(QDialog):
            # 初始化变量
            beginPosition = None
            endPosition = None
            fullScreenImage = None
            captureImage = None
            isMousePressLeft = None
            painter = QPainter()

            def __init__(self):
                super(QWidget, self).__init__()
                self.initWindow()   # 初始化窗口
                self.captureFullScreen()    # 获取全屏

            def initWindow(self):
                self.setMouseTracking(True)     # 鼠标追踪
                self.setCursor(Qt.CrossCursor)  # 设置光标
                self.setWindowFlag(Qt.FramelessWindowHint)  # 窗口无边框
                self.setWindowState(Qt.WindowFullScreen)    # 窗口全屏

            def captureFullScreen(self):
                self.fullScreenImage = QGuiApplication.primaryScreen(
                ).grabWindow(QApplication.desktop().winId())

            def mousePressEvent(self, event):
                if event.button() == Qt.LeftButton:
                    self.beginPosition = event.pos()
                    self.isMousePressLeft = True
                if event.button() == Qt.RightButton:
                    # 如果选取了图片,则按一次右键开始重新截图
                    if self.captureImage is not None:
                        self.captureImage = None
                        self.paintBackgroundImage()
                        self.update()
                    else:
                        self.close()

            def mouseMoveEvent(self, event):
                if self.isMousePressLeft is True:
                    self.endPosition = event.pos()
                    self.update()

            def mouseReleaseEvent(self, event):
                self.endPosition = event.pos()
                self.isMousePressLeft = False

            def mouseDoubleClickEvent(self, event):
                if self.captureImage is not None:
                    self.saveImage()
                    self.close()

            def keyPressEvent(self, event):
                if event.key() == Qt.Key_Escape:
                    self.close()
                if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                    if self.captureImage is not None:
                        self.saveImage()
                        self.close()

            def paintBackgroundImage(self):
                shadowColor = QColor(0, 0, 0, 100)  # 黑色半透明
                self.painter.drawPixmap(0, 0, self.fullScreenImage)
                self.painter.fillRect(
                    self.fullScreenImage.rect(), shadowColor)     # 填充矩形阴影

            def paintEvent(self, event):
                self.painter.begin(self)    # 开始重绘
                self.paintBackgroundImage()
                penColor = QColor(30, 144, 245)     # 画笔颜色
                # 设置画笔,蓝色,1px大小,实线,圆形笔帽
                self.painter.setPen(
                    QPen(penColor, 1, Qt.SolidLine, Qt.RoundCap))
                if self.isMousePressLeft is True:
                    pickRect = self.getRectangle(
                        self.beginPosition, self.endPosition)   # 获得要截图的矩形框
                    self.captureImage = self.fullScreenImage.copy(
                        pickRect)         # 捕获截图矩形框内的图片
                    self.painter.drawPixmap(
                        pickRect.topLeft(), self.captureImage)  # 填充截图的图片
                    self.painter.drawRect(pickRect)     # 画矩形边框
                self.painter.end()  # 结束重绘

            def getRectangle(self, beginPoint, endPoint):
                pickRectWidth = int(qAbs(beginPoint.x() - endPoint.x()))
                pickRectHeight = int(qAbs(beginPoint.y() - endPoint.y()))
                pickRectTop = beginPoint.x() if beginPoint.x() < endPoint.x() else endPoint.x()
                pickRectLeft = beginPoint.y() if beginPoint.y() < endPoint.y() else endPoint.y()
                pickRect = QRect(pickRectTop, pickRectLeft,
                                 pickRectWidth, pickRectHeight)
                # 避免高度宽度为0时候报错
                if pickRectWidth == 0:
                    pickRect.setWidth(2)
                if pickRectHeight == 0:
                    pickRect.setHeight(2)

                return pickRect

            def saveImage(self):
                self.captureImage.save(
                    'picture.png', quality=95)   # 保存图片到当前文件夹中
                byte_array = QByteArray()
                buffer = QBuffer(byte_array)
                buffer.open(QIODevice.WriteOnly)
                self.captureImage.save(buffer, 'jpg', 75)

                cover_image_final = io.BytesIO(byte_array)
                cover_image_final.seek(0)
                byte_data = cover_image_final.getvalue()
                base64_str = base64.b64encode(byte_data).decode('utf8')
                q.put(base64_str)

        if __name__ == "__main__":
            app = QApplication(sys.argv)
            window = CaptureScreen()
            window.show()
            sys.exit(app.exec_())

    def show_text(x):
        from ui import Ui_MainWindow

        class MyMainForm(QMainWindow, Ui_MainWindow):
            def __init__(self, parent=None):
                super(MyMainForm, self).__init__(parent)
                self.setupUi(self)

                self.comboBox_1.addItems(data[0])
                self.comboBox_2.addItems(data[2])
                self.textEdit.setText(x)
                self.pushButton_1.clicked.connect(
                    lambda: self.display_interface('search'))
                self.pushButton_2.clicked.connect(
                    lambda: self.display_interface('translate'))
                self.pushButton_4.clicked.connect(
                    lambda: self.display_interface('open'))
                self.webEngineView = WebEngineView(self.splitter)

            def settext(self, x):
                self.textEdit.setText(x)

            def display_interface(self, m):
                x = self.textEdit.toPlainText()
                url = ''
                if m == 'search':
                    o_url = search_dic[self.comboBox_1.currentText()]
                    url = o_url.replace('%s', x)
                if m == 'translate':
                    o_url = translate_dic[self.comboBox_2.currentText()]
                    url = o_url.replace('%s', x)

                self.webEngineView.load(QUrl(url))
                self.webEngineView.setMinimumSize(QSize(0, 500))
                if m == 'open':
                    QDesktopServices.openUrl(QUrl(self.webEngineView.url()))

        class WebEngineView(QWebEngineView):
            # 重写createwindow()
            def createWindow(self, QWebEnginePage_WebWindowType):
                return self

        if __name__ == "__main__":
            app = QApplication(sys.argv)
            myWin = MyMainForm()
            myWin.show()
            sys.exit(app.exec_())


def xocr(data):
    data = data
    headers = {"Content-type": "application/json"}
    url = "http://127.0.0.1:8080"
    try:
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        print('ocr ok')
    except:
        print('err')
    text = ''
    for i in r.json()['txts']:
        text = text+i+'\n'
    return text

if __name__ == "__main__":
    q = multiprocessing.Queue()
    o = multiprocessing.Process(target=windows.clip, args=(q,))
    o.start()
    o.join()
    text = xocr(q.get())
    s = multiprocessing.Process(target=windows.show_text, args=(text,))
    s.start()
    s.join()