import numpy as np
import sys
import os
import cv2
from PIL import Image
from matplotlib.pyplot as plt
from bbox_toolbox import poly2bbox
import csv

def darknet_format(src,name_location,save_location):
    classes = {}
    abandon_class = {}
    with open(src,"r+") as f:
        annos = f.readlines()
    with open(name_location) as f:
        for i,name in enumerate(f):
            if name == '':
                continue
            else:
                classes[name] = i
        print(len(classes)) 
    for anno in annos:
        img_id = anno["image_id"]
        bboxes = []
        for v,t in zip(anno["polygon"],anno["text"]):
            x_c,y_c,w,h = poly2bbox(v, 2048)
            try:
                cls = classes[t]
                bboxes.append([t,x_c,y_c,w,h])
            except:
                try:
                    abandon_class[t] += 1
                except:
                    abandon_class[t] = 1
        fname = os.path.join(save_location,img_id) + ".txt"
        with open(fname,"w+",newline="") as f:
            w = csv.writer(f,delimiter=' ')
            for b in bboxes:
                w.writerow(b)

        


def draw_bbox_test(img,bbox):
    fig,ax = plt.subplots(1,figsize=(15,15))
    ax.imshow(p)
    x,y,w,h = (*bbox)
    rect = patches.Rectangle((x*2048,y*2048),w*2048,h*2048,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    plt.show()

if __name__ == "__main__":