#!/bin/bash

echo "============================================================"
echo "INSTALLATION DU FRAMEWORK CBU-X"
echo "============================================================"

echo "[1] Vérification de Python..."
if command -v python3 &>/dev/null; then
    echo "  ✓ Python trouvé"
else
    echo "  ✗ Python 3 n'est pas installé."
    exit 1
fi

echo "[2] Création de l'environnement virtuel..."
python3 -m venv venv

echo "[3] Activation de l'environnement..."
source venv/bin/activate

echo "[4] Installation des dépendances..."
pip install -r requirements.txt

echo "[5] Création de la structure des répertoires..."
mkdir -p data logs

echo "============================================================"
echo "INSTALLATION TERMINÉE"
echo "============================================================"
