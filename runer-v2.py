# -*- coding: utf-8 -*-
import os
import tkinter
from tkinter import messagebox

from TkinterDnD2 import *
from tkinter import *

from paddleocr import parse_args, parse_lang, get_model_config, BASE_DIR, VERSION, SUPPORT_DET_MODEL, SUPPORT_REC_MODEL

global img_path
root = TkinterDnD.Tk()
root.withdraw()
root.title('AI汉字转unicode工具')
root.grid_rowconfigure(1, weight=1, minsize=80)
root.grid_columnconfigure(0, weight=1, minsize=100)

Label(root, text='拖拽图片到这里:').pack()
buttonbox = Frame(root)

file_data = ('R0lGODlhGAAYAKIAANnZ2TMzMwAAAJmZmf///yH5BAEAAAAALAA'
             'AAAAYABgAAAPACBi63IqgC4GiyxwogaAbKLrMgSKBoBoousyBogEACIGiyxwoKgGAECI'
             '4uiyCExMTOACBosuNpDoAGCI4uiyCIkREOACBosutSDoAgSI4usyCIjQAGCi63Iw0ACE'
             'oOLrMgiI0ABgoutyMNAAhKDi6zIIiNAAYKLrcjDQAISg4usyCIjQAGCi63Iw0AIGiiqP'
             'LIyhCA4CBosvNSAMQKKo4ujyCIjQAGCi63Iw0AIGiy81IAxCBpMu9GAMAgKPL3QgJADs'
             '=')
folder_data = ('R0lGODlhGAAYAKECAAAAAPD/gP///yH+EUNyZWF0ZWQgd2l0aCBHSU1QA'
               'CH5BAEKAAIALAAAAAAYABgAAAJClI+pK+DvGINQKhCyztEavGmd5IQmYJXmhi7UC8frH'
               'EL0Hdj4rO/n41v1giIgkWU8cpLK4dFJhAalvpj1is16toICADs=')

file_icon = PhotoImage(data=file_data)
# folder_icon = PhotoImage(data=folder_data)
folder_icon = PhotoImage(file="F:/0x4e0a.png")
# folder_icon = folder_icon.zoom(10)
# word_icon = PhotoImage(file="result/0x4e0b.png")
# global img_path
# word_icon = PhotoImage(file=img_path)
# word_icon.zoom()
py_icon = PhotoImage(file="result/0x4e0c.png")

canvas = Canvas(root, name='dnd_demo_canvas', bg='white', relief='sunken',
                bd=1, highlightthickness=1, takefocus=True, width=400, height=500)
# canvas.create_image(100,100,anchor=CENTER,image=folder_icon)
# canvas.grid(row=1, column=0, padx=5, pady=5, sticky='news')
canvas.pack()

# store the filename associated with each canvas item in a dictionary
canvas.filenames = {}
# store the next icon's x and y coordinates in a list
canvas.nextcoords = [50, 20]
# add a boolean flag to the canvas which can be used to disable
# files from the canvas being dropped on the canvas again
canvas.dragging = False

Label(root, text="识别汉字:").pack()
e1 = StringVar()
entry1 = Entry(root, textvariable=e1).pack()
Label(root, text="相似度:").pack()
e2 = StringVar()
entry2 = Entry(root, textvariable=e2).pack()
Label(root, text="unicode编码:").pack()
e3 = StringVar()
entry3 = Entry(root, textvariable=e3).pack()
Label(root, text="用时:").pack()
e4 = StringVar()
entry4 = Entry(root, textvariable=e4).pack()


def copyunicode():
    import pyperclip
    unicode = e3.get()
    pyperclip.copy(unicode)


def generateunicode():
    xinzi = e1.get()
    f = open("result.txt", "w", encoding='utf-8')
    for i in xinzi:
        f.write(i)
    f.close()

    import codecs
    import json

    f2 = codecs.open("result.txt", "r", 'utf-8')
    listimg = []
    for i in range(1):
        lines = f2.read(1)
        listimg.append(lines)
    print(len(listimg))
    dict = {'gbk': listimg}
    jStr = json.dumps(dict)
    print(jStr)

    jStr = jStr.encode()
    with open('result.json', 'wb')as f:
        f.write(jStr)

    result_unicode = json.dumps(listimg[-1]).replace('"', '')

    e1.set(xinzi)
    e2.set("")
    e3.set(result_unicode)
    e4.set("")


buttonbox.pack()
Button(buttonbox, text='复制unicode', command=copyunicode).pack(
    side=LEFT, padx=5)

buttonbox.pack()
Button(buttonbox, text='查找unicode', command=generateunicode).pack(
    side=LEFT, padx=6)


