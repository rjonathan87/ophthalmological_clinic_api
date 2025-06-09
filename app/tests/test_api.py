import requests
import json

# URL base
BASE_URL = 'http://127.0.0.1:8000/api/v1'

# 1. Obtener token
login_data = {
    'username': 'admin_user',
    'password': 'admin1234.',
    'grant_type': 'password',
    'scope': ''  # OAuth2 requiere este campo
}

# Intento de login
try:
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}
response = requests.post(f'{BASE_URL}/auth/token', data=login_data, headers=headers)
    print("\nRespuesta de autenticación:")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print("Body:")
    print(json.dumps(response.json() if response.text else {}, indent=2))
except Exception as e:
    print(f"Error en la autenticación: {str(e)}")

if response.status_code == 200:
    token = response.json()['access_token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # 2. Probar endpoint de roles
    response = requests.get(f'{BASE_URL}/roles', headers=headers)
    print("\nRespuesta del endpoint de roles:")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print("Body:")
    print(json.dumps(response.json() if response.text else {}, indent=2))
