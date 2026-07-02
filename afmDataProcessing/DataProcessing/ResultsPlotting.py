import json
import scipy.stats
import matplotlib.pyplot as plt
from pathlib import Path

input_file = input("Input file name(.json): ") 
input_file_path = Path(input_file)
input_file_stem = input_file_path.stem
in_out_dir = Path(f'Outputs/{input_file_stem}')


with open(in_out_dir/f'{input_file_stem}_fit_pruned.json','r') as f:
    data = json.load(f)

amplitudes = [r['A'] for r in data]
wavelengths = [r['wavelength'] for r in data]
AdhesionEnergies = [r['Adhesion energy'] for r in data]

plt.hist(amplitudes)
plt.savefig(in_out_dir/ 'AmplitudesHistogram.png')
plt.close()
plt.hist(wavelengths)
plt.savefig(in_out_dir/ 'WavelenghtsHistogram.png')
plt.close()
plt.hist(AdhesionEnergies)
plt.savefig(in_out_dir/ 'AdhesionEnergiesHistogram.png')
plt.close
plt.plot()
plt.close()

plt.plot(amplitudes,'ro')
plt.savefig(in_out_dir/ "AmplitudesPlot.png")
plt.close()
plt.plot(wavelengths,'ro')
plt.savefig(in_out_dir/ 'WavelengthsPlot.png')
plt.close()
plt.plot(AdhesionEnergies,'ro')
plt.savefig(in_out_dir/ 'AdhesionEnergyPlot.png')
