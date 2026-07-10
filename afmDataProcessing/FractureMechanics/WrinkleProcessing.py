# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""
import numpy as np
import ruptures as rpt
import matplotlib.pyplot as plt
import scipy.optimize as sp
import json
from pathlib import Path
#import Gwyddion data
from math import pi
from tqdm import tqdm
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
E = 5.7*10**9
strain = 0.03


def adhesion(thickness, wvlength, amplitude):
    aEnergy_1stTerm = (pi**4)/6
    aEnergy_2ndTerm = ((thickness**3)*(amplitude**2))/(wvlength**4)
    aEnergy_3rdTerm = E

    adhesion_energy = aEnergy_1stTerm * aEnergy_2ndTerm * aEnergy_3rdTerm
    return adhesion_energy,aEnergy_1stTerm, aEnergy_2ndTerm,aEnergy_3rdTerm



input_file = input("Data file name? : ")
input_dir = Path('DataMatrices/')
input_file_Path = Path(input_dir/ input_file)
input_file_stem = input_file_Path.stem
output_dir = Path(f'Outputs/{input_file_stem}')
output_dir.mkdir(parents=True, exist_ok=True)

thickness =int(input("Thickness of the flake (in nm)?: "))
thickness *= 10**(-9)
length = 10*10**(-6) #standard length
pixel_width = float(input("Width of pixel(in microns)?:"))
pixel_width *= 10**(-6)

#get x coordinate data
data = np.loadtxt(input_file_Path)

nx = data.shape[1]
x_values = np.arange(nx) * pixel_width

results = []
for row in tqdm(data):
    try:    
        dydx = np.gradient(row)
        algo = rpt.Dynp(model='rbf').fit(dydx)
        breakpoints = algo.predict(n_bkps=2)
        #fit data
        bp1_id = breakpoints[0]
        bp2_id = breakpoints[1] - 1
        bp1 = x_values[bp1_id]
        bp2 = x_values[bp2_id]

        A_guess = np.max(row) - np.median(row)
        baseline = np.median(row)
        guess = [bp1, bp2, A_guess, 0, baseline, 0, baseline]
        lower = [x_values[0], bp1,  -20,      -np.inf, -20,       -np.inf, -20     ]
        upper = [bp2,x_values[-1],  np.inf,  np.inf, np.inf,   np.inf, np.inf ]

        popt, pcov = sp.curve_fit(piecewise_wrinkle, x_values , row, p0=guess, bounds=(lower,upper))
        
        #extract measurements
        lam = popt[1] - popt[0]
        amp = popt[2]

        #calculate energy
        adhesionE = adhesion( thickness, lam, amp) #returns [adhesion energy, first term, second term, third term]

        #append results
        results.append({'A':amp, "wavelength":lam, "Adhesion energy":adhesionE[0] ,"length terms":adhesionE[1]})
    except RuntimeError:
        print("Failure to converge")
        


#stats
amplitudes = [r['A'] for r in results]
wavelengths = [r['wavelength'] for r in results]
AdhesionEnergies = [r['Adhesion energy'] for r in results]
length_terms = [r['length terms'] for r in results]

mean_amplitude = np.mean(amplitudes)
mean_wavelength = np.mean(wavelengths)
mean_adhesion_energy = np.mean(AdhesionEnergies)
adhesion_energy_from_mean =  adhesion(thickness, mean_wavelength,mean_amplitude)
greatest_first_term = np.max(length_terms)
with open(output_dir/ f'{input_file_stem}_fit_results.json','w') as f:
    json.dump(results,f,indent=2)
with open(output_dir/ f'{input_file_stem}_results.txt', 'w') as f:
    f.write(f"For {input_file}:\n")
    f.write(f"Mean amplitude: {mean_amplitude:.2e} +/- {np.std(amplitudes):.2e} \n")
    f.write(f"Mean wavelength: {mean_wavelength:.2e} +/- {np.std(wavelengths):.2e}\n")
    f.write(f"Mean adhesion energy: {mean_adhesion_energy:.2e} +/- {np.std(AdhesionEnergies):.2e}\n")
    f.write(f"Adhesion energy from means: {adhesion_energy_from_mean[0]:.2e}\n")
    f.write(f"Greatest length term: {greatest_first_term:.2e}\n")

