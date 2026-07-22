# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""
import json
import matplotlib
matplotlib.use('Agg')  # non-interactive backend: plotting runs on the GUI's background thread, and Tk's default backend isn't thread-safe
import matplotlib.pyplot as plt
from pathlib import Path


def _plot_set(results, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)

    amplitudes = [r['A'] for r in results]
    wavelengths = [r['wavelength'] for r in results]
    AdhesionEnergies = [r['Adhesion energy'] for r in results]

    #repeats plotting code for a dimensions
    plt.hist(amplitudes) #plot histogram
    plt.xlabel('Amplitude (m)')
    plt.ylabel('Count')
    plt.savefig(out_dir/ 'AmplitudesHistogram.png') #saves figure
    plt.close() #"closes" figure to prevent messing up following figures
    plt.hist(wavelengths)
    plt.xlabel('Wavelength (m)')
    plt.ylabel('Count')
    plt.savefig(out_dir/ 'WavelenghtsHistogram.png')
    plt.close()
    plt.hist(AdhesionEnergies)
    plt.xlabel('Adhesion energy (J/m$^2$)')
    plt.ylabel('Count')
    plt.savefig(out_dir/ 'AdhesionEnergiesHistogram.png')
    plt.close()

    #same thing but regular plots instead of histograms
    plt.plot(amplitudes,'ro')
    plt.xlabel('Profile index')
    plt.ylabel('Amplitude (m)')
    plt.savefig(out_dir/ "AmplitudesPlot.png")
    plt.close()
    plt.plot(wavelengths,'ro')
    plt.xlabel('Profile index')
    plt.ylabel('Wavelength (m)')
    plt.savefig(out_dir/ 'WavelengthsPlot.png')
    plt.close()
    plt.plot(AdhesionEnergies,'ro')
    plt.xlabel('Profile index')
    plt.ylabel('Adhesion energy (J/m$^2$)')
    plt.savefig(out_dir/ 'AdhesionEnergyPlot.png')
    plt.close()


def plot_results(all_results, pruned_results, output_dir, input_file_stem):
    """
    Saves histograms and scatter plots for the raw fit results (WithOutliers) and again
    for the results left after prune_outliers has removed extreme/negative/isolation-forest outliers (NoOutliers)
    """
    stem_dir = Path(output_dir) / input_file_stem
    _plot_set(all_results, stem_dir / 'WithOutliers')
    _plot_set(pruned_results, stem_dir / 'NoOutliers')


if __name__ == '__main__':
    """
    If main block to plot a results file directly. This file is mainly made to be called by GUI so this isn't typically run
    """
    #selects input file
    input_file = input("Input file name(.json): ")

    #a bunch of definitions for relative file paths to organize outputs in folders based on data file name
    input_file_path = Path(input_file)
    input_file_stem = input_file_path.stem
    input_dir = Path(f'Outputs/{input_file_stem}')
    #reads data
    with open(input_dir/f'{input_file_stem}_fit_pruned.json','r') as f:
        clean_data = json.load(f)
    with open(input_dir/f'{input_file_stem}_fit_results.json','r') as f:
        data = json.load(f)

    plot_results(data, clean_data, 'Outputs', input_file_stem)
