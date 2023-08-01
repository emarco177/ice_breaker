##################################
# linkedin_lookup_agent.py
# originally for udemy online class ice_breaker
# 000. 202307287, cliff
##################################
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import get_profile_url

CONTEXT_LIMIT = 16384  # 4096
MODEL_NAME = "gpt-3.5-turbo-16k"  # "gpt-3.5-turbo"


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name=MODEL_NAME)
    summary_template = """Given the full name of a perspn {name_of_person} I want you to get me a link to their LinkedIn profile page.
        Your response should contain only a URL without any additional surrounding text or spaces.
        Your response should look something like: ###https://www.linkedin.com/in/pageidentifier/###
        Validate that the link actually exists and does not return an http status code error of 404. If it does, try again."""
    tools_for_agent = [
    Tool(
            name="Crawl Google for LinkedIn profile page",
            func=get_profile_url,
            description="useful for when you need to find and return the URL for LinkedIn profile page",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=summary_template, input_variables=["name_of_person"]
    )

    linkedin_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))

    return linkedin_profile_url


# enddef
