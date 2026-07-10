function writeAdhesionResults(results, outputDir, inputFileStem, adhesionEnergyFromMean)
%WRITEADHESIONRESULTS Shared JSON/summary writer for adhesion energy
%results, used by both wrinkleWriteResults.m and fractureWriteResults.m.
%   Writes '<inputFileStem>_fit_results.json' (per-row results) and
%   '<inputFileStem>_results.txt' (summary statistics) into outputDir.
%
%   Requires MATLAB R2021a or later for jsonencode's 'PrettyPrint' option.

if isempty(results)
    error('writeAdhesionResults:NoResults', 'No rows converged; nothing to write.');
end

amplitudes = [results.A];
wavelengths = [results.wavelength];
adhesionEnergies = [results.AdhesionEnergy];
lengthTerms = [results.lengthTerm];

if ~exist(outputDir, 'dir')
    mkdir(outputDir);
end

fid = fopen(fullfile(outputDir, sprintf('%s_fit_results.json', inputFileStem)), 'w');
fwrite(fid, jsonencode(results, 'PrettyPrint', true));
fclose(fid);

fid = fopen(fullfile(outputDir, sprintf('%s_results.txt', inputFileStem)), 'w');
fprintf(fid, 'For %s:\n', inputFileStem);
fprintf(fid, 'Mean amplitude: %.2e +/- %.2e \n', mean(amplitudes), std(amplitudes, 1));
fprintf(fid, 'Mean wavelength: %.2e +/- %.2e\n', mean(wavelengths), std(wavelengths, 1));
fprintf(fid, 'Mean adhesion energy: %.2e +/- %.2e\n', mean(adhesionEnergies), std(adhesionEnergies, 1));
fprintf(fid, 'Adhesion energy from means: %.2e\n', adhesionEnergyFromMean);
fprintf(fid, 'Greatest length term: %.2e\n', max(lengthTerms));
fclose(fid);

end
