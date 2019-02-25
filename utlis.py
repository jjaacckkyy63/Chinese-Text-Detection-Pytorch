from __future__ import division

import collections
import matplotlib.patches as patches
import matplotlib.pyplot as plt

%matplotlib inline

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

def 