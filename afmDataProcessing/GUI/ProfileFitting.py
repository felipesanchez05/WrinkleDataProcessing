# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 11:21:25 2026

@author: felsa
"""
import numpy as np
import ruptures as rpt
import scipy.optimize as sp
from math import pi

# Bump only when piecewise_wrinkle or the fitting procedure itself changes
# (i.e. anything that would change popt for a given row). Downstream
# calculations (adhesion formulas, R2, future stats) never need this bumped.
FIT_VERSION = 1

PARAM_NAMES = ('first_breakpoint', 'second_breakpoint', 'A', 'm_left', 'b_left', 'm_right', 'b_right')


def piecewise_wrinkle(x, first_breakpoint, second_breakpoint, A, m_left, b_left, m_right, b_right):
    y = np.zeros_like(x)
    left_mask = x < first_breakpoint
    right_mask = x > second_breakpoint
    wrinkle_mask = (x >= first_breakpoint) & (x <= second_breakpoint)
    y[left_mask] = m_left * x[left_mask] + b_left
    y[right_mask] = m_right * x[right_mask] + b_right
    lam = second_breakpoint - first_breakpoint
    base = m_left * first_breakpoint + b_left
    midpoint = (first_breakpoint + second_breakpoint) / 2
    y[wrinkle_mask] = base + (A / 2) * (1 + np.cos(2 * pi * (x[wrinkle_mask] - midpoint) / lam))

    return y


def _breakpoint_guess(row, x_values):
    """Use ruptures to seed the initial breakpoint guess for the first profile only."""
    dydx = np.gradient(row)
    algo = rpt.Dynp(model='rbf').fit(dydx)
    breakpoints = algo.predict(n_bkps=2)
    bp1_id = breakpoints[0]
    bp2_id = breakpoints[1] - 1
    return x_values[bp1_id], x_values[bp2_id]


def fit_profiles(data_matrix, pixel_width, progress_callback=None, log_callback=print):
    """Fit each row's wrinkle profile once, independent of which adhesion energy model is applied downstream.

    Only the first row's initial guess comes from ruptures breakpoint detection; every
    subsequent row is warm-started from the previous row's fitted parameters, since
    consecutive rows in a scan are similar and this is far cheaper than re-detecting
    breakpoints for every row.
    """
    profiles = []
    nx = data_matrix.shape[1]
    x_values = np.arange(nx) * pixel_width
    total_rows = data_matrix.shape[0]

    lower = [x_values[0], x_values[0], -20, -np.inf, -20, -np.inf, -20]
    upper = [x_values[-1], x_values[-1], np.inf, np.inf, np.inf, np.inf, np.inf]

    guess = None
    for i, row in enumerate(data_matrix):
        try:
            if guess is None:
                bp1, bp2 = _breakpoint_guess(row, x_values)
                A_guess = np.max(row) - np.median(row)
                baseline = np.median(row)
                guess = [bp1, bp2, A_guess, 0, baseline, 0, baseline]

            popt, pcov = sp.curve_fit(piecewise_wrinkle, x_values, row, p0=guess, bounds=(lower, upper))

            lam = popt[1] - popt[0]
            amp = popt[2]

            # Cheap to compute here (row/popt already in hand); storing it now means
            # this and any future post-fit diagnostic never has to redo curve_fit.
            yfit = piecewise_wrinkle(x_values, *popt)
            residuals = row - yfit
            SS_res = np.sum(residuals ** 2)
            SS_tot = np.sum((row - np.mean(row)) ** 2)
            R2 = 1 - SS_res / SS_tot

            profiles.append({
                'A': amp,
                'wavelength': lam,
                'R2': R2,
                'params': dict(zip(PARAM_NAMES, popt.tolist())),
            })
            guess = popt
        except RuntimeError:
            log_callback(f"Row {i}: failed to converge")
        if progress_callback:
            progress_callback(i + 1, total_rows)
    return profiles
