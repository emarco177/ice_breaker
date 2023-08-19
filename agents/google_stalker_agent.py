from tools.tools import get_profile_url
from bs4 import BeautifulSoup
import requests

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.utilities import SerpAPIWrapper
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    messages_from_dict,
    messages_to_dict,
)


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # llm = ChatOpenAI(temperature=0, model_name="gpt4")

    template = """given the person '{name_of_person}' I want you to find webpages that refer to this individual."""
    tools_for_agent1 = [
        Tool(
            name="Search",
            func=google_scraper,    
            description="useful for reading webpages found by a Google search",
        ),
    ]

    agent = initialize_agent(
        tools_for_agent1, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
    )
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )
    

    return agent.run(prompt_template.format_prompt(name_of_person=name))

def google_scraper(query):
    search = SerpAPIWrapper()
    results_page = search.results(query)
    text_results = ""
    for result in results_page["organic_results"]:
        response = requests.get(result["link"])
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        body_text_only = soup.find_all(text=True) # returns a list of strings
        # strip out all the html tags and javascript
        body_text_only = [text for text in body_text_only if text.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']]
        # remove all the newlines and extra spaces
        body_text_only = [text.strip() for text in body_text_only]
        # remove all the empty strings
        body_text_only = [text for text in body_text_only if text]        
        # convert the list of strings into a single string
        body_text_only = " ".join(body_text_only)
        condensed_body_text = condense_for_search(query, body_text_only)
        text_results += condensed_body_text
        print("=!!")
        print(body_text_only)
        print("=>>")
        print(condensed_body_text)
        print("=EE")
    # condense all the results to be less than 3500 tokens
    if count_tokens(text_results) > 3500:
        text_results = condense_for_search(query, text_results)
        print("=!!!!!")
        print(condensed_body_text)
        print("=EEEEE")
    return text_results

def count_tokens(text):
    return len(text.split(" "))

def condense_for_search(query, text_results):   
    # chunk the text into 2000 token chunks
    # we can count how many tokens are in the text by splitting on spaces
    tokens = text_results.split(" ")
    # we want to split the text into chunks of 2000 tokens, so we'll iterate over these chunks
    # and add them to a list
    summary = ""
    count = 0
    template = """Write a summary of the following text as far as any information it reveals about this query: <<{query}>>, the rest can be discarded. If there is no relevant text, give no response. ==={text}==="""
    while count < len(tokens):
        chunk = " ".join(tokens[count:count+2000])
        llm_summary = get_llm_response(template.format(query=query, text=chunk))
        print("==?")
        print(llm_summary)
        print("==?")
        summary += llm_summary
        count += 2000
    return summary

def get_llm_response(user_message):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")    
    response = llm(messages=[fuser(user_message)])
    return response.content

def fuser(msg: str) -> HumanMessage:
    return HumanMessage(content=msg)

def fassistant(msg: str) -> AIMessage:
    return AIMessage(content=msg)
