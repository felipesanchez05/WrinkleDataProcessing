"""
Direct batch evaluation of gamma(lambda, A, h) -- no caching/interpolation.

Since gamma is only computed once per fitted dataset (10-50 datasets),
direct numerical integration on each call is fast enough and more
accurate than building an interpolation table. This just loops over
your fitted (lambda, A, h) triples and integrates each one exactly.

Plug this in after your existing JSON-loading code, which already
gives you three lists: lam_list, A_list, h_list.
"""

import numpy as np
from scipy.integrate import quad

# ------------------------------------------------------------------
# PLACEHOLDER CONSTANTS -- edit these (everything that's fixed
# across all datasets; h is NOT here since it varies per dataset)
# ------------------------------------------------------------------
E_val   = 1.0
L_val   = 1.0
rho_val = 1.0
eps_val = 0.01


# ------------------------------------------------------------------
# Numeric integrands -- mirror I1, I2, J, K from gamma_equation.py
# ------------------------------------------------------------------
def _I1(lam, A):
    alpha = A * np.pi / lam
    integrand = lambda u: np.cos(u)**2 / (1 + alpha**2 * np.sin(u)**2)**3
    val, _ = quad(integrand, 0, 2*np.pi)
    return val

def _I2(lam, A):
    alpha = A * np.pi / lam
    integrand = lambda u: np.sqrt(1 + alpha**2 * np.sin(u)**2)
    val, _ = quad(integrand, 0, 2*np.pi)
    return val

def _J(lam, A):
    alpha = A * np.pi / lam
    integrand = lambda u: (np.cos(u)**2 * np.sin(u)**4) / (1 + alpha**2 * np.sin(u)**2)**4
    val, _ = quad(integrand, 0, 2*np.pi)
    return val

def _K(lam, A):
    alpha = A * np.pi / lam
    integrand = lambda u: np.sin(u)**2 / np.sqrt(1 + alpha**2 * np.sin(u)**2)
    val, _ = quad(integrand, 0, 2*np.pi)
    return val


def gamma_numeric(lam, A, h, E=E_val, L=L_val, rho=rho_val, eps=eps_val):
    """Exact numeric evaluation of gamma for a single (lambda, A, h)."""
    alpha = A * np.pi / lam

    I1 = _I1(lam, A)
    J  = _J(lam, A)
    term1 = -(E * h**3 * A * np.pi**3) / 12 * (
        -3 * I1 / lam**4 + 6 * (alpha**2 / lam**4) * J
    )

    I2 = _I2(lam, A)
    K  = _K(lam, A)
    factor_a = ((lam / (2*np.pi)) * I2 - lam) / L - abs(eps)
    factor_b = (1/L) * (I2/(2*np.pi) - (alpha**2/(2*np.pi)) * K - 1)
    term2 = -E * rho * h * L * factor_a * factor_b

    return term1 + term2


def gamma_batch(lam_list, A_list, h_list, **fixed_constants):
    """
    Evaluate gamma for a whole set of fitted (lambda, A, h) triples.

    lam_list, A_list, h_list : equal-length sequences, one entry per
                                dataset/profile.
    fixed_constants          : optionally override E, L, rho, eps for
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
