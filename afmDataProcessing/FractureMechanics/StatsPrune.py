import json
import scipy.stats
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
input_file = input("Data file name: ")
input_file_path = Path(input_file)
input_file_stem = input_file_path.stem
in_out_dir = Path(f'Outputs/{input_file_stem}')
with open(in_out_dir/f'{input_file_stem}_fit_results.json','r') as f:
    data = json.load(f)
outliers = [r['Adhesion energy'] for r in data]

AE_threshold = np.mean(outliers)*4  # J/m², adjust based on what's physically reasonable
clean = [r for r in data if r['Adhesion energy'] < AE_threshold]
print(f"Removed {len(data) - len(clean)} extreme outliers")

clean = [r for r in clean if r['Adhesion energy'] > 0]
print(f"Removed {len(data) - len(clean)} negative outliers")

amplitudes = [r['A'] for r in clean]
wavelengths = [r['wavelength'] for r in clean]
AdhesionEnergies = [r['Adhesion energy'] for r in clean]

from sklearn.ensemble import IsolationForest
import numpy as np

X = np.column_stack([
    amplitudes,
    wavelengths,
    AdhesionEnergies])

iso = IsolationForest(contamination=0.05, n_estimators=200, random_state=42)
labels = iso.fit_predict(X)

final = [r for r, label in zip(clean, labels) if label == 1]
print(f"After isolation forest: {len(final)} / {len(clean)}")

with open(in_out_dir/ f'{input_file_stem}_fit_pruned.json','w') as f:
    json.dump(final,f,indent=2)

