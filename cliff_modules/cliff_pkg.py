##################################
# cliff_pkg
# originally for udemy online class ice_breaker
# 000, 20230725, cliff: original coding
##################################


##################################
# cliff_get_env
# 000, 20230725, cliff: original coding
##################################
# gets environment variables from .env and reads them in to use manually
##################################
def cliff_get_env(key):
    """
    import os
    retval=os.environ.get(key)
    print("API_KEY=", retval)
    """
    retval = None
    with open(".env") as env:
        file_lines = env.readlines()
        for line in file_lines:
            linekey, lineval = line.split("=")
            if linekey == key:
                retval = lineval.strip()
            #endif
        #endfor
    #endwith

    return retval
#enddef

##################################
# cliff_json_dump
# 000, 20230725, cliff: original coding
##################################
# dumps json in my preferred format
##################################
import json
def cliff_json_dump(the_data, sort=False):
    try:
        my_json = json.dumps(the_data, indent=4, separators=(',', ': '), sort_keys=sort)
    except:
        my_json = the_data
    #endtry
        
    return my_json
#enddef

##################################
# cliff_url_to_filepath
# 000, 20230725, cliff: original coding
##################################
# converts url's to savable filepaths
##################################
import pkg_resources
import urllib.parse
def cliff_url_to_filepath(url: str):
    filename = urllib.parse.quote(url, '')
    filepath = pkg_resources.resource_filename(__name__, filename)
    return filepath
#enddef

##################################
# cliff_file_fresh_secs
# 000, 20230728, cliff: original coding
##################################
# check to see if a file is still fresh based on being within seconds of mod time
##################################
import os
import datetime
def cliff_file_fresh_secs(filepath: str, oldage_in_secs: int) -> bool:
    file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    now = datetime.datetime.today()
    age = now - file_mod_time
    if age.seconds <= oldage_in_secs:
        return True
    else:
        return False
    #endif
#enddef

##################################
# cliff_file_fresh_days
# 000, 20230728, cliff: original coding
##################################
# check to see if a file is still fresh based on being within days of mod time
##################################
def cliff_file_fresh_days(filepath: str, oldage_in_days: int) -> bool:
    return cliff_file_fresh_secs(filepath, oldage_in_days*24*60*60)
#enddef


##################################
# cliff_get_cached_linkedin
# 000, 20230725, cliff: original coding
##################################
# if we have a cached linkedin from proxycurl, then we use it, otherwise we go get a freshone
##################################
# TODO: make them date sensitive
##################################
import requests
import pickle
from cliff_modules import cliff_pkg
import os.path

CONTEXT_LIMIT=4097
CACHE_AGE_IN_DAYS=7
def cliff_get_cached_linkedin(linkedin_profile_url: str, context_limit=CONTEXT_LIMIT):
    NUBELCO_API_KEY=cliff_get_env('NUBELCO_API_KEY')
    ##last_linkedin_profile_url = 'https://www.linkedin.com/in/cliffrayman/'
    linkedin_cached_filepath = cliff_url_to_filepath(linkedin_profile_url)  + '.json'
    
    if os.path.isfile(linkedin_cached_filepath) and cliff_file_fresh_days(linkedin_cached_filepath, 7):
        result = pickle.load( open( linkedin_cached_filepath, "rb" ) )
        print("===== cached result =====")
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        api_key = NUBELCO_API_KEY
        header_dic = {'Authorization': 'Bearer ' + api_key}
        params = {
            'url': linkedin_profile_url,
            'fallback_to_cache': 'on-error',
            'use_cache': 'if-present',
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=header_dic)
        if response.status_code != 200:
            result = response.status_code
            print("===== error result =====", result)
        else:
            data_work = response.json()
            data_work = {
                k: v
                for k, v in data_work.items()
                if v not in ([], "", "", None)
                    and k not in ["people_also_viewed", "certifications"]
                
            }

            if data_work.get('groups'):
                for group_dict in data_work('groups'):
                    group_dict.pop('profile_pic_url')
                #endfor
            #endif

            result = data_work
            pickle.dump( {'result':result},  open(linkedin_cached_filepath, "wb" ) )
            print("===== fresh result =====")
    #endif
    return result
#endif