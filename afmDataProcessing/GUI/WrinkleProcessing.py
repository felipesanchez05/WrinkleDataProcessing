# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""

#import libraries
import numpy as np
import json
from pathlib import Path
from math import pi

from ProfileFitting import fit_profiles

def adhesion(length, thickness, wvlength, amplitude, strain):
    """
    Function which takes flake dimensions as inputs to calculate adhesion energy
    Saves each term separately in addition to adhesion energy to compare magnitude of length term later
    """
    aEnergy_1stTerm = ( (pi**4) * (amplitude**4) * (E)* thickness) / (16 * (wvlength) * length)
    aEnergy_2ndTerm = ( (strain) * (pi**2) * (amplitude**2) * E * thickness ) / (4 * (wvlength**2))
    aEnergy_3rdTerm = ( (pi**4) * (amplitude**2) * E * (thickness**3)) / (4 * wvlength**4)*(1-0.3**2) 

    adhesion_energy = aEnergy_1stTerm - aEnergy_2ndTerm + aEnergy_3rdTerm
    return adhesion_energy,aEnergy_1stTerm, aEnergy_2ndTerm,aEnergy_3rdTerm


def compute_energies(profiles, length, thickness, strain, r2_threshold=0.88):
    """
    Function takes as input the fitted profile paramters from curve fitting to compute adhesion energy
    Profiles input is a list of dictionaries
    """
    results = [] #creates empy list to store result values
    for profile in profiles: #loops through each profile
        amp = profile['A'] #set variable to amplitude value
        lam = profile['wavelength'] #set variable to wavelength value
        adhesionE = adhesion(length, thickness, lam, amp, strain) #returns [adhesion energy, first term, second term, third term]
        if profile['R2'] > r2_threshold:
            results.append({'A':amp, "wavelength":lam, "Adhesion energy":adhesionE[0] ,"length terms":adhesionE[1], "R2":profile['R2']}) #add calculated value to results list
    return results

def fit_data_energy(data_matrix, pixel_width, length, thickness, strain, r2_threshold=0.88, progress_callback=None, log_callback=print):
    """
    Defines a function that calls the fit_profiles function from ProfileFititng file to fit profiles in data matrix to peacewise function
    """
    profiles = fit_profiles(data_matrix, pixel_width, progress_callback=progress_callback, log_callback=log_callback)
    return compute_energies(profiles, length, thickness, strain, r2_threshold)

def write_results(results, output_dir, input_file_stem, length, thickness, strain):
    """
    Saves inputted results to a file for storage
    """

    if not results: #failsafe for empty results list
        raise ValueError("No rows converged; nothing to write.")
    #The block creates float vectors from list of dictionaries by extracting the specific value from results list
    # [] creates the list, the for loop goes through each item in results list, labeled as r, and saves the value corresponding to ['']
    amplitudes = [r['A'] for r in results]
    wavelengths = [r['wavelength'] for r in results]
    AdhesionEnergies = [r['Adhesion energy'] for r in results]
    length_terms = [r['length terms'] for r in results]
    r2 = [r['R2'] for r in results]

    #Uses numpy to find means
    mean_amplitude = np.mean(amplitudes)
    mean_wavelength = np.mean(wavelengths)
    mean_adhesion_energy = np.mean(AdhesionEnergies)
    
    #calls adhesion function using mean values
    adhesion_energy_from_mean =  adhesion(length, thickness, mean_wavelength,mean_amplitude, strain)
    greatest_first_term = np.max(length_terms) #finds the largest length term
    mean_rsquared = np.mean(r2)
    smallest_rsquared = np.min(r2)
    
    #The block creates andwrites results 
    with open(output_dir/ f'{input_file_stem}_fit_results.json','w') as f:
        json.dump(results,f,indent=2) #uses dump from json library to write out results library unto a json file
    with open(output_dir/ f'{input_file_stem}_results.txt', 'w') as f:
        """
        F strings are used to write out mean values
        """
        f.write(f"For {input_file_stem}:\n")
        f.write(f"Mean amplitude: {mean_amplitude:.2e} +/- {np.std(amplitudes):.2e} \n")
        f.write(f"Mean wavelength: {mean_wavelength:.2e} +/- {np.std(wavelengths):.2e}\n")
        f.write(f"Mean adhesion energy: {mean_adhesion_energy:.2e} +/- {np.std(AdhesionEnergies):.2e}\n")
        f.write(f"Adhesion energy from means: {adhesion_energy_from_mean[0]:.2e}\n")
        f.write(f"Greatest length term: {greatest_first_term:.2e}\n")
        f.write(f"Mean R squared: {mean_rsquared:.3f} +/- {np.std(r2):.3f} ; The smallest R squared: {smallest_rsquared:.3f}\n")

#hard coded values
E = 5.7*10**9

if __name__ == '__main__':
    """
    If main block to fit data file. This file is mainly made to be called by GUI so this isn't typically run
    """
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
    strain = float(input("Strain?: "))

    data = np.loadtxt(input_file_Path)
    result = fit_data_energy(data, pixel_width, length, thickness, strain)
    write_results(result, output_dir, input_file_stem, length, thickness, strain)

