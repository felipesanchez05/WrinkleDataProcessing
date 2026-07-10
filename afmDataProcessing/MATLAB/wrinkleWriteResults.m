function wrinkleWriteResults(results, outputDir, inputFileStem, flakeLength, thickness)
%WRINKLEWRITERESULTS Write per-row results and summary statistics for the
%wrinkle-buckling adhesion energy model. Mirrors write_results() in
%WrinkleProcessing.py.

if isempty(results)
    error('wrinkleWriteResults:NoResults', 'No rows converged; nothing to write.');
end

meanWavelength = mean([results.wavelength]);
meanAmplitude = mean([results.A]);
adhesionEnergyFromMean = wrinkleAdhesion(flakeLength, thickness, meanWavelength, meanAmplitude);

writeAdhesionResults(results, outputDir, inputFileStem, adhesionEnergyFromMean);

end
