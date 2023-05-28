from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

information = """
As executive vice president of the Microsoft Cloud and Enterprise group, Scott Guthrie is responsible for the company’s cloud infrastructure, server, database, management and development tools businesses. His engineering team builds Microsoft Azure, Windows Server, SQL Server, Active Directory, System Center, Visual Studio and .NET.

Prior to leading the Cloud and Enterprise group, Guthrie helped lead Microsoft Azure, Microsoft’s public cloud platform. Since joining the company in 1997, he has made critical contributions to many of Microsoft’s key cloud, server and development technologies and was one of the original founders of the .NET project. Guthrie graduated with a bachelor’s degree in computer science from Duke University. He lives in Seattle with his wife and two children.
"""
if __name__ == "__main__":
    print("Hello LangChain!")

    summary_template = """
        give the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    print(chain.run(information=information))
