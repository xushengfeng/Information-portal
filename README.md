# Information-portal

## 简介

这是类似于锤子大爆炸或小米传送门的Linux实现(当然差很远)

electron重写版本地址[eSearch](https://github.com/xushengfeng/eSearch)

目前可以实现的功能:

- [x]  从剪贴板识别
- [x]  OCR屏幕识别(用了PaddleOCR)
- [x]  鼠标旁边弹出窗口
- [x]  内嵌浏览器,可实现搜索和翻译,可选搜索引擎
- [x]  搜索或翻译的网页可以在浏览器打开
- [x]  小于20字时自动搜索或翻译
- [x]  搜索选中内容
- [x]  点击链接浏览器打开(暂时不支持链接编辑)
- [x]  中英判断切换模型
- [ ]  段落，空格识别
- [x]  用electron重写

## 安装和使用

下载本库并打开目录

运行OCR服务:`python ocr.py`

OCR模式:`python main.py`

剪贴板模式:`python main.py c`

### KDE桌面设置快捷键方法:

设置 > 快捷键 > 自定义快捷键

添加命令:`python 你下载本库的位置/main.py`后面添加`c`可实现剪贴板识别

## 其他

由于linux下选中文字便加入剪贴板,所以不加入自动判断是否选中某串字符

本机cv2和pyqt有很奇怪的冲突,所以选择本地OCR服务而不是内嵌,也方便加入其他OCR api

电脑可以自由选择编辑,所以暂时不加入分词

其他翻译或搜索引擎可以在`data.csv`中加入注意要把关键字替换成`%s`
