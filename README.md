
# Recognize-Chinese-Characters-on-Traffic-Signs

## YOLOv3


# Requirements

Python 3.7 or later with the following `pip3 install -U -r requirements.txt` packages:

- `numpy`
- `torch >= 1.0.0`
- `opencv-python`


# Training

**Start Training:** Run `train.py` to begin training 

## Image Augmentation

Augmentation | Description
--- | ---
Translation | +/- 10% (vertical and horizontal)
Rotation | +/- 5 degrees
Shear | +/- 2 degrees (vertical and horizontal)
Scale | +/- 10%
Reflection | 50% probability (horizontal-only)
H**S**V Saturation | +/- 50%
HS**V** Intensity | +/- 50%
Distortation +/- 30%

# Inference

Run `detect.py` to apply trained weights to an image

**YOLOv3:** `detect.py --cfg cfg/yolov3.cfg --weights weights/yolov3.pt`

# Validation mAP

Run `test.py` to validate 

# Results for Red-Round Traffic Sign Detection
