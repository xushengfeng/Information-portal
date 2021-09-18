import keyboard
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage,QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import pyautogui
import pyperclip


# 划词
def wording():
    original_text = pyperclip.paste()
    pyautogui.hotkey('ctrl','c')
    text = pyperclip.paste()
    if text==original_text: # 选区是否变动
        print('kobg')
    else:
        print(text)

wording()
