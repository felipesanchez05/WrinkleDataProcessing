Scripts for analyzing wrinkles for Dr. Tu's lab \
\
General process: \
1.Place AFM data into DataMatrices folder \
2.Run WrinkleProcessing.py to create [filename]_results.txt and [filename]_fit_results.json \
3.Run StatsPrune.py to run data through isolation forest outlier detecterion (and remove negative adhesion energies). Creates [filename]_fit_pruned.json \
4.Run ResulstsPlotting.py to plot filtered data *currently only works after running StatsPruned.py; pulls [filename]_fit_pruned.json \
