import os
from openai import OpenAI
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
        # write out error messages to JSON file later
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