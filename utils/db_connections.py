import os
from pymongo import MongoClient
import pyodbc
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection
def get_mongo_client():
    mongo_uri = os.getenv("MONGODB_URI")
    return MongoClient(mongo_uri)

# Get MSSQL connection
def get_mssql_connection():
    server = os.getenv("MSSQL_SERVER")
    database = os.getenv("MSSQL_DATABASE")
    username = os.getenv("MSSQL_USERNAME")
    password = os.getenv("MSSQL_PASSWORD")

    connection_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    return pyodbc.connect(connection_str)

# Get Outlook access token using Microsoft Graph
def get_outlook_token():
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
