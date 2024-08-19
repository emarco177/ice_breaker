from dotenv import load_dotenv

load_dotenv()
import os
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
from tools.tools import get_profile_url_tavily

def lookup(name: str):
    llm = ChatOpenAI(temperature=0, tiktoken_model_name="gpt-3.5-turbo")
    template = """given the full name{name_of_person} I want to you to get it me a link to theri Linkedin profile page. your answer should contain only a URL"""

    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the linkedin page url" 
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__=="__main__":
    linkedin_url = lookup(name="Eden Marco")
    print(linkedin_url)  # prints the linkedin profile url of Eden Marco



