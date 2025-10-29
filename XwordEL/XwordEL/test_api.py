from colorama import Fore

import requests

def test_api(URL: str) -> bool:
    print(f"Try to connect to the API: {URL}")
    try:
        #set the timeout to 10 seconds
        response = requests.get(URL, timeout=3)
        if response.status_code == 200:
            print(f"{URL} | {Fore.GREEN}API is available.{Fore.RESET}")
            return True
        else:
            print(f"{URL} | {Fore.RED}API is not available.{Fore.RESET}")
            return False
    except Exception as e:
        print(f"{URL} |{ Fore.RED}API is not available.{Fore.RESET}")
        return False
    

if __name__=="__main__":
    from django.conf import settings
    #check if API is available
    Api_url = settings.SPACY_API_URL
    test_api(Api_url)
    Api_url = settings.OCR_API_URL
    test_api(Api_url)
    print("Test API done.")