# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import minimize_scalar

def distance_poincare(x1, y1, x2, y2):
    """
    Distance hyperbolique dans le demi-plan de Poincaré.
    """
    dx = x2 - x1
    dy = y2 - y1
    cosh_dist = 1 + (dx**2 + dy**2) / (2 * y1 * y2)
    cosh_dist = np.clip(cosh_dist, 1.0, None)
    return np.arccosh(cosh_dist)

def distance_cycle(F1, alpha1, F2, alpha2, nu=1.0, beta=1.0):
    """
    Distance dans l'espace d'état (F, alpha) de la guilde-cluster.
    """
    if beta == 1.0:
        x1 = np.log(F1)
        x2 = np.log(F2)
        y1 = alpha1 / nu
        y2 = alpha2 / nu
        dist_poincare = distance_poincare(x1, y1, x2, y2)
        return dist_poincare / nu
    else:
        Z1 = F1**(1 - beta) / (1 - beta) if beta != 1 else np.log(F1)
        Z2 = F2**(1 - beta) / (1 - beta) if beta != 1 else np.log(F2)
        x1, x2 = Z1, Z2
        y1 = alpha1 / nu
        y2 = alpha2 / nu
        dist_poincare = distance_poincare(x1, y1, x2, y2)
        return dist_poincare / nu

def distance_minimisee(F0, alpha0, FK, nu=1.0, beta=1.0):
    """
    Distance minimisée du point initial à la feuille {F = FK}.
    Coût de mutualisation d*.
    """
    if beta == 1.0:
        q = nu * abs(np.log(FK / F0)) / alpha0
        return np.arcsinh(q) / nu
    else:
        def objective(alpha):
            return distance_cycle(F0, alpha0, FK, alpha, nu, beta)
        result = minimize_scalar(objective, bounds=(1e-6, 10*alpha0), method='bounded')
        return result.fun

def incertitude_effective(F0, alpha0, FK, nu=1.0, beta=1.0):
    """
    Incertitude effective du cycle productif (formule de Hagan adaptée).
    """
    if beta == 1.0:
        z = nu * np.log(FK / F0) / alpha0
        if abs(z) < 1e-10:
            return alpha0
        sigma_eff = nu * np.log(FK / F0) / np.arcsinh(z)
        return abs(sigma_eff)
    else:
        d_star = distance_minimisee(F0, alpha0, FK, nu, beta)
        Z0 = F0**(1 - beta) / (1 - beta)
        ZK = FK**(1 - beta) / (1 - beta)
        delta_Z = abs(ZK - Z0)
        if delta_Z < 1e-10:
            return alpha0
        return delta_Z / d_star

def x_rho(z, rho):
    """
    Fonction x_rho(z) pour la formule de Hagan corrélée.
    """
    if abs(rho) >= 1:
        raise ValueError("rho doit être strictement compris entre -1 et 1")
    
    sqrt_term = np.sqrt(1 - 2 * rho * z + z**2)
    numerator = sqrt_term + z - rho
    denominator = 1 - rho
    return np.log(numerator / denominator)

def incertitude_effective_correlee(F0, alpha0, FK, nu=1.0, rho=0.0):
    """
    Incertitude effective avec corrélation (skew).
    """
    z = nu * np.log(FK / F0) / alpha0
    if abs(z) < 1e-10:
        return alpha0
    return nu * np.log(FK / F0) / x_rho(z, rho)

# Exemple d'utilisation
if __name__ == "__main__":
    F0, alpha0 = 1.0, 0.2
    FK = 1.5
    nu = 1.0
    
    print("=" * 60)
    print("GÉOMÉTRIE HYPERBOLIQUE - CBU-X")
    print("=" * 60)
    
    d_star = distance_minimisee(F0, alpha0, FK, nu)
    sigma_eff = incertitude_effective(F0, alpha0, FK, nu)
    
    print(f"Point initial : F0 = {F0}, alpha0 = {alpha0}")
    print(f"Point cible : FK = {FK}")
    print(f"Coût de mutualisation (d*) : {d_star:.4f}")
    print(f"Incertitude effective (sigma_eff) : {sigma_eff:.4f}")
    
    for rho in [-0.5, 0.0, 0.5]:
        sigma_corr = incertitude_effective_correlee(F0, alpha0, FK, nu, rho)
        print(f"sigma_eff (rho = {rho}) : {sigma_corr:.4f}")
