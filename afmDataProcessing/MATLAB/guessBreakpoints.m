function [bp1, bp2] = guessBreakpoints(x, row)
%GUESSBREAKPOINTS Seed an initial [firstBreakpoint, secondBreakpoint]
%guess from a change-point search on the profile's local slope.
%   [bp1, bp2] = GUESSBREAKPOINTS(x, row) mirrors the role of
%   ruptures.Dynp(model='rbf') on np.gradient(row) in the Python version:
%   it is only used to seed the very first row's initial guess in
%   fitProfiles.m, since every later row is warm-started from the
%   previous row's fitted parameters instead.
%
%   Requires the Signal Processing Toolbox (findchangepts).

n = numel(x);
dydx = gradient(row);

idx = findchangepts(dydx, 'MaxNumChanges', 2, 'Statistic', 'linear');
idx = sort(idx);

if numel(idx) < 2
    % Not enough change points found: fall back to thirds of the profile.
    idx = [max(1, round(n / 3)), max(1, round(2 * n / 3))];
elseif numel(idx) > 2
    idx = idx(1:2);
end

if idx(2) <= idx(1)
    idx(2) = min(idx(1) + 1, n);
end

bp1 = x(idx(1));
bp2 = x(idx(2));

end
