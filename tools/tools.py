
from langchain.utilities import SerpAPIWrapper


def get_profile_url(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = SerpAPIWrapper()
    res = search.run(f"{name}")
    return res
