import cv2
import argparse
import numpy as np
from matplotlib import pyplot as plt



parser = argparse.ArgumentParser(description='filter')
parser.add_argument('--blur', '-b', default=-1, type=int, help='ブラーフィルタ')
parser.add_argument('--gaussian', '-g', default=-1, type=int, help='ガウシアンフィルタ')
parser.add_argument('--median', '-m', default=-1, type=int, help='メディアンフィルタ')
parser.add_argument('--bilateral', '-v', default=-1, type=int, help='バイラテラルフィルタ')

args = parser.parse_args()



img = cv2.imread('logo.jpg')

if args.blur >= 0:
    blur = cv2.blur(img,(5,5))
    cv2.imwrite('blur.jpg', blur)

if args.gaussian >= 0:
    gaussian = cv2.GaussianBlur(img,(5,5),0)
    cv2.imwrite('gau_blur.jpg', gaussian)

if args.median >= 0:
    median = cv2.medianBlur(img,5)
    cv2.imwrite('median.jpg', median)

if args.bilateral >= 0:
    bilateral = cv2.bilateralFilter(img,9,75,75)
    cv2.imwrite('bilateral.jpg', bilateral)
