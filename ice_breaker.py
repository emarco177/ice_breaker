import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties import linkedin
from agents.linkedin_agents import lookup as linkedin_lookup_agent

import ollama
load_dotenv()

# Pull the model before using it
#ollama.pull_model('llama3.1')

information = """
    
"""
def ice_break_with(name: str):
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = linkedin.scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    # print(os.environ['OPENAI_API_KEY'])
    summary_template = """
    given the information about {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables="information", template=summary_template
    )
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = ChatOllama(model="mistral")
    #linkedin_data=linkedin.scrape_linkedin_profile(linkedin_profile_url='https://www.linkedin.com/in/eden-marco/')

    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"information": linkedin_data})
    print(res)  # Output: "Hello, World!"
if __name__ == "__main__":
    print("Hello Langchain")
    
    
