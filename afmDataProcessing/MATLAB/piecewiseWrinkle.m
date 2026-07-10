function y = piecewiseWrinkle(p, x)
%PIECEWISEWRINKLE Piecewise linear-cosine wrinkle profile model.
%   y = PIECEWISEWRINKLE(p, x) evaluates the model at the points in x
%   given parameter vector
%       p = [firstBreakpoint, secondBreakpoint, A, mLeft, bLeft, mRight, bRight]
%   Two linear segments (left/right of the wrinkle) are joined by a raised
%   cosine "bump" of amplitude A between the two breakpoints. Matches
%   piecewise_wrinkle() in ProfileFitting.py.

x = x(:)';
firstBreakpoint  = p(1);
secondBreakpoint = p(2);
A      = p(3);
mLeft  = p(4);
bLeft  = p(5);
mRight = p(6);
bRight = p(7);

y = zeros(size(x));
leftMask    = x < firstBreakpoint;
rightMask   = x > secondBreakpoint;
wrinkleMask = (x >= firstBreakpoint) & (x <= secondBreakpoint);

y(leftMask)  = mLeft * x(leftMask) + bLeft;
y(rightMask) = mRight * x(rightMask) + bRight;

lam = secondBreakpoint - firstBreakpoint;
base = mLeft * firstBreakpoint + bLeft;
midpoint = (firstBreakpoint + secondBreakpoint) / 2;
y(wrinkleMask) = base + (A / 2) * (1 + cos(2 * pi * (x(wrinkleMask) - midpoint) / lam));

end