def add_file(filename):
    import os
    icon = file_icon
    global files
    global word_icon
    word_icon = PhotoImage(file=files[0])
    file2, type2 = os.path.splitext(filename)
    # print("file2:",file2)
    # print("type2:",type2)
    if os.path.isdir(filename):
        icon = folder_icon
    elif type2 == '.png' or type2 == '.jpg':
        icon = word_icon
    elif type2 == '.py' or type2 == '.PY':
        icon = py_icon

    id1 = canvas.create_image(250, 200,
                              image=icon, anchor='center', tags=('file',))
    id2 = canvas.create_text(220, 450,
                             text="", anchor='n',
                             justify='center', width=400)
    # id2 = canvas.create_text(canvas.nextcoords[0], canvas.nextcoords[1] + 400,
    #                          text=os.path.basename(filename), anchor='n',
    #                          justify='center', width=400)

    def select_item(ev):
        canvas.select_from(id2, 0)
        canvas.select_to(id2, 'end')

    canvas.tag_bind(id1, '<ButtonPress-1>', select_item)
    canvas.tag_bind(id2, '<ButtonPress-1>', select_item)
    canvas.filenames[id1] = filename
    canvas.filenames[id2] = filename
    if canvas.nextcoords[0] > 450:
        canvas.nextcoords = [50, canvas.nextcoords[1] + 80]
    else:
        canvas.nextcoords = [canvas.nextcoords[0] + 100, canvas.nextcoords[1]]

    import datetime
    startTime = datetime.datetime.now()
    # from paddleocr import PaddleOCR, draw_ocr
    # import os.path

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
    # zi_path = StringVar()
    global img_path
    # global files
    img_path = files[0]
    # img_path = "F:/pythonProject/PaddleOCR-release-2.3/result/0x4e0a.png"
    img_path = img_path.replace('\\', '/')
    print("imag_path:", img_path)
    # for i in range(0, 1076):
    #     img_path = './testimg/0_'+ str(i).zfill(4) +'.jpg'
    result = ocr.ocr(img_path, cls=True)
    print(result)
    if len(result) == 0:
        messagebox.showinfo(title='提示', message='无法识别!')

    for line in result:
        print(line)
    temp_accuary = line[1][1]

    # draw result
    from PIL import Image

    # image = Image.open(img_path).convert('RGB')
    # boxes = [lineimg[0] for lineimg in result]
    txts = [line[1][0] for line in result]
    # scores = [lineimg[1][1] for lineimg in result]
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
    listimg = []
    for i in range(1):
        lines = f2.read(1)
        listimg.append(lines)
    print(len(listimg))
    dict = {'gbk': listimg}
    jStr = json.dumps(dict)
    print(jStr)

    jStr = jStr.encode()
    with open('result.json', 'wb')as f:
        f.write(jStr)

    result_unicode = json.dumps(listimg[-1]).replace('"', '')

    e1.set(listimg[-1])
    e2.set(str(temp_accuary))
    e3.set(result_unicode)
    endTime = datetime.datetime.now()
    e4.set(endTime - startTime)

# drop methods

def drop_enter(event):
    event.widget.focus_force()
    print('Entering %s' % event.widget)
    return event.action


def drop_position(event):
    return event.action


def drop_leave(event):
    print('Leaving %s' % event.widget)
    return event.action


def drop(event):
    if canvas.dragging:
        # the canvas itself is the drag source
        return REFUSE_DROP
    if event.data:
        global files
        files = canvas.tk.splitlist(event.data)
        for f in files:
            add_file(f)
    return event.action


canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<DropEnter>>', drop_enter)
canvas.dnd_bind('<<DropPosition>>', drop_position)
canvas.dnd_bind('<<DropLeave>>', drop_leave)
canvas.dnd_bind('<<Drop>>', drop)


# drag methods

def drag_init(event):
    data = ()
    sel = canvas.select_item()
    if sel:
        # in a decent application we should check here if the mouse
        # actually hit an item, but for now we will stick with this
        data = (canvas.filenames[sel],)
        canvas.dragging = True
        return ((ASK, COPY), (DND_FILES, DND_TEXT), data)
    else:
        # don't start a dnd-operation when nothing is selected; the
        # return "break" here is only cosmetical, return "foobar" would
        # probably do the same
        return 'break'


def drag_end(event):
    # reset the "dragging" flag to enable drops again
    canvas.dragging = False


canvas.drag_source_register(1, DND_FILES)
canvas.dnd_bind('<<DragInitCmd>>', drag_init)
canvas.dnd_bind('<<DragEndCmd>>', drag_end)

root.update_idletasks()
root.deiconify()

root.mainloop()

input()
