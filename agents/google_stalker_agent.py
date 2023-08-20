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
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken
from langchain.text_splitter import TokenTextSplitter

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

def text_only(html_content:str, remove_whitespace:bool=False)->str:
    soup = BeautifulSoup(html_content, 'html.parser')
    body_text_only = soup.find_all(text=True) # returns a list of strings
    # strip out all the html tags and javascript
    body_text_only = [text for text in body_text_only if text.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']]
    if remove_whitespace:
        # remove all the newlines and extra spaces
        body_text_only = [text.strip() for text in body_text_only]
        # remove all the empty strings
        body_text_only = [text for text in body_text_only if text]        
    # convert the list of strings into a single string
    body_text_only = " ".join(body_text_only)
    return body_text_only

def google_scraper(query, pages=2):
    search = SerpAPIWrapper()
    results_page = search.results(query)
    text_results = ""
    for result in results_page["organic_results"]:
        response = requests.get(result["link"])
        html_content = response.text
        text_results += text_only(html_content)
    return condense_for_query(query, text_results)

def count_tokens(text, use_tiktoken=False):
    def tiktoken_len(text):
        tokenizer = tiktoken.get_encoding('cl100k_base')     # use cl100k_base tokenizer for gpt-3.5-turbo and gpt-4
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)
    if use_tiktoken:
        return tiktoken_len(text)
    return len(text.split(" "))


# create the length function used by the RecursiveCharacterTextSplitter

def condense_for_query(query, text_results, summary_guide="Write a summary of information from the following text as far as it gives us insights to the person mentioned in this query:"):   
    text_splitter = TokenTextSplitter(
        chunk_size = 3500,
        chunk_overlap  = 20,
    )
    documents = text_splitter.split_text(text_results)
    summary = ""
    template = """{summary_guide} <<{query}>>. Text:\n{text}"""
    sanitized_template = """Convert the following text into a bulletpoint list of information that can be determined about the person<<{query}>>. Some sentences in this text report that information could not be found, you should continue reading and summarizing until the end of the text. Text:{text}"""
    for doc in documents:
        llm_summary = get_llm_response(template.format(query=query, text=doc, summary_guide=summary_guide))
        print("==?")
        print(llm_summary)
        print("==?")        
        summary += llm_summary
    # claims by the LLM that the text does not provide information about the person mentioned in the query confuse the LLM, so we remove them first
    llm_summary_sanitized = get_llm_response(sanitized_template.format(query=query, text=summary))
    print("==!")
    print(llm_summary_sanitized)
    print("==!")
    return llm_summary_sanitized

def get_llm_response(user_message):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")    
    response = llm(messages=[fuser(user_message)])
    return response.content

def fuser(msg: str) -> HumanMessage:
    return HumanMessage(content=msg)

def fassistant(msg: str) -> AIMessage:
    return AIMessage(content=msg)
