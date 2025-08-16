import requests
import json
import os

def get_cpi_credentials():
    script_dir = os.path.dirname(__file__)
    credentials_path = os.path.join(script_dir, '..', '..', '..', 'credentials.json')
    try:
        with open(credentials_path, 'r') as f:
            credentials = json.load(f)
        return credentials['oauth']
    except FileNotFoundError:
        print(f"Error: credentials.json not found at {credentials_path}")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode credentials.json. Please check its format.")
        return None

def get_oauth_token():
    credentials = get_cpi_credentials()
    if not credentials:
        return None

    token_url = credentials['tokenurl']
    client_id = credentials['clientid']
    client_secret = credentials['clientsecret']

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        return token_data['access_token']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OAuth token: {e}")
        return None

def get_csrf_token(access_token):
    credentials = get_cpi_credentials()
    if not credentials:
        return None

    base_url = credentials['url']
    csrf_url = f"{base_url}/api/v1"

    headers = {
        'X-CSRF-Token': 'Fetch',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.get(csrf_url, headers=headers)
        response.raise_for_status()
        return response.headers.get('X-CSRF-Token')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CSRF token: {e}")
        return None
