from langchain_community.tools.tavily_search import TavilySearchResults
#search api, optimized for generative ai workloads
#connects the agent to the internet 
#basically a web search ai 

def get_profile_url_tavily(name: str) -> str:
    """Search the web for a person's LinkedIn profile page"""
    search = TavilySearchResults(k=10)  # Assuming TavilySearchResults is the correct class
    result = search.run(f"{name} LinkedIn profile")
    return result


