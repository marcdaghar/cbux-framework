@echo off
echo ============================================================
echo INSTALLATION DU FRAMEWORK CBU-X
echo ============================================================

echo [1] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installe.
    pause
    exit /b 1
)

echo [2] Creation de l'environnement virtuel...
python -m venv venv

echo [3] Activation de l'environnement...
call venv\Scripts\activate.bat

echo [4] Installation des dependances...
pip install -r requirements.txt

echo [5] Creation de la structure...
mkdir data 2>nul
mkdir logs 2>nul

echo ============================================================
echo INSTALLATION TERMINEE
echo ============================================================
pause
