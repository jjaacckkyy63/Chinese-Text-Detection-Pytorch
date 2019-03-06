from __future__ import division

import collections
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from __future__ import division

import torch 
import random
import math

import numpy as np
import cv2

def adjust_box(poly):
    key_points = list()
    rotated = collections.deque(poly)
    rotated.rotate(1)
    for (x0, y0), (x1, y1) in zip(poly, rotated):
        for ratio in (1/3, 2/3):
            key_points.append((x0 * ratio + x1 * (1 - ratio), y0 * ratio + y1 * (1 - ratio)))
    x, y = zip(*key_points)
    adjusted_bbox = (min(x), min(y), max(x) - min(x), max(y) - min(y))
    return key_points, adjusted_bbox

def rbbox_transform(poly, angle):
    pi = math.pi()
    rad = angle / 360 * 2 * pi
    rot_mat = np.array([[np.cos(rad), -np.sin(rad)], [ np.sin(rad), np.cos(rad)]])
    
    ctr = np.mean(poly,axis=0)
    poly_ctr = poly - ctr
    poly_rot = np.dot(rot_mat, poly_ctr) + ctr
    
    return poly_rot


# Multi-scale usage
def get_crop_bboxes(imshape, cropshape, cropoverlap):

    """
    generate multi-scale training image bbox
    """
    crop_num_y = int(math.ceil((imshape[0] - cropshape[0]) / (cropshape[0] - cropoverlap[0]) + 1))
    crop_num_x = int(math.ceil((imshape[1] - cropshape[1]) / (cropshape[1] - cropoverlap[1]) + 1))
    for i in range(crop_num_y):
        for j in range(crop_num_x):
            ylo = int(round(i * (imshape[0] - cropshape[0]) / (crop_num_y - 1)))
            xlo = int(round(j * (imshape[1] - cropshape[1]) / (crop_num_x - 1)))
            yield {'name': '{}_{}'.format(i, j), 'xlo': xlo, 'ylo': ylo}