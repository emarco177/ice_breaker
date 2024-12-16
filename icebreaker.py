from dotenv import load_dotenv
load_dotenv()  # This will load the variables from .env
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama;
from langchain_core.output_parsers import StrOutputParser

from third_parties.linkedin import scrape_linkedin_profile



if __name__ == "__main__":
    print("Hello Langchain")
    print(os.getenv('OPENAI_API_KEY'))
    print("stage 4")
    summary_template = """
         given the linkedin information {information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them
     """
    
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    #contains input variables and template
    #template = text before we inject variables 

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    #temperature = how creative the model is, 0 = least creative
    # llm = ChatOllama(model="llama3.2")
    # llm = ChatOllama(model='mistral')

    chain = summary_prompt_template | llm | StrOutputParser()
    #pipe operator comes drom langchain expresssion language
    #making an api call to openai

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/adam-punnoose/", mock=False)
    res = chain.invoke(input={"information": linkedin_data})
    print(res)
