# -*- coding: utf-8 -*-
"""
Module : api_taux.py
API REST pour le taux de conversion X → euro
Auteur : Marc Daghar
Licence : CC BY-SA 4.0
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import redis
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.unit_x_calculator import UnitXCalculator

app = Flask(__name__)

# Configuration Redis avec gestion d'erreur
try:
    cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
    cache.ping()  # Vérifie que Redis est accessible
    print("✅ Redis connecté avec succès")
except redis.ConnectionError:
    print("⚠️ Redis non disponible - le cache sera désactivé")
    cache = None

calc = UnitXCalculator()

# Durée de validité du cache (12 heures)
CACHE_DURATION = 12 * 60 * 60

@app.route('/api/v1/exchange-rate', methods=['GET'])
def get_exchange_rate():
    """
    Endpoint : récupère le taux de conversion X → euro.
    
    Paramètres optionnels :
        - date : date au format YYYY-MM-DD (défaut : aujourd'hui)
        - currency : 'X' (défaut) ou 'EUR'
    
    Exemple :
        GET /api/v1/exchange-rate?date=2026-06-15&currency=X
    """
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    currency = request.args.get('currency', 'X')
    
    # Validation du format de date
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}), 400
    
    if currency.upper() != 'X':
        return jsonify({'error': 'Seule la devise X est supportée'}), 400
    
    # Vérification du cache (si Redis disponible)
    if cache:
        cache_key = f"taux_{date_str}_{currency}"
        cached = cache.get(cache_key)
        if cached:
            return jsonify(json.loads(cached))
    
    # Calcul du taux
    resultat = calc.calculer_taux()
    
    # Construction de la réponse
    response = {
        'base': 'X',
        'target': 'EUR',
        'rate': round(resultat['taux'], 4),
        'date': date_str,
        'valid_until': (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'cbx-calculator',
        'details': {
            'P_energie': round(resultat['P_energie'], 4),
            'S_horaire': round(resultat['S_horaire'], 2),
            'I_matieres': round(resultat['I_matieres'], 2)
        }
    }
    
    # Mise en cache (si Redis disponible)
    if cache:
        cache.setex(cache_key, CACHE_DURATION, json.dumps(response))
    
    return jsonify(response)

@app.route('/api/v1/convert', methods=['POST'])
def convert():
    """
    Endpoint : convertit un montant X → euro (ou euro → X).
    
    Body JSON :
        {
            "amount": 100.0,
            "from": "X",
            "to": "EUR",
            "date": "2026-06-15" (optionnel)
        }
    
    Exemple :
        POST /api/v1/convert
        {
            "amount": 100,
            "from": "X",
            "to": "EUR"
        }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données JSON requises'}), 400
    
    amount = data.get('amount')
    if amount is None:
        return jsonify({'error': 'Le champ "amount" est requis'}), 400
    
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return jsonify({'error': 'Le montant doit être un nombre valide'}), 400
    
    from_currency = data.get('from', 'X').upper()
    to_currency = data.get('to', 'EUR').upper()
    date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Validation du format de date
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}), 400
    
    # Récupération du taux (avec cache si possible)
    if cache:
        cache_key = f"taux_{date_str}_X"
        cached = cache.get(cache_key)
        if cached:
            taux_data = json.loads(cached)
            taux = taux_data['rate']
        else:
            taux = calc.calculer_taux()['taux']
    else:
        taux = calc.calculer_taux()['taux']
    
    # Conversion
    if from_currency == 'X' and to_currency == 'EUR':
        result = amount * taux
        rate_used = taux
    elif from_currency == 'EUR' and to_currency == 'X':
        if taux == 0:
            return jsonify({'error': 'Taux de conversion nul'}), 400
        result = amount / taux
        rate_used = taux
    else:
        return jsonify({
            'error': f'Conversion non supportée: {from_currency} → {to_currency}',
            'supported_pairs': ['X → EUR', 'EUR → X']
        }), 400
    
    return jsonify({
        'amount': amount,
        'from': from_currency,
        'to': to_currency,
        'rate': round(rate_used, 4),
        'result': round(result, 2),
        'date': date_str,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    Endpoint de santé pour vérifier le bon fonctionnement du service.
    """
    status = {
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'redis': 'connected' if cache else 'disconnected'
    }
    
    if not cache:
        status['warning'] = 'Redis non disponible - cache désactivé'
    
    return jsonify(status)

@app.route('/api/v1/cache/clear', methods=['DELETE'])
def clear_cache():
    """
    Endpoint pour vider le cache Redis.
    (Utile pour le développement et le débogage)
    """
    if not cache:
        return jsonify({'error': 'Redis non disponible'}), 503
    
    try:
        # Supprime toutes les clés qui commencent par "taux_"
        keys = cache.keys("taux_*")
        if keys:
            cache.delete(*keys)
        return jsonify({
            'message': f'Cache vidé: {len(keys)} clés supprimées',
            'keys_deleted': len(keys)
        })
    except Exception as e:
        return jsonify({'error': f'Erreur lors du nettoyage du cache: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trouvé'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur interne du serveur'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("CBU-X API v1.0.0")
    print("=" * 60)
    print(f"📅 Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 URL: http://localhost:5000")
    print("📚 Endpoints disponibles:")
    print("  - GET  /api/v1/exchange-rate  (taux de conversion)")
    print("  - POST /api/v1/convert       (conversion de montant)")
    print("  - GET  /api/v1/health        (vérification de santé)")
    print("  - DELETE /api/v1/cache/clear (vider le cache)")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
