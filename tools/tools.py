from langchain.agents import tool

from langchain.utilities import SerpAPIWrapper


@tool
def get_profile_url(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = SerpAPIWrapper()
    res = search.run(f"{name}")
    return res
