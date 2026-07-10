function results = wrinkleComputeEnergies(profiles, flakeLength, thickness)
%WRINKLECOMPUTEENERGIES Apply the wrinkle-buckling adhesion energy model
%to already-fitted profiles. Mirrors compute_energies() in
%WrinkleProcessing.py.
%   results = WRINKLECOMPUTEENERGIES(profiles, flakeLength, thickness)
%   returns a struct array with fields A, wavelength, AdhesionEnergy and
%   lengthTerm.

n = numel(profiles);
results = struct('A', cell(1, n), 'wavelength', cell(1, n), ...
    'AdhesionEnergy', cell(1, n), 'lengthTerm', cell(1, n));

for i = 1:n
    amp = profiles(i).A;
    lam = profiles(i).wavelength;
    [adhesionEnergy, term1] = wrinkleAdhesion(flakeLength, thickness, lam, amp);

    results(i).A = amp;
    results(i).wavelength = lam;
    results(i).AdhesionEnergy = adhesionEnergy;
    results(i).lengthTerm = term1;
end

end
