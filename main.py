from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis n'importe quelle origine

# Votre token API Clash Royale
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM5MDkwMWEzLThjZGEtNGJiMi04NTRjLWNjZDhkMjc2ZDgxYiIsImlhdCI6MTc1OTY2MTIxOSwic3ViIjoiZGV2ZWxvcGVyLzc5NmI3NDZhLTZlMjEtMDBiZi0yNDVjLTc4NDY2YWVmMGUzOSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI5MC4xMDUuMTEwLjIwMyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.wIFwZ3aAzNml1PVPp34YYYsMF2xFGWSQi5iPunlyWla5CVBtcvVqVLNfIKYOVbFdu6s3MbBsQF3n8uhrWIeHBg'
API_BASE = 'https://api.clashroyale.com/v1'

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'message': 'Backend Clash Royale API est en ligne!',
        'endpoints': [
            '/api/player/<tag>',
            '/api/cards'
        ]
    })

@app.route('/api/player/<tag>')
def get_player(tag):
    """Récupère les informations d'un joueur par son tag"""
    try:
        # Nettoyer le tag (enlever le # s'il existe)
        clean_tag = tag.replace('#', '').upper()
        
        # Faire la requête à l'API Clash Royale
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Accept': 'application/json'
        }
        
        url = f'{API_BASE}/players/%23{clean_tag}'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({'error': 'Joueur non trouvé'}), 404
        else:
            return jsonify({'error': 'Erreur API', 'details': response.text}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cards')
def get_cards():
    """Récupère la liste de toutes les cartes"""
    try:
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Accept': 'application/json'
        }
        
        url = f'{API_BASE}/cards'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Erreur API', 'details': response.text}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Vérifier que l'API est accessible"""
    try:
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Accept': 'application/json'
        }
        
        # Test simple avec un tag connu
        response = requests.get(f'{API_BASE}/cards', headers=headers, timeout=5)
        
        if response.status_code == 200:
            return jsonify({'status': 'healthy', 'api': 'connected'})
        else:
            return jsonify({'status': 'unhealthy', 'api': 'disconnected'}), 503
            
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)