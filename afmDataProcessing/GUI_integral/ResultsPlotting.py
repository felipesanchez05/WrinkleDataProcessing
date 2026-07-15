import json
import scipy.stats
import matplotlib.pyplot as plt
from pathlib import Path
#selects input file
input_file = input("Input file name(.json): ") 

#a bunch of definitions for relative file paths to organize outputs in folders based on data file name
input_file_path = Path(input_file)
input_file_stem = input_file_path.stem
input_dir = Path(f'Outputs/{input_file_stem}')
out_dir_outliers = Path(f'Outputs/{input_file_stem}/WithOutliers')
out_dir_outliers.mkdir(parents=True, exist_ok=True)
out_dir_no_outliers = Path(f'Outputs/{input_file_stem}/NoOutliers')
out_dir_no_outliers.mkdir(parents=True, exist_ok=True)
#reads data
with open(input_dir/f'{input_file_stem}_fit_pruned.json','r') as f:
   clean_data = json.load(f)
with open(input_dir/f'{input_file_stem}_fit_results.json','r') as f:
   data = json.load(f)


amplitudes = [r['A'] for r in data]
wavelengths = [r['wavelength'] for r in data]
AdhesionEnergies = [r['Adhesion energy'] for r in data]


#repeats plotting code for a dimensions 
plt.hist(amplitudes) #plot histogram
plt.savefig(out_dir_outliers/ 'AmplitudesHistogram.png') #saves figure
plt.close() #"closes" figure to prevent messing up following figures
plt.hist(wavelengths)
plt.savefig(out_dir_outliers/ 'WavelenghtsHistogram.png')
plt.close()
plt.hist(AdhesionEnergies)
plt.savefig(out_dir_outliers/ 'AdhesionEnergiesHistogram.png')
plt.close
plt.plot()
plt.close()

#same thing but regular plots instead of histograms
plt.plot(amplitudes,'ro')
plt.savefig(out_dir_outliers/ "AmplitudesPlot.png")
plt.close()
plt.plot(wavelengths,'ro')
plt.savefig(out_dir_outliers/ 'WavelengthsPlot.png')
plt.close()
plt.plot(AdhesionEnergies,'ro')
plt.savefig(out_dir_outliers/ 'AdhesionEnergyPlot.png')

#repeat for data with removed outliers
amplitudes = [r['A'] for r in clean_data]
wavelengths = [r['wavelength'] for r in clean_data]
AdhesionEnergies = [r['Adhesion energy'] for r in clean_data]

plt.hist(amplitudes)
plt.savefig(out_dir_no_outliers/ 'AmplitudesHistogram.png')
plt.close()
plt.hist(wavelengths)
plt.savefig(out_dir_no_outliers/ 'WavelenghtsHistogram.png')
plt.close()
plt.hist(AdhesionEnergies)
plt.savefig(out_dir_no_outliers/ 'AdhesionEnergiesHistogram.png')
plt.close
plt.plot()
plt.close()

plt.plot(amplitudes,'ro')
plt.savefig(out_dir_no_outliers/ "AmplitudesPlot.png")
plt.close()
plt.plot(wavelengths,'ro')
plt.savefig(out_dir_no_outliers/ 'WavelengthsPlot.png')
plt.close()
plt.plot(AdhesionEnergies,'ro')
plt.savefig(out_dir_no_outliers/ 'AdhesionEnergyPlot.png')
