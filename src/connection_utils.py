import requests

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
    
# Test
if checkInternet():
    print("Internet connected")
else:
    print("Internet not connected")
    