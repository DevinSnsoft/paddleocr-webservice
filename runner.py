from tkinter import *
import win32ui
import win32con
import tkinter.messagebox

from paddleocr import parse_args, parse_lang, get_model_config, BASE_DIR, VERSION, SUPPORT_DET_MODEL, SUPPORT_REC_MODEL

file_type = 'All File(*.*)|*.*|' \
            'Html File(*.html)|*.html|' \
            'Image File(*.bmp .jpg .png)|*.png;*.jpg;*.bmp|' \
            'python File(*.py .pyc)|*.py;*.pyc|' \
            '|'

API_flag = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST

entrypath = ""


def Win_Open_File():
    dlg = win32ui.CreateFileDialog(1, None, None, API_flag, file_type)  # 指定为打开文件窗口
    dlg.SetOFNInitialDir("C:")
    dlg.DoModal()
    path = dlg.GetPathName()
    entrypath.set(path)
    print(path)


def Win_Save_File():  # 保存文件时，文件后缀需要另处理
    print("Save File\n")
    dlg = win32ui.CreateFileDialog(0, None, None, API_flag, file_type)  # 指定为保存文件窗口
    dlg.SetOFNInitialDir('C:')  # 默认打开的位置
    dlg.DoModal()
    path = dlg.GetPathName()  # 获取打开的路径
    entrypath.set(path)
    print(path)


def closeWin():
    MainWindows.destroy()


def distinguish():
    tkinter.messagebox.showinfo('识别结果', '333333333333')


MainWindows = Tk()  # 主窗体
MainWindows.title("AI汉字识别工具")

Button(text='上传图片', command=Win_Open_File).pack(ipadx=10, anchor="center")
entrypath = StringVar()
e = Entry(MainWindows, textvariable=entrypath, width=50).pack()
Button(text='开始识别', command=closeWin).pack()

MainWindows.geometry("500x300")
MainWindows.mainloop()

