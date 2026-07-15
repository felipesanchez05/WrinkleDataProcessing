import json
import scipy.stats
import matplotlib.pyplot as plt
from pathlib import Path

input_file = input("Data file name: ")
input_file_path = Path(input_file)
input_file_stem = input_file_path.stem
in_out_dir = Path(f'Outputs/{input_file_stem}')

with open(in_out_dir/f'{input_file_stem}_fit_results.json','r') as f:
    data = json.load(f) #Reads results from json file using json library

AE_threshold = 50 #hard cap for physically unreasonable data. 50 is a high bar, but if its too low, an irregular wrinkle will just return 0 values
clean = [r for r in data if r['Adhesion energy'] < AE_threshold] #creates a new list excluding all values above the threshold
print(f"Removed {len(data) - len(clean)} extreme outliers")

clean = [r for r in clean if r['Adhesion energy'] > 0] #creates a new list excluding all negative values
print(f"Removed {len(data) - len(clean)} negative outliers")

#Creates float vectors from the list of dictionaries for each dimension
amplitudes = [r['A'] for r in clean]
wavelengths = [r['wavelength'] for r in clean]
AdhesionEnergies = [r['Adhesion energy'] for r in clean]

#import statememtns
from sklearn.ensemble import IsolationForest
import numpy as np

#stacks up the amplitudes, wavelenghts, and adhesion energies again but wihout the extra values such as R squared 
X = np.column_stack([
    amplitudes,
    wavelengths,
    AdhesionEnergies])

iso = IsolationForest(contamination=0.05, n_estimators=200, random_state=42) #sets up isolation forest algorithm
labels = iso.fit_predict(X)

final = [r for r, label in zip(clean, labels) if label == 1] #creates a list without outliers excluded by isoltion forest algorithm
print(f"After isolation forest: {len(final)} / {len(clean)}")

#Writes out new file with removed nonsense values and outliers
with open(in_out_dir/ f'{input_file_stem}_fit_pruned.json','w') as f:
    json.dump(final,f,indent=2)

