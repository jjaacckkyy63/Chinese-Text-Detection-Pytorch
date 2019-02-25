from __future__ import division

import collections
import matplotlib.patches as patches
import matplotlib.pyplot as plt

%matplotlib inline

from __future__ import division

import torch 
import random

import numpy as np
import cv2

def confidence_filter(result, confidence):
    conf_mask = (result[:,:,4] > confidence).float().unsqueeze(2)
    result = result*conf_mask    
    
    return result

def confidence_filter_cls(result, confidence):
    max_scores = torch.max(result[:,:,5:25], 2)[0]
    res = torch.cat((result, max_scores),2)
    print(res.shape)
    
    
    cond_1 = (res[:,:,4] > confidence).float()
    cond_2 = (res[:,:,25] > 0.995).float()
    
    conf = cond_1 + cond_2
    conf = torch.clamp(conf, 0.0, 1.0)
    conf = conf.unsqueeze(2)
    result = result*conf   
    return result
    

def bbox_iou(box1, box2):
    """
    computing IOU of bboxes
    """

    #Get the coordinates of bounding boxes
    b1_x1, b1_y1, b1_x2, b1_y2 = box1[:,0], box1[:,1], box1[:,2], box1[:,3]
    b2_x1, b2_y1, b2_x2, b2_y2 = box2[:,0], box2[:,1], box2[:,2], box2[:,3]
    
    #get the corrdinates of the intersection rectangle
    inter_rect_x1 =  torch.max(b1_x1, b2_x1)
    inter_rect_y1 =  torch.max(b1_y1, b2_y1)
    inter_rect_x2 =  torch.min(b1_x2, b2_x2)
    inter_rect_y2 =  torch.min(b1_y2, b2_y2)
    
    #Intersection area
    if torch.cuda.is_available():
            inter_area = torch.max(inter_rect_x2 - inter_rect_x1 + 1,torch.zeros(inter_rect_x2.shape).cuda())*torch.max(inter_rect_y2 - inter_rect_y1 + 1, torch.zeros(inter_rect_x2.shape).cuda())
    else:
            inter_area = torch.max(inter_rect_x2 - inter_rect_x1 + 1,torch.zeros(inter_rect_x2.shape))*torch.max(inter_rect_y2 - inter_rect_y1 + 1, torch.zeros(inter_rect_x2.shape))
    
    #Union Area
    b1_area = (b1_x2 - b1_x1 + 1)*(b1_y2 - b1_y1 + 1)
    b2_area = (b2_x2 - b2_x1 + 1)*(b2_y2 - b2_y1 + 1)
    
    iou = inter_area / (b1_area + b2_area - inter_area)
    
    return iou


def write(x, batches, results, colors, classes):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    img = results[int(x[0])]
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    color = random.choice(colors)
    cv2.rectangle(img, c1, c2,color, 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(img, c1, c2,color, -1)
    cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225,255,255], 1);
    return img

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

def rbbox_transform(ex_rois, gt_rois):

    """
    implement rotating bounding box
    """
	ex_widths = ex_rois[:, 3] 
	ex_heights = ex_rois[:, 2] 
	ex_ctr_x = ex_rois[:, 0]
	ex_ctr_y = ex_rois[:, 1]
	ex_angle = ex_rois[:, 4] 	

	gt_widths = gt_rois[:, 3]
	gt_heights = gt_rois[:, 2]
	gt_ctr_x = gt_rois[:, 0]
	gt_ctr_y = gt_rois[:, 1]
	gt_angle = gt_rois[:, 4]

	targets_dx = (gt_ctr_x - ex_ctr_x)*1.0 / ex_widths
    	targets_dy = (gt_ctr_y - ex_ctr_y)*1.0 / ex_heights
    	targets_dw = np.log(gt_widths*1.0 / ex_widths)
    	targets_dh = np.log(gt_heights*1.0 / ex_heights)

	#ex_angle = np.pi / 180 * ex_angle
	#gt_angle = np.pi / 180 * gt_angle
	
	targets_da = gt_angle - ex_angle

	targets_da[np.where((gt_angle<=-30) & (ex_angle>=120))]+=180
	targets_da[np.where((gt_angle>=120) & (ex_angle<=-30))]-=180

	targets_da = 3.14159265358979323846264338327950288/180*targets_da
	

	targets = np.vstack(
		 (targets_dx, targets_dy, targets_dw, targets_dh, targets_da)
	).transpose()

	return targets



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