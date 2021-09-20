import web
from paddleocr import PaddleOCR
import json
import base64
import cv2
import numpy as np

def ocr(data):
    ocr = PaddleOCR(use_gpu=False,lang="ch") # 首次执行会自动下载模型文件
    image_string = data
    img_data = base64.b64decode(image_string)
    nparr = np.fromstring(img_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = ocr.ocr(img_np)
    dic={}
    dic["boxes"] = [line[0] for line in result]
    dic["txts"] = [line[1][0] for line in result]
    # dic["scores"] = [line[1][1] for line in result]
    return dic


urls = (
    '/', 'index'
)

class index:
    def POST(self):
        data = web.data()
        return json.dumps((ocr(data)))
        

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()