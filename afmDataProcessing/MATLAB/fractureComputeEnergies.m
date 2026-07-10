function results = fractureComputeEnergies(profiles, thickness)
%FRACTURECOMPUTEENERGIES Apply the fracture-mechanics adhesion energy
%model to already-fitted profiles. Mirrors compute_energies() in
%FractureMechanics.py.
%   results = FRACTURECOMPUTEENERGIES(profiles, thickness) returns a
%   struct array with fields A, wavelength, AdhesionEnergy, lengthTerm
%   and R2.

n = numel(profiles);
results = struct('A', cell(1, n), 'wavelength', cell(1, n), ...
    'AdhesionEnergy', cell(1, n), 'lengthTerm', cell(1, n), 'R2', cell(1, n));

for i = 1:n
    amp = profiles(i).A;
    lam = profiles(i).wavelength;
    [adhesionEnergy, term1] = fractureAdhesion(thickness, lam, amp);

    results(i).A = amp;
    results(i).wavelength = lam;
    results(i).AdhesionEnergy = adhesionEnergy;
    results(i).lengthTerm = term1;
    results(i).R2 = profiles(i).R2;
end

end
