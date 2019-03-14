import numpy as np
import sys
import os
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from bbox_toolbox import poly2bbox
import csv
from tqdm import tqdm
import json

def darknet_format_anno(src,name_location,save_location,threshold):
    classes = {}
    abandon_class = {}
    with open(src,"r+") as f:
        annos = f.readlines()
    with open(name_location) as f:
        for i,name in enumerate(f):
            if name == '':
                continue
            else:
                classes[name.strip()] = i
    os.makedirs(save_location,exist_ok=True)
    for anno in tqdm(annos):
        anno = json.loads(anno)
        img_id = anno["image_id"]
        ignored = anno["ignore"]
        file_name = anno["file_name"]
        bboxes = []
        fname = os.path.join(save_location,img_id) + ".txt"

        for text in anno["annotations"]:
            for character in text:
                x_c,y_c,w,h = poly2bbox(character["polygon"], 2048)
                
                if x_c > 1 or y_c > 1 or w < threshold or h < threshold:
                    continue
                
                else:
                    try:
                        cls = classes[character["text"]]
                        bboxes.append([cls,x_c,y_c,w,h])
                    except:
                        bboxes.append([1000,x_c,y_c,w,h])
        with open(fname,"w",newline="") as f:
            w = csv.writer(f,delimiter=' ')
            for b in bboxes:
                w.writerow(b)

def darknet_format_txt(src,name_location,img_location,txt_name):
    
    files = os.listdir(img_location)
    imgs = []
    classes = []
    with open(src,"r+") as f:
        annos = f.readlines()
    with open(name_location) as f:
        for i,name in enumerate(f):
            if name == '':
                continue
            else:
                classes.append(name.strip())
    for anno in tqdm(annos):
        anno = json.loads(anno)
        img_id = anno["image_id"]
        ignored = anno["ignore"]
        file_name = anno["file_name"]
        num = 0
        for text in anno["annotations"]:
            for character in text:
                if character["text"] in classes:
                    num +=1
        if num > 0:
            imgs.append(file_name)
    qualified = [x for x in files if x in imgs]
    qualified = [os.path.join(img_location,x) for x in qualified]

    with open(txt_name,"a+") as f:
        for line in qualified:
            f.write(line+"\n")
            

def draw_bbox_test(img,bbox):
    fig,ax = plt.subplots(1,figsize=(15,15))
    ax.imshow(p)
    x,y,w,h = bbox
    rect = patches.Rectangle((x*2048,y*2048),w*2048,h*2048,linewidth=1,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    plt.show()

if __name__ == "__main__":

    train_src = "/home/ej/projects/CTW-Pytorch/annotations/train.jsonl" 
    valid_src = "/home/ej/projects/CTW-Pytorch/annotations/val.jsonl"
    name = "/home/ej/projects/CTW-Pytorch/YOLOv3/data/ctw1000.names"
    bbox_save = "/home/ej/projects/CTW-Pytorch/YOLOv3/data/trainval/labels"
    train_img = "/media/ej/eb1186dc-fe0d-4742-9219-5766b227e606/ej/ctw/data/trainval/images"
    val_image = "/media/ej/eb1186dc-fe0d-4742-9219-5766b227e606/ej/ctw/data/trainval/images"
    train_text = "train1000.txt"
    val_text = "val1000.txt"
    threshold = 0.008

    darknet_format_anno(train_src,name,bbox_save,threshold)
    darknet_format_anno(valid_src,name,bbox_save,threshold)
    darknet_format_txt(train_src,name,train_img,train_text)
    darknet_format_txt(valid_src,name,val_image,val_text)