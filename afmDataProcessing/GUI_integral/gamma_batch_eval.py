"""
Direct batch evaluation of gamma(lambda, A, h) -- no caching/interpolation.

Mirrors the method in Adhesionenergy.m: the bending-energy derivative
is evaluated by numerically integrating I1/I2, and the membrane-energy
derivative is evaluated in closed form via complete elliptic integrals
(no small-slope approximation).

Since gamma is only computed once per fitted dataset (10-50 datasets),
this direct evaluation on each call is fast enough.

Plug this in after your existing JSON-loading code, which already
gives you three lists: lam_list, A_list, h_list.
"""

import numpy as np
from scipy.integrate import quad
from scipy.special import ellipe, ellipk

# ------------------------------------------------------------------
# PLACEHOLDER CONSTANTS -- edit these (everything that's fixed
# across all datasets; h is NOT here since it varies per dataset)
# ------------------------------------------------------------------
E_val   = 5.7*10**9
L_val   = 10*10**-6
v_val   = 0.3
eps_val = 0.0255


# ------------------------------------------------------------------
# Numeric integrands -- mirror integrand1/integrand2 from Adhesionenergy.m
# ------------------------------------------------------------------
def _I1(lam, A):
    alpha = A * np.pi / lam
    integrand = lambda u: np.cos(u)**2 / (1 + alpha**2 * np.sin(u)**2)**3
    val, _ = quad(integrand, 0, 2*np.pi)
    return val

def _I2(lam, A):
    alpha = A * np.pi / lam
    integrand = lambda u: (np.cos(u)**2 * np.sin(u)**2) / (1 + alpha**2 * np.sin(u)**2)**4
    val, _ = quad(integrand, 0, 2*np.pi)
    return val


def gamma_numeric(lam, A, h, E=E_val, L=L_val, v=v_val, eps=eps_val):
    """Exact evaluation of gamma for a single (lambda, A, h), matching Adhesionenergy.m."""
    eps = abs(eps)
    E_bending = E / (1 - v**2)

    # Bending-energy derivative (dUb_dl)
    I1 = _I1(lam, A)
    I2 = _I2(lam, A)
    dUb_dl = (E_bending * h**3) / 12 * (
        -3 * A**2 * np.pi**3 / lam**4 * I1
        + 6 * A**4 * np.pi**5 / lam**6 * I2
    )

    # Membrane-energy derivative (dUm_dl) via complete elliptic integrals
    m = -(A**2 * np.pi**2) / lam**2
    EllE = ellipe(m)
    EllK = ellipk(m)
    EllE_deriv = -lam**2 / (2 * A**2 * np.pi**2) * (EllE - EllK)

    bracket1 = (2 * lam / np.pi * EllE - lam) / L - eps
    bracket2 = 2 / np.pi * EllE + 4 * A**2 / lam**2 * EllE_deriv - 1
    dUm_dl = E * h * bracket1 * bracket2

    return -dUm_dl - dUb_dl


def gamma_batch(lam_list, A_list, h_list, **fixed_constants):
    """
    Evaluate gamma for a whole set of fitted (lambda, A, h) triples.

    lam_list, A_list, h_list : equal-length sequences, one entry per
                                dataset/profile.
    fixed_constants          : optionally override E, L, v, eps for
                                all datasets, e.g. gamma_batch(..., L=2.0)

    Returns a numpy array of gamma values, same order as the inputs.
    """
    assert len(lam_list) == len(A_list) == len(h_list), \
        "lam_list, A_list, h_list must be the same length"

    results = np.empty(len(lam_list))
    for i, (lam, A, h) in enumerate(zip(lam_list, A_list, h_list)):
        results[i] = gamma_numeric(lam, A, h, **fixed_constants)
    return results


if __name__ == "__main__":
    # --- example usage, replace with your actual loaded lists ---
    lam_list = [1.2, 2.5, 0.8, 3.1]
    A_list   = [0.3, 0.6, 0.15, 0.9]
    h_list   = [0.05, 0.08, 0.03, 0.11]   # different h per profile

    gamma_vals = gamma_batch(lam_list, A_list, h_list)

    for lam, A, h, g in zip(lam_list, A_list, h_list, gamma_vals):
        print(f"lambda={lam:.3f}, A={A:.3f}, h={h:.3f}  ->  gamma = {g:.6e}")
