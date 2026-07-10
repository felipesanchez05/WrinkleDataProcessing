function fractureWriteResults(results, outputDir, inputFileStem, thickness)
%FRACTUREWRITERESULTS Write per-row results and summary statistics for
%the fracture-mechanics adhesion energy model. Mirrors write_results() in
%FractureMechanics.py.

if isempty(results)
    error('fractureWriteResults:NoResults', 'No rows converged; nothing to write.');
end

meanWavelength = mean([results.wavelength]);
meanAmplitude = mean([results.A]);
adhesionEnergyFromMean = fractureAdhesion(thickness, meanWavelength, meanAmplitude);

writeAdhesionResults(results, outputDir, inputFileStem, adhesionEnergyFromMean);

end
