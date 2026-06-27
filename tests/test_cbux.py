# -*- coding: utf-8 -*-
import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.unit_x_calculator import UnitXCalculator
from src.core.hyperbolic_metric import (
    distance_poincare,
    distance_cycle,
    distance_minimisee,
    incertitude_effective,
    x_rho,
    incertitude_effective_correlee
)

class TestUnitXCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = UnitXCalculator(alpha=0.5, beta=0.3, gamma=0.2)
    
    def test_initialisation(self):
        self.assertEqual(self.calc.alpha, 0.5)
        self.assertEqual(self.calc.beta, 0.3)
        self.assertEqual(self.calc.gamma, 0.2)
    
    def test_calcul_taux(self):
        resultat = self.calc.calculer_taux()
        self.assertIn('taux', resultat)
        self.assertGreater(resultat['taux'], 0)
    
    def test_conversion(self):
        resultat = self.calc.calculer_taux()
        taux = resultat['taux']
        montant_x = 100.0
        montant_eur = self.calc.calculer_montant_eur(montant_x, taux)
        self.assertAlmostEqual(montant_eur, montant_x * taux, places=2)

class TestHyperbolicMetric(unittest.TestCase):
    def test_distance_poincare(self):
        d = distance_poincare(1, 2, 1, 2)
        self.assertAlmostEqual(d, 0.0, places=10)
    
    def test_distance_minimisee(self):
        F0, alpha0 = 1.0, 0.2
        nu = 1.0
        d = distance_minimisee(F0, alpha0, F0, nu)
        self.assertAlmostEqual(d, 0.0, places=10)
    
    def test_incertitude_effective(self):
        F0, alpha0 = 1.0, 0.2
        nu = 1.0
        sigma = incertitude_effective(F0, alpha0, F0, nu)
        self.assertAlmostEqual(sigma, alpha0, places=10)

if __name__ == "__main__":
    unittest.main()
