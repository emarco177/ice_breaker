from dotenv import load_dotenv
load_dotenv()  # This will load the variables from .env
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama;
from langchain_core.output_parsers import StrOutputParser

from output_parsers import summary_parser;
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent;

def ice_break_with(name: str) -> str:
    linkedin_url = linkedin_lookup_agent(name=name) #get linkedin url
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=False) #get linkedin data

    summary_template = """
         given the linkedin information {information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them

        \n {format_instructions}
     """
    
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )
    #contains input variables and template
    #template = text before we inject variables 

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    #temperature = how creative the model is, 0 = least creative
    # llm = ChatOllama(model="llama3.2")
    # llm = ChatOllama(model='mistral')

    # chain = summary_prompt_template | llm | StrOutputParser()
    #pipe operator comes drom langchain expresssion language
    #making an api call to openai

    chain = summary_prompt_template | llm | summary_parser
    #langhain expression model (syntax)

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=False)
    res = chain.invoke(input={"information": linkedin_data})
    print(res)



if __name__ == "__main__":
    load_dotenv()
    print(os.getenv('OPENAI_API_KEY'))
    print(ice_break_with("jamie dimon"))