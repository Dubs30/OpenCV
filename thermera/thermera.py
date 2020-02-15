#-*- coding:utf-8 -*-
import sys
import glob
import datetime
import os
import copy
from tkinter import filedialog
import shutil
import cv2
import numpy as np
import csv
import const_gui as csg
import copy


class Data_dir:

    def __init__(self, fld):
        self.fld = fld


    def make_dir(self):
        now = datetime.datetime.now()
        data_path = str(self.fld) + '/{0:%m%d}_{0:%H%M}'.format(now)
        try:
            os.mkdir(data_path)

        except:
            shutil.rmtree(data_path)
            os.mkdir(data_path)
            print("上書き保存しました！")

        os.chdir(data_path)
        os.mkdir('Train_data')
        [os.mkdir(str(COLOR_VALUE[i][0]))for i in range(len(COLOR_VALUE))]



class ImageProcessing_1:

    def __init__(self, img):
        self.img = img


    def _mouse_callback(self, event, x, y, flags, param):
        global ix, iy, width, height, drawing

        if event == cv2.EVENT_MOUSEMOVE:
            if(drawing == True):
                width = x-ix
                height = y-iy

        elif event == cv2.EVENT_LBUTTONDOWN:
            drawing == True
            ix, iy = x, y
            width = height = 0

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            if(width<0):
                ix += width
                width *= -1
            if(height<0):
                iy += height
                height *= -1


    def first_cut(self):
        global isFirst, ix, iy, width, height, drawing
        if isFirst == True:
            source_window = "draw_rectangle"
            temp = self.img.copy()
            cv2.namedWindow(source_window)
            cv2.setMouseCallback(source_window, self._mouse_callback)

            while(1):
                cv2.imshow(source_window, temp)
                if(drawing):
                    temp = self.img.copy()
                    cv2.rectangle(temp, (ix, iy), (ix+width, iy+height), (0, 255, 0), 1)

                k = cv2.waitKey(1)&0xFF
                if k == 13: # Enter key
                    cv2.destroyAllWindows()
                    break
                elif k == 27:   # Esc key
                    sys.exit()


    def _thresh(self, cut_img):
        img_gray = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
        img_thresh = cv2.threshold(img_gray, int(csg.GrayLow), int(csg.GrayUp), cv2.THRESH_BINARY)[1]
        # img_thresh = cv2.bitwise_not(img_thresh)
        return img_thresh


    def cut(self):
        if isFirst == True:
            self.first_cut()

        # img_ = self.img[iy:iy+height, ix:ix+width]
        img_ = self.img
        
        img_thresh_ = self._thresh(img_)
        Total_Area = cv2.countNonZero(img_thresh_)

        try:
            contours, _ = cv2.findContours(img_thresh_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_cnt = max(contours, key=lambda x: cv2.contourArea(x))
            x,y,w,h = cv2.boundingRect(max_cnt)
            img1 = copy.deepcopy(self.img[y:y+h, x:x+w])
            sputter_num = len(contours)-1

            if sputter_num>0:
                max_img = copy.deepcopy(img_thresh_[y:y+h, x:x+w])
                max_area = cv2.countNonZero(max_img)
                sputter_area = Total_Area - max_area
            else:
                sputter_area = 0

        except:
            img1 = copy.deepcopy(img_)
            sputter_num = sputter_area = 0

        return Total_Area, img1, sputter_num, sputter_area



class ImageProcessing_2:

    def __init__(self, name, use_img, color, low, up):
        self.name = name
        self.use_img = use_img
        self.color = color
        self.low = low
        self.up = up


    def _pick_color(self):
        try:
            img_mask = cv2.inRange(self.use_img, self.low, self.up )
            contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            num_contours = len(contours)
            arr = np.empty((num_contours,4), np.int32)
            for i in range(0, num_contours):
                x, y, w, h = cv2.boundingRect(contours[i])
                arr[i] = np.array([x, y, w, h])

        except:
            img_mask = self.use_img
            arr = 0

        return img_mask, arr


    def bounding(self):
        img_mask_, arr_ = self._pick_color()
        try:
            whiteArea = cv2.countNonZero(img_mask_)
            x_value = min(arr_[:,0])
            y_value = min(arr_[:,1])
            w_value = max(arr_[:,0]+arr_[:,2])-x_value
            h_value = max(arr_[:,1]+arr_[:,3])-y_value
            # img2 = cv2.rectangle(copy.deepcopy(img_mask_),(x_value,y_value), (x_value+w_value, y_value+h_value),(255,255,255),1)
            # cv2.imwrite(str(self.color)+'/'+str(self.name)+'_pick.jpg', img2)
            cv2.imwrite(str(self.color)+'/'+str(self.name)+'_pick.jpg', img_mask_)

        except:
            whiteArea = w_value = h_value = 0
            cv2.imwrite(str(self.color)+'/'+str(self.name)+'_pick.jpg', copy.deepcopy(img_mask_))

        return whiteArea, w_value, h_value


def save_all_frames(videoPath, ext='jpg'):
    cap = cv2.VideoCapture(videoPath)
    if not cap.isOpened():
        return

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    n = 0
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("Img_data/"+"{}_{}.{}".format("data", str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return

def img_option(img1):
        # ----- フィルタリンング -----
        if int(csg.BLUR) > 0:
            img1 = cv2.blur(img1,(5,5))
            if isFirst == True:
                print("use BLUR Filter")

        elif int(csg.GAUSSIAN) > 0:
            img1 = cv2.GaussianBlur(img1,(5,5),0)
            if isFirst == True:
                print("use GAUSSIAN Filter")

        elif int(csg.MEDIAN) > 0:
            img1 = cv2.medianBlur(img1,5)
            if isFirst == True:
                print("use MEDIAN Filter")

        elif int(csg.BILATERAL) > 0:
            img1 = cv2.bilateralFilter(img1, 9, 75, 75)
            if isFirst == True:
                print("use BILATERAL Filter")

        if int(csg.colorMode) == 1:    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)  # HSV変換

        return img1


def main():

    global COLOR_VALUE, ix, iy, width, height, drawing, isFirst
    isFirst = True
    drawing = False
    ix, iy, width, height = -1, -1, 0, 0

    if int(csg.colorMode) == 0:
        COLOR_VALUE = csg.COLOR_BGR

    elif int(csg.colorMode) == 1:
        COLOR_VALUE = csg.COLOR_HSV

    # ----- 画像フォルダ選択＆データ保存フォルダ作成 -----
    SELECT_DIR = filedialog.askdirectory(initialdir = 'C:\\pg')
    data = Data_dir(SELECT_DIR)
    data.make_dir()

    ex_path = glob.glob(str(SELECT_DIR)+'/*.*')[0]
    EXTENSION = os.path.splitext(os.path.basename(ex_path))[1]


    print("START")
    print("-------")

    if EXTENSION in {'.jpg', '.BMP'}:
        lists = glob.glob(str(SELECT_DIR) + '/*'+ str(EXTENSION))

    elif EXTENSION in {'.avi', '.mp4'}:
        os.mkdir("Img_data")
        video_path = glob.glob(str(SELECT_DIR) + '/*'+ str(EXTENSION))[0]
        save_all_frames(video_path)
        lists = glob.glob('Img_data/*.*')

    else:
        print(読み込みファイルを認識できません)
        sys.exit()

    print("読み込みファイル拡張子：{}".format(EXTENSION))
    print("サンプリング周期:{}".format(csg.SAMPLING))

    if int(csg.colorMode) == 0:
        print("色抽出：RGB")
    elif int(csg.colorMode) == 1:
        print("色抽出：HSV")


    with open('data.csv','w', newline='') as f:
        writer = csv.writer(f)

        LABEL = ["ファイル名", "時間", "全面積", "スパッタ数", "スパッタ面積"]
        for i in range(len(COLOR_VALUE)):
            LABEL += [str(COLOR_VALUE[i][0])+"_面積", str(COLOR_VALUE[i][0])+"_横", str(COLOR_VALUE[i][0])+"_縦"]

        writer.writerow(LABEL)


        for num, list in enumerate(lists):
            image = cv2.imread(list)    # 画像読み込み
            IMAGE_NAME = os.path.splitext(os.path.basename(list))[0]
            output_data = []
            SAMPLING = float(csg.SAMPLING)*num
            output_data.extend([IMAGE_NAME, SAMPLING])

            # ----- 抽出範囲画像を作成 -----
            run_1 = ImageProcessing_1(image)
            totalArea, image1, sputterNum, sputterArea = run_1.cut()
            output_data.extend([totalArea, sputterNum, sputterArea])
            use_image = img_option(image1)
            isFirst = False

            cv2.imwrite("Train_data/"+str(IMAGE_NAME)+"_train.jpg", use_image)


            #----- 色抽出 -----
            for i in range(len(COLOR_VALUE)):
                run_2 = ImageProcessing_2(IMAGE_NAME, use_image, COLOR_VALUE[i][0], np.array(COLOR_VALUE[i][1]), np.array(COLOR_VALUE[i][2]))
                area, w_out, h_out = run_2.bounding()
                output_data.extend([area, w_out, h_out])

            writer.writerow(output_data)

        print("------")
        print("End")


if __name__ == "__main__":
    main()
