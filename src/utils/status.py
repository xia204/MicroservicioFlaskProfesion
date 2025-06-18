import requests

STATUS_URL_BASE = 'http://localhost:8080/api/status'

def obtener_status(status_id):
    response = requests.get(f'{STATUS_URL_BASE}/{status_id}')
    if response.status_code == 200:
        status_data = response.json()
        return {
            'id': status_data.get('id'),
            'nombre': status_data.get('nombre')
        }
    return None
