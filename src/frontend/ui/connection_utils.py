import os
import openai
from openai import OpenAI
client = OpenAI()
import requests

class Connection:
    def __init__(self):
        pass

    def checkInternet(self, url="https://www.google.com", timeout=60):
        try:
            response = requests.head(url, timeout=timeout)
           # print("Internet connection successful.")
            return response.status_code == 200 # Internet connection available
        except requests.ConnectionError: # "No internet connection"
           # print("No internet connection.")
            return False
        except requests.Timeout: # Server taking too long to respond
           # print("Connection timed out.")
            return False
        except requests.RequestException: # Send a report
           # print("An error occurred while checking the internet connection.")
            return False
    
    # OpenAI authentication testing and error handling code snippet from API documentation
    # https://platform.openai.com/docs/guides/error-codes
    def checkOpenai(self):
        client = OpenAI(
            api_key = os.environ.get("OPENAI_API_KEY")
        )
        try:
            completion = client.chat.completions.create(
                model = "gpt-4o",
                messages = [
                    {
                        "role": "user",
                        "content": "Confirm that you can respond to this message."
                    }
                ]
            )
            print(completion)
            print("OpenAI API connection successful.")
            return True
        except openai.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            return False
        except openai.APIConnectionError as e:
            #Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
            return False
        except openai.RateLimitError as e:
            #Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")
            return False