from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.google_stalker_agent import lookup as google_stalker_agent
from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_ice_breaker_chain,
)
from third_parties.linkedin import scrape_linkedin_profile

from third_parties.twitter import scrape_user_tweets
from output_parsers import (
    summary_parser,
    topics_of_interest_parser,
    ice_breaker_parser,
    Summary,
    IceBreaker,
    TopicOfInterest,
)


def ice_break_with(name: str) -> Tuple[Summary, IceBreaker, TopicOfInterest, str]:
    print()
    web_data = google_stalker_agent(name=name)
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    combined_data = str(linkedin_data) + "\n" + web_data

    summary_chain = get_summary_chain()
    summary_and_facts = summary_chain.run(
        information=combined_data
    )
    summary_and_facts = summary_parser.parse(summary_and_facts)

    interests_chain = get_interests_chain()
    interests = interests_chain.run(information=combined_data)
    interests = topics_of_interest_parser.parse(interests)

    ice_breaker_chain = get_ice_breaker_chain()
    ice_breakers = ice_breaker_chain.run(
        information=combined_data
    )
    ice_breakers = ice_breaker_parser.parse(ice_breakers)

    return (
        summary_and_facts,
        interests,
        ice_breakers,
        linkedin_data.get("profile_pic_url"),
    )


if __name__ == "__main__":
    pass
