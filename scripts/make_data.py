from PIL import Image
import numpy as np
import glob
import pytesseract
import argparse
import os
import os.path
import pickle
import time

klst = ["ALK","LR03","LR6","1.5V","1,5V","NI-CD","NICD","NIMH","NI-MH","MHNI","MH-NI","HR14","HR20","LI-ION","LIION","LITHIUM","3,7V","3.7V"]

def get_boxes(in_lst):
    box_lst = []
    print("Start text recognition")
    print("======================")
    for im in in_lst:
        if os.path.isfile(im):
            for degree in [0, 90, 180, 270]:
                s_time = time.time()
                print(im + " " + str(degree))
                box_lst.append((im, pytesseract.image_to_boxes(Image.open(im).rotate(degree,expand=True)),degree))
                print("Time: " + str(round(time.time()-s_time, 2)) + 'sec')
    print("======================")
    print("Finnish")
    return box_lst

#to arrange output data
def arrange_data(box_lst, klst):
    pad = 10
    coordinates = []
    for im, line, degree in box_lst:
        line_lst = line.split("\n")
        line_lst2 = []
        for line1 in line_lst:
            line_lst2.append(line1.upper().split(" "))
        array = np.array(line_lst2).T
        txt = ''
        for w in array[0]:
            txt += w
        indexs = []
        key_lst = []
        for keyword in klst:
            l = len(keyword)
            x = txt.find(keyword)
            if x != -1:
                indexs.append((x, x+l-1))
                key_lst.append(keyword)
        if indexs != []:
            im_s = Image.open(im).rotate(degree, expand=True)
            x, y = im_s.size
            coordinate = []
            for s, e in indexs:
                x_1 = array[1][s].astype(np.int) - pad
                y_1 = y - (array[2][s].astype(np.int) - pad)
                x_2 = array[3][e].astype(np.int) + pad
                y_2 = y - (array[4][e].astype(np.int) + pad)
                if x_1 < 0:
                    x_1 = 0
                if y_2 < 0:
                    y_2 = 0
                if x_2 > x:
                    x_2 = x
                if y_1 > y:
                    y_1 = y
                x1 = min(x_1, x_2)
                x2 = max(x_1, x_2)
                y2 = min(y_1, y_2)
                y1 = max(y_1, y_2)
                w = x2 - x1
                h = y1 - y2
                if (x1 != 0) & (y2 != 0) & (x2 != x) & (y1 != y) & (w > 20) & (h > 20):
                    coordinate.append((x1,y2,x2,y1))
            if coordinate != []:
                coordinates.append((im, coordinate, key_lst, degree))
    return coordinates

#to save coordinates
def save_coordinates(coordinates, outpath):
    f = open(outpath, 'wb')
    pickle.dump(coordinates, f, protocol=2)
    f.close()
