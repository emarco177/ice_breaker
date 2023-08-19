from langchain.utilities import SerpAPIWrapper


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret


def get_profile_url(text: str):
    """Searches for Linkedin or twitter Profile Page."""
    # for debugging, cache past responses
    mapping = {
        "https://nz.linkedin.com/in/peter-gu-a6151134":["Peter Yongqi", "LinkedIn"],
        #'https://twitter.com/petergyang?lang=en':["Peter Yongqi", "Twitter"],
    }
    # if all values of the key are the same, return that value
    for key, value in mapping.items():
        # if each string in the key is found in text, then return value
        if all([string in text for string in value]):
            return key
    else: 
        #return the result from SerpAPI
        search = CustomSerpAPIWrapper()
        res = search.run(f"{text}")
        return res

def extract_twitter_username(url: str):
    """Extracts the twitter username from a twitter url."""
    # remove the leading https://twitter.com/ and the trailing /
    # remove any ?lang=xx query parameters
    return str(url.replace("https://twitter.com/", "").replace("/", "").split("?")[0])