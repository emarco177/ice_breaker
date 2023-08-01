from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from third_parties import linkedin
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from cliff_modules import cliff_pkg
import json


# information = """
#   Jessica Trinca, a business person who works in startups
# """
#
#
CONTEXT_LIMIT = 16384  #4096
MODEL_NAME = "gpt-3.5-turbo-16k"    #"gpt-3.5-turbo"
if __name__ == "__main__":
    #    print(f"Hello Langchain - ")
    #
    summary_template = """
        Given the information {information} about a person, I want you to create:
        1. A short summary
        2. Two interesting facts about them
    """

    linkedin_profile_name = "Cliff Rayman CTO CIO"
    linkedin_profile_url = linkedin_lookup_agent(linkedin_profile_name)
    #linkedin_profile_url = 'https://www.linkedin.com/in/cliffrayman/'
    #linkedin_profile_url = 'https://www.linkedin.com/in/larrytwersky'
    linkedin_data = linkedin.scrape_linkedin_profile(linkedin_profile_url, CONTEXT_LIMIT)

    print("len(linkedin_data=)", len(json.dumps(linkedin_data).encode("utf-8")))

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    #OPENAI_API_KEY = cliff_pkg.cliff_get_env('OPENAI_API_KEY')
    ##print('$Env:OPENAI_API_KEY = "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"')
 
    llm = ChatOpenAI(temperature=0, model_name=MODEL_NAME)
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    print(chain.run(information=linkedin_data))

    ##print(linkedin_data)

# endif
