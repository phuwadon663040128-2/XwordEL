
from colorama import Fore
from django.conf import settings
import requests

def get_base_words(text: str):
    #send the text to api
    error_msg_to_user=""
    try:
        api_url = settings.SPACY_API_URL
        api_spliter_url = f"{api_url}/get_base_words"
        response = requests.post(api_spliter_url, json={"text": text, "max_word_length": 8, "min_word_length": 3})
        responsejson = response.json()
        base_words = responsejson["words"]
        print(f"{Fore.GREEN}Base words: {base_words}{Fore.RESET}")
        status = "success"
    except Exception as e:
        print(f"{Fore.RED}Error in get_base_words: {e}{Fore.RESET}")
        status = "error"
        error_msg_to_user = f"Error in get_base_words: connection error"
        base_words = []
    
    info = {
        "status": status,
        "base_words": base_words,
        "error_msg": error_msg_to_user
    }
    return info