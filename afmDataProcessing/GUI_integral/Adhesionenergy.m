
A = 94.7.*10^-9; 

l = 1.58 .*10^-6;
v = 0.3;
E = 5.7.*10^9;
E_bending = E./(1-v^2);
L = 10.*10^-6;
t = 336 .*10^-9; 


strain = 0.0255;  
strain = abs(strain);



Baseadhesion =  -(strain * pi^2 * A^2 * E * t / (4 * l^2)) + (pi^4 * A^2 * E_bending * t^3 / (4 * l^4));


%{

alpha = (A * pi) / l;

I1 = integral(@(u) (cos(u).^2) ./ (1 + alpha^2 * sin(u).^2).^3, 0, 2*pi);
J  = integral(@(u) (cos(u).^2 .* sin(u).^2) ./ (1 + alpha^2 * sin(u).^2).^4, 0, 2*pi);

bracket = -3 * I1 / l^4 + 6 * alpha^2 * J / l^4;

I2 = integral(@(u) sqrt(1 + alpha^2 * sin(u).^2), 0, 2*pi);
I3 = integral(@(u) sin(u).^2 ./ sqrt(1 + alpha^2 * sin(u).^2), 0, 2*pi);

T = (l/(2*pi) * I2 - l) / L - strain;
dT_dl = (1/L) * ( (I2/(2*pi)) - (alpha^2/(2*pi))*I3 - 1 );

Integraladhesion = -(E_bending * h^3 * A * pi^3 / 12) * bracket - E * h * L * T * dT_dl;

%}

% Derived parameter
k = A * pi / l;

% Define the integrands
integrand1 = @(u) (cos(u).^2) ./ (1 + k^2 * sin(u).^2).^3;
integrand2 = @(u) (cos(u).^2 .* sin(u).^2) ./ (1 + k^2 * sin(u).^2).^4;

% Numerical evaluation of the integrals
I1 = integral(integrand1, 0, 2*pi);
I2 = integral(integrand2, 0, 2*pi);

% Compute the derivative
dUb_dl = (E_bending.*t^3)./12.*(-3 * A^2 * pi^3 / l^4 * I1 ...
              + 6 * A^4 * pi^5 / l^6 * I2);

% Display result
%disp(dUb_dl)


% Define the parameter for the elliptic integrals
m = - (A^2 * pi^2) / l^2;

% Complete elliptic integrals
EllE = ellipticE(m);        % Second kind
EllK = ellipticK(m);        % First kind

% Derivative of ellipticE
EllE_deriv = -l^2 / (2 * A^2 * pi^2) * (EllE - EllK);

% The first bracket term
bracket1 = (2 * l / pi * EllE - l) / L - strain;

% The second bracket term
bracket2 = 2 / pi * EllE + 4 * A^2 / l^2 * EllE_deriv - 1;

% The total derivative
dUm_dl = E * t * bracket1 * bracket2;

% Display the result
%disp(dUm_dl)

%display adhesion energies
totaladhesion = -dUm_dl - dUb_dlambda;
disp('total adhesion');
disp(totaladhesion);
disp('small slope adhesion');
disp(Baseadhesion);
%{
A = 94.7.*10^-9;      % Amplitude (meters), from sinusoidal fit
lambda = 1.58 .*10^-6; % Wavelength (meters), from sinusoidal fit
epsilon = -0.0255;% strain (dimensionless)
h = 336 .*10^-9;      % thickness (meters)
Eh = 5.7.*10^9;     % modulus (Pascals)
L = 10*10^-6;   % use lambda for per-wavelength calculation

%}