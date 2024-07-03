from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from third_parties.linkedin import scrape_linkedin_profile


if __name__ == '__main__':
    load_dotenv() # load environment variables dynamically
    
    summary_template = """
    given the LinkedIn information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """
    
    summary_prompt_template = PromptTemplate(
        input_valriables=['information'], template=summary_template
    )
    
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url = "https://www.linkedin.com/in/hyunh317/"
    )
    
    res = chain.invoke(input={"information": linkedin_data})
    
    print(res['text'])