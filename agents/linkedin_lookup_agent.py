from dotenv import load_dotenv
import os
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain_community.llms.ollama import Ollama
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
    )
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

def lookup(name:str) -> str:
    llm = Ollama(model="dolphin-mistral",temperature=0)
    template = """given the full name {name_of_person} I want you to get me a valid link or URL to their Linkedin profile page. """
    prompt_template = PromptTemplate(
    template=template, input_variables=["name_of_person"]
    )
    
    tools_for_agent = [
        Tool(
            name="Crawl Google For LinkedIn Page URL",
            func=get_profile_url_tavily,
            description="useful for when you want to get the LinkedIn page URL"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=20
        )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    linkedin_profile_url = result["output"]
    return linkedin_profile_url


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]


if __name__ == "__main__":
    linkedin_url = lookup(name="Subhadeep Chakraborty")
    print(linkedin_url)