#-*- coding:utf-8 -*-
import glob
import datetime
import os
import copy
from tkinter import filedialog
import shutil
import cv2
import numpy as np
import csv
import const as cs


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
            print("error1:上書き保存しました！")

        os.chdir(data_path)
        os.mkdir('train_data')
        for i in range(len(COLOR_VALUE)):
            os.mkdir(str(COLOR_VALUE[i][0]))


class Image_processing_1:

    def __init__(self, name, img):
        self.name = name
        self.img = img

    def _thresh(self):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        img_thresh = cv2.threshold(img_gray, 30, 255, cv2.THRESH_BINARY)[1]
        img_thresh = cv2.bitwise_not(img_thresh)
        return img_thresh

    def cut(self):
        img_thresh_ = self._thresh()
        try:
            contours, _ = cv2.findContours(img_thresh_, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            max_cnt = max(contours, key=lambda x: cv2.contourArea(x))
            x,y,w,h = cv2.boundingRect(max_cnt)
            img1 = copy.deepcopy(self.img[y:y+h, x:x+w])

        except:
            img1 = copy.deepcopy(self.img)
            print("error2:対象がありません")

        # ----- フィルタリンング -----
        if cs.BLUR > 0:
            img1 = cv2.blur(img1,(5,5))
        elif cs.GAUSSIAN > 0:
            img1 = cv2.GaussianBlur(img1,(5,5),0)
        elif cs.MEDIAN > 0:
            img1 = cv2.medianBlur(img1,5)
        elif cs.BILATERAL > 0:
            img1 = cv2.bilateralFilter(img1,9,75,75)

        cv2.imwrite('train_data/'+str(self.name)+'_train.jpg', img1)
        if cs.MODE == 1:    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)  # HSV変換

        return img1


class Image_processing_2:

    def __init__(self, name, hsv_img, color, low, up):
        self.name = name
        self.hsv_img = hsv_img
        self.color = color
        self.low = low
        self.up = up

    def _pick_color(self):
        try:
            hsv_mask = cv2.inRange(self.hsv_img, self.low, self.up )
            contours, _ = cv2.findContours(hsv_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            num = len(contours)
            arr = np.empty((num,4), np.int32)
            for i in range(0, num):
                x, y, w, h = cv2.boundingRect(contours[i])
                arr[i] = np.array([x, y, w, h])

        except:
            hsv_mask = self.hsv_img
            arr = 0
            print("error3:対象がありません")

        return hsv_mask, arr

    def bounding(self):
        hsv_mask_, arr_ = self._pick_color()
        try:
            whiteArea = cv2.countNonZero(hsv_mask_)
            x_value = min(arr_[:,0])
            y_value = min(arr_[:,1])
            w_value = max(arr_[:,0]+arr_[:,2])-x_value
            h_value = max(arr_[:,1]+arr_[:,3])-y_value
            img2 = cv2.rectangle(copy.deepcopy(hsv_mask_),(x_value,y_value), (x_value+w_value, y_value+h_value),(255,255,255),1)
            cv2.imwrite(str(self.color)+'/'+str(self.name)+'_pick.jpg', img2)

        except:
            whiteArea = w_value = h_value = 0
            cv2.imwrite(str(self.color)+'/'+str(self.name)+'_pick.jpg', copy.deepcopy(hsv_mask_))
            print("error4:対象がありません")

        return whiteArea, w_value, h_value


def main():

    global COLOR_VALUE
    if cs.MODE == 0:
        COLOR_VALUE = cs.COLOR_BGR
        print("color : RGB")

    elif cs.MODE == 1:
        COLOR_VALUE = cs.COLOR_HSV
        print("color : HSV")

    # ----- 画像フォルダ選択＆データ保存フォルダ作成 -----
    SELECT_DIR = filedialog.askdirectory(initialdir = 'C:\\pg')
    data = Data_dir(SELECT_DIR)
    data.make_dir()
    lists = glob.glob(str(SELECT_DIR) + '/*.jpg')   # 画像リスト読み込み

    number = 0

    with open('data.csv','a') as f:
        writer = csv.writer(f)
        LABEL = ["ファイル名", "時間"]
        for i in range(len(COLOR_VALUE)):
            LABEL += [str(COLOR_VALUE[i][0])+"_面積", str(COLOR_VALUE[i][0])+"_横", str(COLOR_VALUE[i][0])+"_縦"]

        writer.writerow(LABEL)

        for list in lists:
            image = cv2.imread(list)    # 画像読み込み
            IMAGE_NAME = os.path.splitext(os.path.basename(list))[0]
            SAMPLING = cs.SAMPLING*number
            output_data = []
            output_data.extend([IMAGE_NAME, SAMPLING])

            # ----- 抽出範囲画像を作成 -----
            run_1 = Image_processing_1(IMAGE_NAME, image)
            use_image = run_1.cut()

            #----- 色抽出 -----
            run_2 = Image_processing_2(IMAGE_NAME, use_image, COLOR_VALUE[0][0], np.array(COLOR_VALUE[0][1]), np.array(COLOR_VALUE[0][2]))
            area, w_out, h_out = run_2.bounding()
            output_data.extend([area, w_out, h_out])

            run_2 = Image_processing_2(IMAGE_NAME, use_image, COLOR_VALUE[1][0], np.array(COLOR_VALUE[1][1]), np.array(COLOR_VALUE[1][2]))
            area, w_out, h_out = run_2.bounding()
            output_data.extend([area, w_out, h_out])

            run_2 = Image_processing_2(IMAGE_NAME, use_image, COLOR_VALUE[2][0], np.array(COLOR_VALUE[2][1]), np.array(COLOR_VALUE[2][2]))
            area, w_out, h_out = run_2.bounding()
            output_data.extend([area, w_out, h_out])


            writer.writerow(output_data)
            number = number+1

        print("Success!!")


if __name__ == "__main__":
    main()
