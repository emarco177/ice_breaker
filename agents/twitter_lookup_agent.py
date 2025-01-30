from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

from dotenv import load_dotenv
from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    template = """
       given the name {name_of_person} I want you to find a link to their Twitter/ X profile page, and extract from it their username
       In Your Final answer only the person's username
       which is extracted from: https://x.com/USERNAME"""
    tools_for_agent_twitter = [
        Tool(
            name="Crawl Google 4 Twitter profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Twitter Page URL",
        ),
    ]

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm, tools=tools_for_agent_twitter, prompt=react_prompt
    )
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent_twitter, verbose=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    twitter_username = result["output"]

    return twitter_username
