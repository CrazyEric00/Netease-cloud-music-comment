from tkinter import *
import time
import numpy as np
import pandas as pd
import requests
import json
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from scipy.misc import imread


class MY_GUI():
    def __init__(self, init_name):
        self.init_name = init_name

    def get_comments(musicid, limit, offset):
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}?limit={}&offset={}'.format(musicid, limit,
                                                                                                  offset)
        payload = {
            'params': '4hmFbT9ZucQPTM8ly/UA60NYH1tpyzhHOx04qzjEh3hU1597xh7pBOjRILfbjNZHqzzGby5ExblBpOdDLJxOAk4hBVy5/XNwobA+JTFPiumSmVYBRFpizkWHgCGO+OWiuaNPVlmr9m8UI7tJv0+NJoLUy0D6jd+DnIgcVJlIQDmkvfHbQr/i9Sy+SNSt6Ltq',
            'encSecKey': 'a2c2e57baee7ca16598c9d027494f40fbd228f0288d48b304feec0c52497511e191f42dfc3e9040b9bb40a9857fa3f963c6a410b8a2a24eea02e66f3133fcb8dbfcb1d9a5d7ff1680c310a32f05db83ec920e64692a7803b2b5d7f99b14abf33cfa7edc3e57b1379648d25b3e4a9cab62c1b3a68a4d015abedcd1bb7e868b676'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            'Referer': 'http://music.163.com/song?id={}'.format(musicid),
            'Host': 'music.163.com',
            'Origin': 'http://music.163.com'
        }
        response = requests.post(url=url, headers=headers, data=payload)
        data = json.loads(response.text)
        contents = []
        for s in data['comments']:
            contents.append(s['content'])
        return contents

    # 设置窗口
    def set(self):
        self.init_name.title("网易云音乐爬虫")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')#290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"
        # self.init_window_name.attributes("-alpha",0.9)       #虚化，值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_name, text="日志")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Entry(self.init_name, width=67,height=15,borderwidth=3)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        # 按钮
        self.button = Button(self.init_name, text="字符串转MD5", bg="lightblue", width=10,
                                              )  # 调用内部方法 加()为直接调用
        self.button.grid(row=1, column=11)




def start():
    init = Tk()  # 实例化出一个父窗口
    my_gui = MY_GUI(init)
    # 设置根窗口默认属性
    my_gui.set()
    init.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if __name__=='__main__':
    start()
