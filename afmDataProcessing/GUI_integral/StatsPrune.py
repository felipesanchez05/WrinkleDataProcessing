# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""
import json
import numpy as np
from pathlib import Path
from sklearn.ensemble import IsolationForest


def prune_outliers(results, ae_threshold, log_callback=print):
    """
    Removes physically unreasonable and statistically outlying rows from a list of fit results.
    ae_threshold caps 'Adhesion energy' from above; callers pick it per adhesion-energy model
    (wrinkle: fixed hard cap, fracture: relative to the mean).
    """
    clean = [r for r in results if r['Adhesion energy'] < ae_threshold] #creates a new list excluding all values above the threshold
    log_callback(f"Removed {len(results) - len(clean)} extreme outliers")

    clean = [r for r in clean if r['Adhesion energy'] > 0] #creates a new list excluding all negative values
    log_callback(f"Removed {len(results) - len(clean)} negative outliers")

    #Creates float vectors from the list of dictionaries for each dimension
    amplitudes = [r['A'] for r in clean]
    wavelengths = [r['wavelength'] for r in clean]
    AdhesionEnergies = [r['Adhesion energy'] for r in clean]

    #stacks up the amplitudes, wavelenghts, and adhesion energies again but wihout the extra values such as R squared
    X = np.column_stack([
        amplitudes,
        wavelengths,
        AdhesionEnergies])

    iso = IsolationForest(contamination=0.05, n_estimators=200, random_state=42) #sets up isolation forest algorithm
    labels = iso.fit_predict(X)

    final = [r for r, label in zip(clean, labels) if label == 1] #creates a list without outliers excluded by isoltion forest algorithm
    log_callback(f"After isolation forest: {len(final)} / {len(clean)}")
    return final


def write_pruned_results(pruned, output_dir, input_file_stem):
    """
    Saves inputted pruned results to a file for storage
    """
    with open(Path(output_dir) / f'{input_file_stem}_fit_pruned.json', 'w') as f:
        json.dump(pruned, f, indent=2)


if __name__ == '__main__':
    """
    If main block to prune a results file directly. This file is mainly made to be called by GUI so this isn't typically run
    """
    input_file = input("Data file name: ")
    input_file_path = Path(input_file)
    input_file_stem = input_file_path.stem
    in_out_dir = Path(f'Outputs/{input_file_stem}')

    with open(in_out_dir/f'{input_file_stem}_fit_results.json','r') as f:
        data = json.load(f) #Reads results from json file using json library

    AE_threshold = 50 #hard cap for physically unreasonable data. 50 is a high bar, but if its too low, an irregular wrinkle will just return 0 values
    pruned = prune_outliers(data, AE_threshold)
    write_pruned_results(pruned, in_out_dir, input_file_stem)
