import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from utils.place_info_search import TavilySearchTool

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.tavily_search = TavilySearchTool()
        self.search_anything_tool = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup a single tool that can answer any internet query using Tavily.
        """

        @tool
        def internet_search(query: str) -> str:
            """
            Search the internet to answer any general or real-time query.
            Example: "Latest news on AI", "Top places to visit in Japan", etc.
            """
            result = self.tavily_search.search_anything(query)
            return f"📡 Internet answer:\n{result}"

        return [internet_search]
