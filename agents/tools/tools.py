from langchain_community.tools.tavily_search import TavilySearchResults
#an search api that is highly utilized for genai

def get_profile_url_tavily(name: str):
    """Search for a profile on Tavily and return the URL."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]