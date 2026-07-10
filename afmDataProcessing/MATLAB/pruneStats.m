function pruneStats(inputFileStem, outputsRoot)
%PRUNESTATS Remove non-physical and statistical outliers from a fitted
%results JSON file. Mirrors StatsPrune.py.
%   PRUNESTATS(inputFileStem) reads
%   '<outputsRoot>/<inputFileStem>/<inputFileStem>_fit_results.json',
%   drops rows with a non-physical adhesion energy (>= 10 J/m^2, or <= 0),
%   then removes statistical outliers with an isolation forest over
%   [A, wavelength, AdhesionEnergy], and writes the survivors to
%   '<inputFileStem>_fit_pruned.json' in the same folder.
%
%   PRUNESTATS(inputFileStem, outputsRoot) uses outputsRoot instead of
%   the default 'Outputs'.
%
%   Requires the Statistics and Machine Learning Toolbox (iforest,
%   introduced in R2021a).

if nargin < 2 || isempty(outputsRoot)
    outputsRoot = 'Outputs';
end

inOutDir = fullfile(outputsRoot, inputFileStem);
data = jsondecode(fileread(fullfile(inOutDir, sprintf('%s_fit_results.json', inputFileStem))));

aeThreshold = 10; % J/m^2, adjust based on what's physically reasonable

adhesionEnergy = [data.AdhesionEnergy]';
keep = adhesionEnergy < aeThreshold;
fprintf('Removed %d extreme outliers\n', sum(~keep));
clean = data(keep);

adhesionEnergy = [clean.AdhesionEnergy]';
keep = adhesionEnergy > 0;
fprintf('Removed %d negative outliers\n', sum(~keep));
clean = clean(keep);

amplitudes = [clean.A]';
wavelengths = [clean.wavelength]';
adhesionEnergies = [clean.AdhesionEnergy]';
X = [amplitudes, wavelengths, adhesionEnergies];

rng(42); % matches the fixed random_state used on the Python side
[~, isOutlier] = iforest(X, 'ContaminationFraction', 0.05, 'NumLearners', 200);

final = clean(~isOutlier);
fprintf('After isolation forest: %d / %d\n', numel(final), numel(clean));

fid = fopen(fullfile(inOutDir, sprintf('%s_fit_pruned.json', inputFileStem)), 'w');
fwrite(fid, jsonencode(final, 'PrettyPrint', true));
fclose(fid);

end
