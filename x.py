import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage,QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import pyautogui
import pyperclip
from paddleocr import PaddleOCR, draw_ocr

# 划词
def wording():
    original_text = pyperclip.paste()
    pyautogui.hotkey('ctrl','c')
    text = pyperclip.paste()
    if text==original_text: # 选区是否变动
        print('kobg')
    else:
        print(text)

# wording()

def orc():
    ocr = PaddleOCR(use_gpu=False,lang="ch") # 首次执行会自动下载模型文件
    img_path = "aipeom.png"
    result = ocr.ocr(img_path)
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]