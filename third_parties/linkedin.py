import os
import requests
from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama
from langchain.chains.llm import LLMChain
from langchain.prompts.prompt import PromptTemplate

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url:str,mock:bool=True):
    """Scrape info from Linkedin profiles
    Manually scrape info from Linkedin profiles"""

    summary_template = """From the given string - {linkedin_profile_url} ,extract only the first linkedin profile URL as answer. Make sure the answer has only the URL nothing else"""
    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_profile_url"],template=summary_template
        )
    #Code to make sure the linkdin url is a URL for sure
    llm = Ollama(model="llama3")

    chain = LLMChain(llm= llm,prompt= summary_prompt_template)

    linkedin_profile_url = chain.invoke(input={"linkedin_profile_url": linkedin_profile_url})

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/jellybeantatai/8aa85ad8f8a2286fad924606d7273d9c/raw/832322a3d628fc7eb818cdf76c1f206518408831/satyaLinkedin.json"
        response = requests.get(linkedin_profile_url,timeout=10)

    else:
        api_key = os.environ.get("PROXYCURL_API_KEY")
        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url': linkedin_profile_url["text"],
            # 'twitter_profile_url': 'https://twitter.com/abhinabakar',
            # 'facebook_profile_url': 'https://www.facebook.com/abhinaba94',
            'personal_contact_number': 'include',
            'personal_email': 'include',
            'inferred_salary': 'include',
            'skills': 'include',
            'use_cache': 'if-present',
            'fallback_to_cache': 'on-error',
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers)

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data
    
if __name__ == "__main__":
    print(scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/satyanadella/"
    ))