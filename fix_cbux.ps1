# Correction des imports pour hyperbolic_metric.py
$file = "src/core/hyperbolic_metric.py"
$content = Get-Content $file -Raw
$content = $content -replace "from scipy.special import arcsinh, arccosh", "from scipy.special import asinh as arcsinh, acosh as arccosh"
$content | Out-File -FilePath $file -Encoding UTF8
Write-Host "✅ hyperbolic_metric.py corrigé"

# Installer les dépendances manquantes
pip install flask redis requests matplotlib plotly streamlit statsmodels scikit-learn web3 eth-account py-solc-x --quiet
Write-Host "✅ Dépendances installées"

Write-Host ""
Write-Host "🚀 Vous pouvez maintenant lancer l'API et le dashboard"
