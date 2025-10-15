from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# === Configuration ===
API_BASE = "https://api.clashroyale.com/v1"
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjNkNjVhNjA1LWY2NDMtNGJhZi04ZjFjLWM2NzM5NzA5M2NlZiIsImlhdCI6MTc2MDQ2Mjg5Niwic3ViIjoiZGV2ZWxvcGVyLzc5NmI3NDZhLTZlMjEtMDBiZi0yNDVjLTc4NDY2YWVmMGUzOSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI2Ni4zMy4yMi4yNTQiXSwidHlwZSI6ImNsaWVudCJ9XX0.RccEds9pKApSkjac4ji-DuheIqjntzYE8P7rB61GMf1QWY36UXKrHDRP-cKnRSi_VQsBhSLod3ZMT4C6bEB25g'

PROXIES = {
    "http": "http://tramway.proxy.rlwy.net:18838",
    "https": "http://tramway.proxy.rlwy.net:18838"
}

# === Routes ===
@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'message': '✅ Backend Clash Royale API est en ligne !',
        'endpoints': [
            '/api/player/<tag>',
            '/api/cards',
            '/api/health'
        ]
    })

@app.route('/api/player/<tag>')
def get_player(tag):
    try:
        clean_tag = tag.replace('#', '').upper()
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Accept': 'application/json'
        }
        url = f'{API_BASE}/players/%23{clean_tag}'
        response = requests.get(url, headers=headers, proxies=PROXIES, timeout=10)
        
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
    try:
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Accept': 'application/json'
        }
        url = f'{API_BASE}/cards'
        response = requests.get(url, headers=headers, proxies=PROXIES, timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Erreur API', 'details': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    try:
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Accept': 'application/json'
        }
        response = requests.get(f'{API_BASE}/cards', headers=headers, proxies=PROXIES, timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'healthy', 'api': 'connected'})
        else:
            return jsonify({'status': 'unhealthy', 'api': 'disconnected'}), 503
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

# === Lancement ===
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
