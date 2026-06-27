# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.unit_x_calculator import UnitXCalculator

app = Flask(__name__)

calc = UnitXCalculator()

@app.route('/api/v1/exchange-rate', methods=['GET'])
def get_exchange_rate():
    currency = request.args.get('currency', 'X')
    
    if currency.upper() != 'X':
        return jsonify({'error': 'Seule la devise X est supportée'}), 400
    
    resultat = calc.calculer_taux()
    
    return jsonify({
        'base': 'X',
        'target': 'EUR',
        'rate': round(resultat['taux'], 2),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'valid_until': (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'cbx-calculator',
        'details': {
            'P_energie': round(resultat['P_energie'], 3),
            'S_horaire': round(resultat['S_horaire'], 2),
            'I_matieres': round(resultat['I_matieres'], 2)
        }
    })

@app.route('/api/v1/convert', methods=['POST'])
def convert_amount():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Données JSON requises'}), 400
    
    amount = data.get('amount')
    from_currency = data.get('from', 'X').upper()
    to_currency = data.get('to', 'EUR').upper()
    
    if from_currency != 'X':
        return jsonify({'error': 'Seule la conversion depuis X est supportée'}), 400
    
    if to_currency != 'EUR':
        return jsonify({'error': 'Seule la conversion vers EUR est supportée'}), 400
    
    resultat = calc.calculer_taux()
    taux = resultat['taux']
    
    return jsonify({
        'amount': amount,
        'from': from_currency,
        'to': to_currency,
        'rate': round(taux, 2),
        'result': round(amount * taux, 2),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
