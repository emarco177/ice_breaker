from cliff_modules import cliff_pkg

CONTEXT_LIMIT=4097
def scrape_linkedin_profile(linkedin_profile_url:str, context_limit=CONTEXT_LIMIT):
    """ scrape information from linkedin profiles.
    Manually scrape the information from the Linkedin Profile"""
    result = cliff_pkg.cliff_get_cached_linkedin(linkedin_profile_url, context_limit)
    return result
#enddef


