# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""
import numpy as np
import json
from pathlib import Path
from math import pi

from ProfileFitting import fit_profiles

def adhesion(thickness, wvlength, amplitude):
    aEnergy_1stTerm = (pi**4)/6
    aEnergy_2ndTerm = ((thickness**3)*(amplitude**2))/(wvlength**4)
    aEnergy_3rdTerm = E

    adhesion_energy = aEnergy_1stTerm * aEnergy_2ndTerm * aEnergy_3rdTerm
    return adhesion_energy,aEnergy_1stTerm, aEnergy_2ndTerm,aEnergy_3rdTerm


def compute_energies(profiles, thickness):
    results = []
    for profile in profiles:
        amp = profile['A']
        lam = profile['wavelength']
        adhesionE = adhesion(thickness, lam, amp) #returns [adhesion energy, first term, second term, third term]
        results.append({'A':amp, "wavelength":lam, "Adhesion energy":adhesionE[0] ,"length terms":adhesionE[1], "R2":profile['R2']})
    return results

def fit_data_energy(data_matrix, pixel_width, thickness, progress_callback=None, log_callback=print):
    profiles = fit_profiles(data_matrix, pixel_width, progress_callback=progress_callback, log_callback=log_callback)
    return compute_energies(profiles, thickness)

def write_results(results, output_dir, input_file_stem, thickness):
    if not results:
        raise ValueError("No rows converged; nothing to write.")

    amplitudes = [r['A'] for r in results]
    wavelengths = [r['wavelength'] for r in results]
    AdhesionEnergies = [r['Adhesion energy'] for r in results]
    length_terms = [r['length terms'] for r in results]
    r2 = [r['R2'] for r in results]

    mean_amplitude = np.mean(amplitudes)
    mean_wavelength = np.mean(wavelengths)
    mean_adhesion_energy = np.mean(AdhesionEnergies)
    adhesion_energy_from_mean =  adhesion(thickness, mean_wavelength,mean_amplitude)
    greatest_first_term = np.max(length_terms)
    mean_rsquared = np.mean(r2)
    largest_rsquared = np.max(r2)
    with open(output_dir/ f'{input_file_stem}_fit_results.json','w') as f:
        json.dump(results,f,indent=2)
    with open(output_dir/ f'{input_file_stem}_results.txt', 'w') as f:
        f.write(f"For {input_file_stem}:\n")
        f.write(f"Mean amplitude: {mean_amplitude:.2e} +/- {np.std(amplitudes):.2e} \n")
        f.write(f"Mean wavelength: {mean_wavelength:.2e} +/- {np.std(wavelengths):.2e}\n")
        f.write(f"Mean adhesion energy: {mean_adhesion_energy:.2e} +/- {np.std(AdhesionEnergies):.2e}\n")
        f.write(f"Adhesion energy from means: {adhesion_energy_from_mean[0]:.2e}\n")
        f.write(f"Greatest length term: {greatest_first_term:.2e}\n")
        f.write(f"Mean R squared: {mean_rsquared:.3f} +/- {np.std(r2):.3f} ; The largest R squared: {largest_rsquared:.3f}\n")
E = 5.7*10**9

if __name__ == '__main__':
    input_file = input("Data file name? : ")
    input_dir = Path('DataMatrices/')
    input_file_Path = Path(input_dir/ input_file)
    input_file_stem = input_file_Path.stem
    output_dir = Path(f'Outputs/{input_file_stem}')
    output_dir.mkdir(parents=True, exist_ok=True)

    thickness =int(input("Thickness of the flake (in nm)?: "))
    thickness *= 10**(-9)
    pixel_width = float(input("Width of pixel(in microns)?:"))
    pixel_width *= 10**(-6)

    data = np.loadtxt(input_file_Path)
    result = fit_data_energy(data, pixel_width, thickness)
    write_results(result, output_dir, input_file_stem, thickness)
