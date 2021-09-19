import os
import sys
import multiprocessing
import csv
from PyQt5.QtCore import QBuffer, QRect, Qt, qAbs,QUrl,QSize
from PyQt5.QtGui import QColor, QGuiApplication, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextBrowser, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import webbrowser

data=list(csv.reader(open('data.csv')))
search_dic={}
for n ,i in enumerate(data[0]):
    search_dic[i]=data[1][n]
translate_dic={}
for n ,i in enumerate(data[2]):
    translate_dic[i]=data[3][n]

class windows():
    # 截屏
    def clip():
        photo = None
        class CaptureScreen(QWidget):
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
                self.fullScreenImage = QGuiApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

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
                self.painter.fillRect(self.fullScreenImage.rect(), shadowColor)     # 填充矩形阴影

            def paintEvent(self, event):
                self.painter.begin(self)    # 开始重绘
                self.paintBackgroundImage()
                penColor = QColor(30, 144, 245)     # 画笔颜色
                self.painter.setPen(QPen(penColor, 1, Qt.SolidLine, Qt.RoundCap))    # 设置画笔,蓝色,1px大小,实线,圆形笔帽
                if self.isMousePressLeft is True:
                    pickRect = self.getRectangle(self.beginPosition, self.endPosition)   # 获得要截图的矩形框
                    self.captureImage = self.fullScreenImage.copy(pickRect)         # 捕获截图矩形框内的图片
                    self.painter.drawPixmap(pickRect.topLeft(), self.captureImage)  # 填充截图的图片
                    self.painter.drawRect(pickRect)     # 画矩形边框
                self.painter.end()  # 结束重绘

            def getRectangle(self, beginPoint, endPoint):
                pickRectWidth = int(qAbs(beginPoint.x() - endPoint.x()))
                pickRectHeight = int(qAbs(beginPoint.y() - endPoint.y()))
                pickRectTop = beginPoint.x() if beginPoint.x() < endPoint.x() else endPoint.x()
                pickRectLeft = beginPoint.y() if beginPoint.y() < endPoint.y() else endPoint.y()
                pickRect = QRect(pickRectTop, pickRectLeft, pickRectWidth, pickRectHeight)
                # 避免高度宽度为0时候报错
                if pickRectWidth == 0:
                    pickRect.setWidth(2)
                if pickRectHeight == 0:
                    pickRect.setHeight(2)

                return pickRect

            def saveImage(self):
                self.captureImage.save('picture.png', quality=95)   # 保存图片到当前文件夹中
                # ocr()

        if __name__ == "__main__":
            app = QApplication(sys.argv)
            window = CaptureScreen()
            window.show()
            sys.exit(app.exec_())
    
    def show_text(x):
        from fk import Ui_MainWindow
        from PyQt5.QtWidgets import QApplication, QMainWindow
        class MyMainForm(QMainWindow, Ui_MainWindow):
            def __init__(self, parent=None):
                super(MyMainForm, self).__init__(parent)
                self.setupUi(self)

                self.comboBox_1.addItems(data[0])
                self.comboBox_2.addItems(data[2])
                self.textEdit.setText(x)
                self.pushButton_1.clicked.connect(lambda:self.display_interface('search'))
                self.pushButton_2.clicked.connect(lambda:self.display_interface('translate'))
            def display_interface(self,m):
                x=self.textEdit.toPlainText()
                url=''
                if m=='search':
                    o_url=search_dic[self.comboBox_1.currentText()]
                    url=o_url.replace('%s', x)
                if m=='translate':
                    o_url=translate_dic[self.comboBox_2.currentText()]
                    url=o_url.replace('%s', x)
                self.webEngineView.setUrl(QUrl(url))
                self.webEngineView.setMinimumSize(QSize(0, 500))
                if m=='open':
                    webbrowser.open_new(srt(url))
                # else:
                    # QMessageBox.warning(self,"标题","",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

        if __name__ == "__main__":
            app = QApplication(sys.argv)
            myWin = MyMainForm()
            myWin.show()
            sys.exit(app.exec_())

def ocr(x):
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_gpu=False,lang="ch") # 首次执行会自动下载模型文件
    img_path = "picture.png"
    result = ocr.ocr(img_path)
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    x.put(txts)

if __name__ == "__main__":
    c = multiprocessing.Process(target=windows.clip)
    c.start()
    c.join()

    q = multiprocessing.Queue()
    o = multiprocessing.Process(target=ocr,args=(q,))
    o.start()
    o.join()
    show_text=''
    for i in q.get():
        show_text=show_text+i+'\n'
    windows.show_text(show_text)