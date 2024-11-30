import os
from openai import OpenAI
import requests

class Connection:
    def __init__(self):
        pass

    def checkInternet(url="https://www.google.com", timeout=60):
        try:
            response = requests.head(url, timeout=timeout)
            return response.status_code == 200 # Internet connection available
        except requests.ConnectionError: # "No internet connection"
            return False
        except requests.Timeout: # Server taking too long to respond
            return False
        except requests.RequestException: # Send a report
            return False
        
    def checkOpenai():
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
        except client.error.AuthenticationError:
            print("Authentication error: Cannot establish a connection with the current API key.")
            return False
        except client.error.APIConnectionError:
            print("API connection error: Unable to reach OpenAI servers.")
            return False
        except client.error.RateLimitError:
            print("Rate limit exceeded: Too many requests.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        except:
            print("OpenAI API connection failed.")
            return False
        
'''   
# Test internet
if checkInternet():
    print("Internet connected")
else:
    print("Internet not connected")

# Test OpenAI
checkOpenai()
'''
    