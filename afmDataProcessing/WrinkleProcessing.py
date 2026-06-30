# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""
import numpy as np
import ruptures as rpt
import matplotlib.pyplot as plt
#import Gwyddion data

data = np.loadtxt("testProcessing.txt",delimiter=";",skiprows=3)  # rows = parallel profiles
x1, y1 = data[:, 0], data[:, 1]
x2, y2 = data[:, 2], data[:, 3]
#x = np.arange(data.shape[1]) * pixel_size  # position along wrinkle direction
plt.plot(x1,y1)
plt.plotx2,y2)

#find breakpoints

#fit data

#extract measurements

#calculate data

#stats