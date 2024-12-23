import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import(
    create_react_agent, # built in function in langchain
    AgentExecutor # runtime of the agent
)
from langchain import hub
from tools.tools import get_profile_url_tavily
def lookup(name: str) -> str:
    print(os.getenv('TAVILY_API_KEY'))
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini") #no creativity
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                        Your answer should contain only a URL""" #dont want fluff in the answer
    
    prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)
    tools_for_agent = [ #define tools for agent 
        Tool(
            name="Crawl Google 4 LinkedIn profile page", #displayed in logs
            func=get_profile_url_tavily, #python function to be used
            description="useful when you need to get the LinkedIn page url" #how the llm determines the llm will use this tool 
        )
    ]

    react_prompt = hub.pull("hwchase17/react") #username of harrison chase 
    #prompt that chase wrote for react prompting 
    #reasoning enginer for the agent 
    #prompt is sent to the llm 
    #langchain plugs in values for us, alot of heacy lifting done by langchain
    #implements react paper, uses the chain of thought research paper 
    #llm takes this and the scratch pad (history of the agent so far)
    #either returns an answer or a list of tools with arguments to use 

    agent = create_react_agent(llm, tools_for_agent, prompt=react_prompt)
    #accepts llm, tools, react prompt
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    #runtime of the agent 
    #verbose = print out the logs
    #agent = recipe, executor = cook, orchestrator

    result = agent_executor.invoke(
        input={"input": prompt_template.invoke({"name_of_person": name})}
    )

    linkedin_profile_url = result["output"]

    return linkedin_profile_url

if __name__ == "__main__":
    print(lookup(name = "Eden Marco"))