# tools/mongo_tool.py

from langchain.tools import tool
from utils.db_connections import get_mongo_client

@tool
def query_mongodb(database: str, collection: str, query: dict) -> list:
    """Query a MongoDB collection. Provide the database name, collection name, and a query dict."""
    client = get_mongo_client()
    db = client[database]
    results = db[collection].find(query)
    return [doc for doc in results]
