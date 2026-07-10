function profiles = fitProfiles(dataMatrix, pixelWidth, logFcn, progressFcn)
%FITPROFILES Fit each row's wrinkle profile once, independent of which
%adhesion energy model is applied downstream. Mirrors fit_profiles() in
%ProfileFitting.py.
%
%   profiles = FITPROFILES(dataMatrix, pixelWidth) fits every row of
%   dataMatrix (nRows x nCols) to piecewiseWrinkle and returns a struct
%   array with fields A, wavelength, R2 and params (the full fitted
%   parameter set), one entry per row that converged.
%
%   profiles = FITPROFILES(dataMatrix, pixelWidth, logFcn, progressFcn)
%   additionally routes convergence-failure messages through
%   logFcn(message) and, if supplied, calls progressFcn(rowIndex, nRows)
%   after every row.
%
%   Only the first row's initial guess comes from a change-point search
%   (see guessBreakpoints.m); every subsequent row is warm-started from
%   the previous row's fitted parameters, since consecutive rows in a
%   scan are similar and this is far cheaper than re-detecting
%   breakpoints for every row. If a row fails to converge, the guess used
%   for that row is kept as-is for the next attempt.
%
%   Requires the Optimization Toolbox (lsqcurvefit).

if nargin < 3 || isempty(logFcn)
    logFcn = @(msg) fprintf('%s\n', msg);
end
if nargin < 4
    progressFcn = [];
end

% Bump only when piecewiseWrinkle or the fitting procedure itself changes
% (i.e. anything that would change popt for a given row). Downstream
% calculations (adhesion formulas, R2, future stats) never need this bumped.
FIT_VERSION = 1; %#ok<NASGU>

paramNames = {'firstBreakpoint', 'secondBreakpoint', 'A', 'mLeft', 'bLeft', 'mRight', 'bRight'};

[nRows, nCols] = size(dataMatrix);
xValues = (0:nCols - 1) * pixelWidth;

lb = [xValues(1), xValues(1), -20, -Inf, -20, -Inf, -20];
ub = [xValues(end), xValues(end), Inf, Inf, Inf, Inf, Inf];

options = optimoptions('lsqcurvefit', 'Display', 'off');

profiles = struct('A', {}, 'wavelength', {}, 'R2', {}, 'params', {});
guess = [];

for i = 1:nRows
    row = dataMatrix(i, :);

    if isempty(guess)
        [bp1, bp2] = guessBreakpoints(xValues, row);
        aGuess = max(row) - median(row);
        baseline = median(row);
        guess = [bp1, bp2, aGuess, 0, baseline, 0, baseline];
    end

    [popt, ~, ~, exitflag] = lsqcurvefit(@piecewiseWrinkle, guess, xValues, row, lb, ub, options);

    if exitflag <= 0
        logFcn(sprintf('Row %d: failed to converge', i));
    else
        lam = popt(2) - popt(1);
        amp = popt(3);

        % Cheap to compute here (row/popt already in hand); storing it now means
        % this and any future post-fit diagnostic never has to redo lsqcurvefit.
        yfit = piecewiseWrinkle(popt, xValues);
        residuals = row - yfit;
        ssRes = sum(residuals .^ 2);
        ssTot = sum((row - mean(row)) .^ 2);
        r2 = 1 - ssRes / ssTot;

        profiles(end + 1) = struct('A', amp, 'wavelength', lam, 'R2', r2, ...
            'params', cell2struct(num2cell(popt(:)), paramNames(:), 1)); %#ok<AGROW>
        guess = popt;
    end

    if ~isempty(progressFcn)
        progressFcn(i, nRows);
    end
end

end
