import requests

api_key = '1l3LeQW_nAFJFjYsCsK96A'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'url': 'https://www.linkedin.com/in/adam-punnoose/'
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)
print(response.json())