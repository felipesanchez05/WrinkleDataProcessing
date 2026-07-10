function plotResults(inputFileStem, outputsRoot)
%PLOTRESULTS Save histograms and per-row plots of amplitude, wavelength
%and adhesion energy, before and after outlier pruning. Mirrors
%ResultsPlotting.py.
%   PLOTRESULTS(inputFileStem) reads
%   '<outputsRoot>/<inputFileStem>/<inputFileStem>_fit_results.json' and
%   '..._fit_pruned.json' (see pruneStats.m) and saves PNG plots into
%   'WithOutliers/' and 'NoOutliers/' subfolders.
%
%   PLOTRESULTS(inputFileStem, outputsRoot) uses outputsRoot instead of
%   the default 'Outputs'.

if nargin < 2 || isempty(outputsRoot)
    outputsRoot = 'Outputs';
end

inputDir = fullfile(outputsRoot, inputFileStem);
outDirOutliers = fullfile(inputDir, 'WithOutliers');
outDirNoOutliers = fullfile(inputDir, 'NoOutliers');
if ~exist(outDirOutliers, 'dir'); mkdir(outDirOutliers); end
if ~exist(outDirNoOutliers, 'dir'); mkdir(outDirNoOutliers); end

data = jsondecode(fileread(fullfile(inputDir, sprintf('%s_fit_results.json', inputFileStem))));
cleanData = jsondecode(fileread(fullfile(inputDir, sprintf('%s_fit_pruned.json', inputFileStem))));

savePlots(data, outDirOutliers);
savePlots(cleanData, outDirNoOutliers);

end

function savePlots(data, outDir)
amplitudes = [data.A]';
wavelengths = [data.wavelength]';
adhesionEnergies = [data.AdhesionEnergy]';

saveHistogram(amplitudes, fullfile(outDir, 'AmplitudesHistogram.png'));
saveHistogram(wavelengths, fullfile(outDir, 'WavelengthsHistogram.png'));
saveHistogram(adhesionEnergies, fullfile(outDir, 'AdhesionEnergiesHistogram.png'));

saveLinePlot(amplitudes, fullfile(outDir, 'AmplitudesPlot.png'));
saveLinePlot(wavelengths, fullfile(outDir, 'WavelengthsPlot.png'));
saveLinePlot(adhesionEnergies, fullfile(outDir, 'AdhesionEnergyPlot.png'));
end

function saveHistogram(values, outFile)
fig = figure('Visible', 'off');
histogram(values);
saveas(fig, outFile);
close(fig);
end

function saveLinePlot(values, outFile)
fig = figure('Visible', 'off');
plot(values, 'ro');
saveas(fig, outFile);
close(fig);
end
