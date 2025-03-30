
import os
if __name__== '__main__':
    print("Welcome to the Ice Breaker program!")
    api_key = os.environ.get('OPENAI_API_KEY', 'No API key found')
    print(api_key)