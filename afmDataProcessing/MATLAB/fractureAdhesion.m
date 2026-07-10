function [adhesionEnergy, term1, term2, term3] = fractureAdhesion(thickness, wavelength, amplitude)
%FRACTUREADHESION Adhesion energy from the fracture-mechanics model.
%   Mirrors adhesion() in FractureMechanics.py.
%   [adhesionEnergy, term1, term2, term3] = FRACTUREADHESION(thickness,
%   wavelength, amplitude)

E = 5.7e9;

term1 = pi^4 / 6;
term2 = (thickness^3 * amplitude^2) / wavelength^4;
term3 = E;

adhesionEnergy = term1 * term2 * term3;

end
