# utils/outlook_utils.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

def get_outlook_token() -> str:
    """
    Authenticate using Client Credentials and return a Microsoft Graph access token.
    """
    tenant_id = os.getenv("MS_TENANT_ID")
    client_id = os.getenv("MS_CLIENT_ID")
    client_secret = os.getenv("MS_CLIENT_SECRET")
    scope = "https://graph.microsoft.com/.default"

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": scope
    }

    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def make_graph_api_request(endpoint: str, token: str, params: dict = None) -> dict:
    """
    Generic helper to make requests to Microsoft Graph API.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(f"{GRAPH_BASE_URL}/{endpoint}", headers=headers, params=params)
    response.raise_for_status()
    return response.json()
