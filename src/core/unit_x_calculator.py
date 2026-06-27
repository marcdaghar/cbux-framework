# -*- coding: utf-8 -*-
import numpy as np
from datetime import datetime

class UnitXCalculator:
    def __init__(self, alpha=0.5, beta=0.3, gamma=0.2):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        self.matiere_weights = {
            'cuivre': 0.40,
            'acier': 0.35,
            'bois': 0.25
        }
        
        self.prix_ref = {
            'cuivre': 8.50,
            'acier': 0.70,
            'bois': 0.15
        }
    
    def get_prix_energie(self):
        return 0.15 + 0.001 * np.random.randn()
    
    def get_salaire_horaire(self):
        return 25.00 + 0.1 * np.random.randn()
    
    def get_indice_matieres(self):
        prix_cuivre = 8.50 + 0.5 * np.random.randn()
        prix_acier = 0.70 + 0.05 * np.random.randn()
        prix_bois = 0.15 + 0.02 * np.random.randn()
        
        indice = 100 * (
            0.40 * prix_cuivre / self.prix_ref['cuivre'] +
            0.35 * prix_acier / self.prix_ref['acier'] +
            0.25 * prix_bois / self.prix_ref['bois']
        )
        return indice
    
    def calculer_taux(self):
        P_energie = self.get_prix_energie()
        S_horaire = self.get_salaire_horaire()
        I_matieres = self.get_indice_matieres()
        
        taux = (self.alpha * P_energie + 
                self.beta * S_horaire + 
                self.gamma * I_matieres)
        
        return {
            'taux': taux,
            'P_energie': P_energie,
            'S_horaire': S_horaire,
            'I_matieres': I_matieres,
            'timestamp': datetime.now().isoformat()
        }
    
    def calculer_montant_eur(self, montant_x, taux):
        return montant_x * taux
