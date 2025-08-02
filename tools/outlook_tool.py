# tools/outlook_tool.py

from langchain.tools import tool
from utils.outlook_utils import get_outlook_token, make_graph_api_request

@tool
def get_user_emails(user_id: str, max_emails: int = 5) -> list:
    """
    Fetch recent Outlook emails for a given user (by userPrincipalName or ID).
    """
    token = get_outlook_token()
    response = make_graph_api_request(f"users/{user_id}/messages", token, {"$top": max_emails})
    return response.get("value", [])