import datetime
from paddle import *
startTime = datetime.datetime.now()
# from paddleocr import PaddleOCR, draw_ocr
# import os.path

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`


import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import sys

__dir__ = os.path.dirname(__file__)
sys.path.append(os.path.join(__dir__, ''))

import cv2
import logging
import numpy as np
from pathlib import Path

from tools.infer import predict_system
from ppocr.utils.logging import get_logger

logger = get_logger()
from ppocr.utils.utility import check_and_read_gif
from ppocr.utils.network import maybe_download, download_with_progressbar, confirm_model_dir_url
class PaddleOCR(predict_system.TextSystem):
    def __init__(self, **kwargs):
        """
        paddleocr package
        args:
            **kwargs: other params show in paddleocr --help
        """
        params = parse_args(mMain=False)
        params.__dict__.update(**kwargs)
        if not params.show_log:
            logger.setLevel(logging.INFO)
        self.use_angle_cls = params.use_angle_cls
        lang, det_lang = parse_lang(params.lang)

        # init model dir
        det_model_config = get_model_config(params.version, 'det', det_lang)
        params.det_model_dir, det_url = confirm_model_dir_url(
            params.det_model_dir,
            os.path.join(BASE_DIR, VERSION, 'ocr', 'det', det_lang),
            det_model_config['url'])
        rec_model_config = get_model_config(params.version, 'rec', lang)
        params.rec_model_dir, rec_url = confirm_model_dir_url(
            params.rec_model_dir,
            os.path.join(BASE_DIR, VERSION, 'ocr', 'rec', lang),
            rec_model_config['url'])
        cls_model_config = get_model_config(params.version, 'cls', 'ch')
        params.cls_model_dir, cls_url = confirm_model_dir_url(
            params.cls_model_dir,
            os.path.join(BASE_DIR, VERSION, 'ocr', 'cls'),
            cls_model_config['url'])
        # download model
        maybe_download(params.det_model_dir, det_url)
        maybe_download(params.rec_model_dir, rec_url)
        maybe_download(params.cls_model_dir, cls_url)

        if params.det_algorithm not in SUPPORT_DET_MODEL:
            logger.error('det_algorithm must in {}'.format(SUPPORT_DET_MODEL))
            sys.exit(0)
        if params.rec_algorithm not in SUPPORT_REC_MODEL:
            logger.error('rec_algorithm must in {}'.format(SUPPORT_REC_MODEL))
            sys.exit(0)

        if params.rec_char_dict_path is None:
            params.rec_char_dict_path = str(
                Path(__file__).parent / rec_model_config['dict_path'])

        print(params)
        # init det_model and rec_model
        super().__init__(params)

    def ocr(self, img, det=True, rec=True, cls=True):
        """
        ocr with paddleocr
        args：
            img: img for ocr, support ndarray, img_path and list or ndarray
            det: use text detection or not, if false, only rec will be exec. default is True
            rec: use text recognition or not, if false, only det will be exec. default is True
        """
        assert isinstance(img, (np.ndarray, list, str))
        if isinstance(img, list) and det == True:
            logger.error('When input a list of images, det must be false')
            exit(0)
        if cls == True and self.use_angle_cls == False:
            logger.warning(
                'Since the angle classifier is not initialized, the angle classifier will not be uesd during the forward process'
            )

        if isinstance(img, str):
            # download net image
            if img.startswith('http'):
                download_with_progressbar(img, 'tmp.jpg')
                img = 'tmp.jpg'
            image_file = img
            img, flag = check_and_read_gif(image_file)
            if not flag:
                with open(image_file, 'rb') as f:
                    np_arr = np.frombuffer(f.read(), dtype=np.uint8)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if img is None:
                logger.error("error in loading image:{}".format(image_file))
                return None
        if isinstance(img, np.ndarray) and len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if det and rec:
            dt_boxes, rec_res = self.__call__(img, cls)
            return [[box.tolist(), res] for box, res in zip(dt_boxes, rec_res)]
        elif det and not rec:
            dt_boxes, elapse = self.text_detector(img)
            if dt_boxes is None:
                return None
            return [box.tolist() for box in dt_boxes]
        else:
            if not isinstance(img, list):
                img = [img]
            if self.use_angle_cls and cls:
                img, cls_res, elapse = self.text_classifier(img)
                if not rec:
                    return cls_res
            rec_res, elapse = self.text_recognizer(img)
            return rec_res


ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # need to run only once to download and load model into memory
# img_path = './result/0x4e0a.png'
img_path = entrypath.get()
img_path = img_path.replace('\\','/')
print("imag_path:", img_path)
# for i in range(0, 1076):
#     img_path = './testimg/0_'+ str(i).zfill(4) +'.jpg'
result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)
temp_accuary = line[1][1]

# draw result
from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/chinese_cht.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.png')
# data_dir = os.path.join('result.txt')

f = open("result.txt", "w", encoding='utf-8')
for i in txts:
    f.write(i)
f.close()

import codecs
import json

f2 = codecs.open("result.txt", "r", 'utf-8')
list = []
for i in range(1):
    lines = f2.read(1)
    list.append(lines)
print(len(list))
dict = {'gbk': list}
jStr = json.dumps(dict)
print(jStr)

jStr = jStr.encode()
with open('result.json', 'wb')as f:
    f.write(jStr)

print(list[-1])
temp = json.dumps(list[-1]).replace('"', '')

print(temp)

ResultWindows = Tk()  # 主窗体
ResultWindows.title("AI汉字识别工具")
Label(ResultWindows, text="识别汉字:").grid(row=0)
Label(ResultWindows, text="识别概率:").grid(row=1)
Label(ResultWindows, text="unicode编码:").grid(row=2)
Label(ResultWindows, text="用时:").grid(row=3)

e1 = Entry(ResultWindows)
e2 = Entry(ResultWindows)
e3 = Entry(ResultWindows)
e4 = Entry(ResultWindows)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

e1.insert(0, list[-1])
e2.insert(0, str(temp_accuary))
e3.insert(0, temp)
endTime = datetime.datetime.now()
e4.insert(0, endTime-startTime)
ResultWindows.geometry("500x300")
ResultWindows.mainloop()


