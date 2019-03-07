import numpy as np
import sys
import os
import cv2
from PIL import Image
from matplotlib.pyplot as plt
from bbox_toolbox import poly2bbox

def darknet_format(src,save_location):
    with open(src,"r+") as f:
        annos = f.readlines()
    for anno in annos:
        img_id = anno["image_id"]
        bboxes = []
        


def draw_bbox_test(img,bbox):
    fig,ax = plt.subplots(1,figsize=(15,15))
    ax.imshow(p)
    x,y,w,h = (*bbox)
    rect = patches.Rectangle((x*2048,y*2048),w*2048,h*2048,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    plt.show()

if __name__ == "__main__":