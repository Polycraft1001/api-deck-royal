from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis n'importe quelle origine

# Récupérer le token depuis les variables d'environnement pour plus de sécurité
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZiZGU0ZGVkLTA5NTEtNDBhZS1hZGMyLTYxZDhiNWRhMGRmMyIsImlhdCI6MTc2MDUyNTg5Niwic3ViIjoiZGV2ZWxvcGVyLzc5NmI3NDZhLTZlMjEtMDBiZi0yNDVjLTc4NDY2YWVmMGUzOSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIwLjAuMC4wIl0sInR5cGUiOiJjbGllbnQifV19.dhYMLBd9VU51zBRPMlGqBOBBZCxBYZVw0BXPrX4ceUSfZP1QbtbHtpbUuU2V_pjbZWy7uGsmSVLWhfi4UkDsqg'


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
        clean_tag = tag.replace('#', '').upper()
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
        response = requests.get(f'{API_BASE}/cards', headers=headers, timeout=5)
        
        if response.status_code == 200:
            return jsonify({'status': 'healthy', 'api': 'connected'})
        else:
            return jsonify({'status': 'unhealthy', 'api': 'disconnected'}), 503
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

# Ne plus utiliser app.run() en production ; Gunicorn s'occupe du serveur
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
