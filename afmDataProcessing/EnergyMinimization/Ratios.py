import json
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
input_file = input("Data file name: ")
input_file_path = Path(input_file)
input_file_stem = input_file_path.stem
in_out_dir = Path(f'Outputs/{input_file_stem}')
with open(in_out_dir/f'{input_file_stem}_fit_results.json','r') as f:
    data = json.load(f)


amplitudes = [r['A'] for r in data]
wavelengths = [r['wavelength'] for r in data]
ratios = []
for count in range(len(amplitudes)):
    ratios.append(amplitudes[count]/wavelengths[count])

plt.plot(ratios)
plt.savefig(in_out_dir/f'{input_file_stem}ratios_plot.png')
avg_ratio = np.mean(ratios)

with open(in_out_dir/f'{input_file_stem}_ratios_average.txt','w') as f:
    f.write(f'{avg_ratio:.2f}')

