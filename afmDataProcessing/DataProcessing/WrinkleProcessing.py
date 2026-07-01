# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""
import numpy as np
import ruptures as rpt
import matplotlib.pyplot as plt
import scipy.optimize as sp
#import Gwyddion data
import pandas as pd
from math import pi
def piecewise_wrinkle(x,first_breakpoint,second_breakpoint, A, m_left, b_left, m_right, b_right):
    y = np.zeros_like(x)
    left_mask = x < first_breakpoint
    right_mask = x > second_breakpoint
    wrinkle_mask = (x >= first_breakpoint) & (x <= second_breakpoint)
    y[left_mask] = m_left * x[left_mask] + b_left
    y[right_mask] = m_right * x[right_mask] + b_right
    lam = second_breakpoint - first_breakpoint
    base = m_left * first_breakpoint + b_left
    midpoint = (first_breakpoint + second_breakpoint) / 2
    y[wrinkle_mask] = base + (A/2) * (1 + np.cos(2 * pi * (x[wrinkle_mask] - midpoint) / lam))

    return y

input_file = input("Data file name? : ")
pixel_horizontal_dimension = input("Size of pixel?: ")

df = pd.read_csv(input_file, 
                 delimiter=";", 
                 skiprows=3,
                 header=None,
                 names=["x1","y1","x2","y2","drop"],
                 usecols=[0,1,2,3])  # ignore the trailing empty column

x1 = df["x1"].values
y1 = df["y1"].values 
mask2 = df["x2"].notna()
x2 = df["x2"][mask2].values
y2 = df["y2"][mask2].values


plt.plot(x1,y1)
plt.plot(x2,y2)
plt.savefig('output.png')
plt.close()
#find breakpoints
dydx1 = np.gradient(y1,x1)
dydx2 = np.gradient(y2,x2)

algo = rpt.Dynp(model='rbf').fit(dydx1.reshape(-1,1))
algo2 = rpt.Dynp(model='rbf').fit(dydx2.reshape(-1,1))
breakpoints1 = algo.predict(n_bkps=2)
breakpoints2 = algo2.predict(n_bkps=2)
rpt.display(y1,breakpoints1)
plt.savefig('output2.png')
rpt.display(y2,breakpoints2)
plt.savefig("output3.png")
plt.close()   


#fit data
bp1_id = breakpoints1[0]
bp2_id = breakpoints1[1]
bp1 = x1[bp1_id]
bp2 = x1[bp2_id-1]
print(f"Wrinkle from {bp1*1e6:.2f} to {bp2*1e6:.2f} μm")
A_guess = y1.max() - np.median(y1)
baseline = np.median(y1)
guess = [bp1, bp2, A_guess, 0, baseline, 0, baseline]
lower = [bp1 * 0.8, bp2 * 0.8,  0,      -np.inf, 0,       -np.inf, 0      ]
upper = [bp1 * 1.2, bp2 * 1.2,  np.inf,  np.inf, np.inf,   np.inf, np.inf ]
popt, pcov = sp.curve_fit(piecewise_wrinkle, x1, y1, p0=guess, bounds=(lower,upper))
yfit=piecewise_wrinkle(x1,*popt)
plt.figure()
plt.plot(x1,y1, 'bo', label ='data')
plt.plot(x1,yfit, 'r-',label='fit')
plt.savefig('output4.png')
print(popt)

bp1_id_2 = breakpoints2[0]
bp2_id_2 = breakpoints2[1]
bp1_2 = x2[bp1_id_2]
bp2_2 = x2[bp2_id_2-1]
A_guess_2 = y2.max() - np.median(y2)
baseline_2 = np.median(y2)
guess_2 = [bp1_2, bp2_2, A_guess_2, 0, baseline_2, 0, baseline_2]
lower_2 = [bp1_2 * 0.8, bp2_2 * 0.8,  0,      -np.inf, 0,       -np.inf, 0      ]
upper_2 = [bp1_2 * 1.2, bp2_2 * 1.2,  np.inf,  np.inf, np.inf,   np.inf, np.inf ]
popt2, pcov2 = sp.curve_fit(piecewise_wrinkle, x2, y2, p0=guess_2, bounds=(lower_2,upper_2))
yfit2=piecewise_wrinkle(x2,*popt2)
plt.figure()
plt.plot(x2,y2, 'bo', label ='data')
plt.plot(x2,yfit2, 'r-',label='fit')
plt.savefig('output5.png')
#extract measurements

#calculate data

#stats
