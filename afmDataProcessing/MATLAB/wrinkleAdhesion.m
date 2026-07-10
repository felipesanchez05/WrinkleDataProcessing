function [adhesionEnergy, term1, term2, term3] = wrinkleAdhesion(flakeLength, thickness, wavelength, amplitude)
%WRINKLEADHESION Adhesion energy from the wrinkle-buckling model.
%   Mirrors adhesion() in WrinkleProcessing.py.
%   [adhesionEnergy, term1, term2, term3] = WRINKLEADHESION(flakeLength,
%   thickness, wavelength, amplitude)

E = 5.7e9;
strain = 0.03;

term1 = (pi^4 * amplitude^4 * E * thickness) / (16 * wavelength * flakeLength);
term2 = (strain * pi^2 * amplitude^2 * E * thickness) / (4 * wavelength^2);
term3 = (pi^4 * amplitude^2 * E * thickness^3) / (4 * wavelength^4);

adhesionEnergy = term1 - term2 + term3;

end
