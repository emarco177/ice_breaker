from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI


from output_parsers import Summary, IceBreaker, TopicOfInterest

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_creative = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")


def get_summary_chain() -> RunnableSequence:
    summary_template = """
         given the information about a person from linkedin {information}, and twitter posts {twitter_posts} I want you to create:
         1. a short summary
         2. two interesting facts about them
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
    )

    return summary_prompt_template | llm.with_structured_output(Summary)


def get_interests_chain() -> RunnableSequence:
    interesting_facts_template = """
         given the information about a person from linkedin {information}, and twitter posts {twitter_posts} I want you to create:
         3 topics that might interest them
     """

    interesting_facts_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=interesting_facts_template,
    )

    return interesting_facts_prompt_template | llm.with_structured_output(TopicOfInterest)


def get_ice_breaker_chain() -> RunnableSequence:
    ice_breaker_template = """
         given the information about a person from linkedin {information}, and twitter posts {twitter_posts} I want you to create:
         2 creative Ice breakers with them that are derived from their activity on Linkedin and twitter, preferably on latest tweets
     """

    ice_breaker_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=ice_breaker_template,
    )

    return ice_breaker_prompt_template | llm.with_structured_output(IceBreaker)
