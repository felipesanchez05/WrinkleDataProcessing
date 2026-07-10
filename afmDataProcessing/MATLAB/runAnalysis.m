%RUNANALYSIS Interactive driver that fits wrinkle profiles once and
%computes wrinkle-buckling and/or fracture-mechanics adhesion energies
%for them. This is the orchestration logic from GUI.py's
%process_in_background, without the GUI: it fits each row's profile a
%single time (fitProfiles.m) and applies whichever energy model(s) are
%selected to that same fit, so nothing gets fit twice.
%
%   Expects the data file to be readable by readmatrix (whitespace- or
%   comma-delimited numeric text, matching np.loadtxt in the Python
%   version) inside a 'DataMatrices' folder relative to the current
%   folder. Writes outputs under 'Outputs/<stem>/'.

inputFile = input('Data file name? : ', 's');
inputFilePath = fullfile('DataMatrices', inputFile);
[~, inputFileStem] = fileparts(inputFilePath);
outputDir = fullfile('Outputs', inputFileStem);
if ~exist(outputDir, 'dir')
    mkdir(outputDir);
end

thicknessNm = input('Thickness of the flake (in nm)? : ');
thickness = thicknessNm * 1e-9;
flakeLength = 10e-6; % standard flake length in meters, matches WrinkleProcessing.py

pixelWidthUm = input('Width of pixel (in microns)? : ');
pixelWidth = pixelWidthUm * 1e-6;

runWrinkle = promptYesNo('Run wrinkle-buckling analysis? [Y/n]: ', true);
runFracture = promptYesNo('Run fracture-mechanics analysis? [y/N]: ', false);
if ~runWrinkle && ~runFracture
    error('runAnalysis:NoMethodSelected', 'Select at least one analysis method.');
end

data = readmatrix(inputFilePath);

fprintf('Fitting wrinkle profiles...\n');
profiles = fitProfiles(data, pixelWidth);

if runWrinkle
    fprintf('Computing wrinkle adhesion energy...\n');
    results = wrinkleComputeEnergies(profiles, flakeLength, thickness);
    wrinkleWriteResults(results, outputDir, [inputFileStem '_wrinkle'], flakeLength, thickness);
    fprintf('Wrinkle analysis complete.\n');
end

if runFracture
    fprintf('Computing fracture mechanics adhesion energy...\n');
    results = fractureComputeEnergies(profiles, thickness);
    fractureWriteResults(results, outputDir, [inputFileStem '_fracture'], thickness);
    fprintf('Fracture mechanics analysis complete.\n');
end

fprintf('Done. Results written to %s\n', outputDir);

function tf = promptYesNo(promptText, defaultValue)
answer = strtrim(input(promptText, 's'));
if isempty(answer)
    tf = defaultValue;
else
    tf = strcmpi(answer, 'y') || strcmpi(answer, 'yes');
end
end
