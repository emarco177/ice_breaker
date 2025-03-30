from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import openai
import os
from langchain_core.output_parsers import StrOutputParser
if __name__== '__main__':
    print("Welcome to the Ice Breaker program!")
    api_key = os.environ.get('OPENAI_API_KEY', 'No API key found')
    print(api_key)

    # Set the API endpoint for LM Studio (default port is 1234)
    API_BASE_URL = "http://localhost:1234/v1"

    
    # Initialize the OpenAI model
    summary_template = """

    You are a helpful assistant. Your task is to summarize the {information} in a friendly and engaging manner.
    The summary should be concise and capture the main points of the text. Please avoid using
    technical jargon and make it easy to understand for a general audience.
    """

    summary_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )

    #llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")
    llm = ChatOllama(model="mistral", temperature=0.5, max_tokens=1000)
    chain = summary_template | llm | StrOutputParser()
    res = chain.invoke(
        {"information": "The ice breaker program is designed to help people get to know each other better. It includes fun activities and games that encourage interaction and communication."}
    )

    print(res)