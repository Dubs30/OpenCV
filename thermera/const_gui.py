#-*- coding:utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import ttk


def end_config():
    global BLUR, GAUSSIAN, MEDIAN, BILATERAL, SAMPLING, GrayLow, GrayUp, colorMode, root


    SAMPLING = sampling.get()
    GrayLow = gray_low.get()
    GrayUp = gray_up.get()
    colorMode = color_mode.get()
    root.quit()

    if BLUR.get() == True:
        BLUR = 1
    else:
        BLUR = 0

    if GAUSSIAN.get() == True:
        GAUSSIAN = 1
    else:
        GAUSSIAN = 0

    if MEDIAN.get() == True:
        MEDIAN = 1
    else:
        MEDIAN = 0

    if BILATERAL.get() == True:
        BILATERAL = 1
    else:
        BILATERAL = 0



# ----- BGRで色の範囲を設定 :mode=0 -----
COLOR_BGR = [["Red", [0, 0, 230], [20, 20, 255]],
            ["Green", [0, 230, 0], [20, 255, 20]],
            ["Blue", [230, 0, 0], [255, 20, 20]]
            ]

# ----- HSVで色の範囲を設定 :mode=1 -----
COLOR_HSV = [["Blue", [230, 0, 0], [255, 20, 20]],
            ["Red", [0, 0, 230], [20, 20, 255]],
            ["Green", [0, 230, 0], [20, 255, 20]]
            ]


global BLUR, GAUSSIAN, MEDIAN, BILATERAL, SAMPLING, GrayLow, GrayUp, colorMode, root

root = Tk()
root.title('初期設定')
# root.resizable(False, False)
frame1 = ttk.Frame(root, padding=10)
frame1['relief'] = 'sunken'
frame1['borderwidth'] = 5
frame1.grid()


# ラベル設定
label1 = ttk.Label(frame1, text='サンプリング周期：', padding=(5,5))
label1.grid(row=0,column=0,sticky=E)
label2 = ttk.Label(frame1, text='グレースケール：', padding=(5,5))
label2.grid(row=1,column=0,sticky=E)
label2 = ttk.Label(frame1, text='下限', padding=(5,5))
label2.grid(row=1,column=1,sticky=E)
label3 = ttk.Label(frame1, text='上限', padding=(5,5))
label3.grid(row=1,column=3,sticky=E)
label4 = ttk.Label(frame1, text='色抽出：', padding=(5,5))
label4.grid(row=2,column=0,sticky=E)
label5 = ttk.Label(frame1, text='画像フィルタ：', padding=(5,5))
label5.grid(row=3,column=0,sticky=E)


# サンプリング周期
sampling = StringVar()
sampling_entry = ttk.Entry(frame1, textvariable=sampling, width=10 )
sampling_entry.insert(tk.END, 0.01)
sampling_entry.grid(row=0,column=1)

# グレースケール値
gray_low = StringVar()
gray_low_entry = ttk.Entry(frame1, textvariable=gray_low, width=10 )
gray_low_entry.insert(tk.END, 10)
gray_low_entry.grid(row=1,column=2,sticky='ew')

gray_up = StringVar()
gray_up_entry = ttk.Entry(frame1, textvariable=gray_up, width=10 )
gray_up_entry.insert(tk.END, 255)
gray_up_entry.grid(row=1,column=4,sticky='ew')

# 色抽出
color_mode = tk.IntVar()
cm1 = ttk.Radiobutton(frame1, value=0, padding=5, text='RGB', variable=color_mode)
cm1.grid(row=2,column=1)

cm2 = ttk.Radiobutton(frame1, value=1, padding=5, text='HSV', variable=color_mode)
cm2.grid(row=2,column=2)
cm2.state(['selected'])

# 画像フィルタ
BLUR = tk.BooleanVar()
BLUR.set(False)
GAUSSIAN = tk.BooleanVar()
GAUSSIAN.set(False)
MEDIAN = tk.BooleanVar()
MEDIAN.set(False)
BILATERAL = tk.BooleanVar()
BILATERAL.set(False)


fl1 = ttk.Checkbutton(frame1, padding=5, text='ブラーフィルタ', variable=BLUR)
fl1.grid(row=3,column=1)

fl2 = ttk.Checkbutton(frame1, padding=5, text='ガウシアンフィルタ', variable=GAUSSIAN )
fl2.grid(row=3,column=2)

fl3 = ttk.Checkbutton(frame1, padding=5, text='メディアンフィルタ', variable=MEDIAN)
fl3.grid(row=3,column=3)

fl4 = ttk.Checkbutton(frame1, padding=5, text='バイラテラルフィルタ', variable=BILATERAL)
fl4.grid(row=3,column=4)



# 終了ボタン
frame2 = ttk.Frame(frame1, padding=(0,5))
frame2.grid(row=4,column=2,sticky=W)

button1 = ttk.Button(frame2, text='設定完了',command=end_config)
button1.pack(side=LEFT)

root.mainloop()
