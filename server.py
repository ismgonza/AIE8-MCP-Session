from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dice_roller import DiceRoller
from webzio import Webzio

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

"""
Add your own tool here, and then use it through Cursor!
"""
# @mcp.tool()
# def YOUR_TOOL_NAME(query: str) -> str:
#     """YOUR_TOOL_DESCRIPTION"""
#     return "YOUR_TOOL_RESPONSE"

@mcp.tool()
def get_news(query: str, sentiment: str, language: str = "english") -> str:
    """Get the news for the given query, sentiment, and language
    
    Args:
        query: The search query for news articles (e.g., "climate change", "AI technology")
        sentiment: The sentiment filter - must be one of: positive, negative, or neutral
        language: The language of news articles (default: english)
    
    Returns:
        A formatted string containing news articles matching the search criteria
    """
    webzio = Webzio(query, sentiment, language)
    return str(webzio)

if __name__ == "__main__":
    mcp.run(transport="stdio")