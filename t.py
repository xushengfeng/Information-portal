import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
 
################################################
#######创建主窗口
################################################
class MainWindow(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.setWindowTitle('My Browser')
    self.showMaximized()
 
    self.webview = WebEngineView()
    self.webview.load(QUrl("https://www.baidu.com"))
    self.setCentralWidget(self.webview)
 
################################################
#######创建浏览器
################################################
class WebEngineView(QWebEngineView):
  # 重写createwindow()
  def createWindow(self, QWebEnginePage_WebWindowType):
    return self
 
################################################
#######程序入门
################################################
if __name__ == "__main__":
  app = QApplication(sys.argv)
  w = MainWindow()
  w.show()
  sys.exit(app.exec_())
