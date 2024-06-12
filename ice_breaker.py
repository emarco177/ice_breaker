from dotenv import load_dotenv
import os
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain_community.llms.ollama import Ollama

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile


def ice_break_with(name:str) -> str :
    linkdIn_username = linkedin_lookup_agent(name)
    linkedIn_data = scrape_linkedin_profile(linkedin_profile_url=linkdIn_username,mock=True)

    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],template=summary_template
        )
    # linkedIn_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/satyanadella/")
    # llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")
    llm = Ollama(model="llama3")

    chain = LLMChain(llm= llm,prompt= summary_prompt_template)

    res = chain.invoke(input={"information": linkedIn_data})

    print(res)

if __name__ == '__main__':
    load_dotenv()
    # print(os.environ['OPENAI_API_KEY'])

    print("Ice Breaker Enter")

    ice_break_with(name="Bantu Sona")