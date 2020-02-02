#-*- coding:utf-8 -*-
import numpy as np
import cv2

img = cv2.imread('logo.jpg',1)  # カラー画像
# img = cv2.imread('logo.jpg',0)  # グレースケール画像
# img = cv2.imread('logo.jpg',-1)  # アルファチャンネルあり画像

cv2.imshow('image',img) # 表示
cv2.waitKey(0)  # キーボード入力待ち

cv2.imwrite('out.png',img)    # 保存
img = cv2.destroyAllWindows()   # window閉じる
