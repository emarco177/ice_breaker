import os;
import requests;
from dotenv import load_dotenv;

load_dotenv();

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from a linkedin profiles, 
    manually scrape the information from the linkedin profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/adampunnoose/627e1532fd5ea450c1f00bb7067078b0/raw/cda4bdd02c02f94b13e467df02847cb0ed2f809b/gistfile1.txt"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )
    data = response.json()
    data = { #removes empty values
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"): #removes empty values
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/adam-punnoose/",
            mock=True
        )
    )
