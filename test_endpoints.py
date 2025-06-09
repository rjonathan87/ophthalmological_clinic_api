import requests
import json

def test_api():
    # URL base
    BASE_URL = 'http://127.0.0.1:8000/api/v1'

    # 1. Obtener token
    login_data = {
        'username': 'admin_user',
        'password': 'admin1234.',
        'grant_type': 'password',
        'scope': ''  # OAuth2 requiere este campo
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    try:
        print("\nIntentando autenticación...")
        auth_response = requests.post(
            f'{BASE_URL}/auth/token',
            data=login_data,
            headers=headers
        )
        print(f"Status Code: {auth_response.status_code}")
        print(f"Headers: {dict(auth_response.headers)}")
        print("Response Body:")
        print(json.dumps(auth_response.json() if auth_response.text else {}, indent=2))

        if auth_response.status_code == 200:
            token = auth_response.json()['access_token']
            auth_headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/json'
            }
            
            # 2. Probar endpoint de roles
            print("\nProbando endpoint de roles...")
            roles_response = requests.get(
                f'{BASE_URL}/roles',
                headers=auth_headers
            )
            print(f"Status Code: {roles_response.status_code}")
            print(f"Headers: {dict(roles_response.headers)}")
            print("Response Body:")
            print(json.dumps(roles_response.json() if roles_response.text else {}, indent=2))

            # 3. Probar otros endpoints
            endpoints = [
                '/users',
                '/clinics',
                '/permissions',
                '/role-permissions'
            ]

            for endpoint in endpoints:
                print(f"\nProbando endpoint {endpoint}...")
                response = requests.get(
                    f'{BASE_URL}{endpoint}',
                    headers=auth_headers
                )
                print(f"Status Code: {response.status_code}")
                if response.status_code != 200:
                    print(f"Error: {response.text}")
                else:
                    print("Response Body:")
                    print(json.dumps(response.json(), indent=2))

    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_api()
