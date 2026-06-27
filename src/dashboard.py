# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.unit_x_calculator import UnitXCalculator
from core.hyperbolic_metric import (
    distance_minimisee,
    incertitude_effective,
    incertitude_effective_correlee
)

st.set_page_config(
    page_title="CBU-X Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CBU-X : Tableau de bord")
st.markdown("*Monnaie de Compensation Multilatérale*")

with st.sidebar:
    st.header("⚙️ Paramètres")
    alpha = st.slider("α (Poids énergie)", 0.0, 1.0, 0.5, 0.05)
    beta = st.slider("β (Poids salaire)", 0.0, 1.0, 0.3, 0.05)
    gamma = st.slider("γ (Poids matières premières)", 0.0, 1.0, 0.2, 0.05)
    
    total = alpha + beta + gamma
    if total != 0:
        alpha /= total
        beta /= total
        gamma /= total
    
    st.subheader("Paramètres du cycle")
    F0 = st.number_input("Fonds initial (F0)", value=1.0, step=0.1)
    alpha0 = st.number_input("Incertitude initiale (α0)", value=0.2, step=0.05, min_value=0.01)
    nu = st.number_input("Courbure hyperbolique (ν)", value=1.0, step=0.1, min_value=0.1)
    rho = st.slider("Corrélation (ρ)", -0.9, 0.9, -0.3, 0.1)

st.header("💰 Taux de conversion X → euro")

col1, col2, col3 = st.columns(3)

with col1:
    calc = UnitXCalculator(alpha=alpha, beta=beta, gamma=gamma)
    resultat = calc.calculer_taux()
    taux = resultat['taux']
    st.metric("Taux X/EUR", f"1 X = {taux:.2f} €")

with col2:
    montant_x = st.number_input("Montant en X", value=100.0, step=10.0)
    montant_eur = montant_x * taux
    st.metric("Montant en euros", f"{montant_eur:.2f} €")

with col3:
    st.write("**Détails du calcul :**")
    st.write(f"P_énergie : {resultat['P_energie']:.3f} €")
    st.write(f"S_horaire : {resultat['S_horaire']:.2f} €")
    st.write(f"I_matériaux : {resultat['I_matieres']:.2f}")

st.header("📐 Coût de mutualisation")

FK_range = np.linspace(0.5, 2.0, 50)
d_star_range = [distance_minimisee(F0, alpha0, FK, nu) for FK in FK_range]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=FK_range,
    y=d_star_range,
    mode='lines',
    name="d*(FK)",
    line=dict(color='blue', width=2)
))
fig.add_vline(x=F0, line_dash="dash", line_color="red", annotation_text="F0")
fig.update_layout(
    title="Coût de mutualisation d*",
    xaxis_title="Fonds cible FK",
    yaxis_title="d*",
    height=300
)
st.plotly_chart(fig, use_container_width=True)

st.caption("© Marc Daghar - Licence CC BY-SA 4.0")
