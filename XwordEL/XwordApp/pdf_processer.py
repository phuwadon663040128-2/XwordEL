from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings

from colorama import Fore
import concurrent.futures
import traceback
import requests
import fitz

class OcrApiError(Exception):
    pass

class SpacyApiError(Exception):
    pass

def process_page(page):
    text = page.get_text()
    results = []
    print(f"read Page {page.number+1}")

    for result in results:
        text += result
    
    return text


def get_words_from_pdf(uploaded_file, ocr:bool=False):
    error_msg_to_user = ""
    file_data = uploaded_file.read()
    pdf = fitz.open("pdf", file_data)

    texts = []

    if ocr:
        #send the file to the OCR API
        ocr_url =f"{settings.OCR_API_URL}/ocr"
        try:
            '''
            curl -X 'POST' \
            'http://0.0.0.0:8882/ocr' \
            -H 'accept: application/json' \
            -H 'Content-Type: multipart/form-data' \
            -F 'file=@gui4(2p).pdf;type=application/pdf'
            '''
            print(f"file name: {uploaded_file.name}")
            print(f"file type: {uploaded_file.content_type}")
            print(f"file size: {uploaded_file.size}")
            print(f"file type: {type(uploaded_file.file)}")
            file = uploaded_file.file
            if hasattr(file, 'getvalue'):
                file_to_send = file.getvalue()
            else:
                file.seek(0)
                file_to_send = file.read()

            files = {
                'file': (uploaded_file.name, file_to_send, uploaded_file.content_type)
            }
            headers = {
                'accept': 'application/json'
            }
            r = requests.post(ocr_url, files=files, headers=headers, timeout=10)
            print(f"{Fore.YELLOW} OCR Response: {r.status_code}{Fore.RESET}")
            #print response full details
            print(f"OCR Response: {r.json()}")
            if r.status_code == 400:
                print(f"{Fore.RED}Error in OCR: {r.json()}{Fore.RESET}")
                error_msg = r.json()["detail"]
                #raise ocrapi error
                raise OcrApiError(error_msg)
         
            elif r.status_code == 200:
                ocr_words = r.json()["words"]
                texts.extend(ocr_words)
            else:
                print(f"{Fore.RED}Unknown response from OCR API: {r.status_code}{Fore.RESET}")
                raise Exception(f"Unknown response from OCR API: {r.json()}")
        
        except OcrApiError as e:
            print(f"{Fore.RED}Error in OCR: {e}{Fore.RESET}")
            error_msg_to_user = f"Error in OCR: {e}"

        except requests.exceptions.ConnectionError as e:
            print(f"{Fore.RED}Error in OCR: {e}{Fore.RESET}")
            error_msg_to_user = f"Error in OCR: connection error"   

        except Exception as e:
            print(f"{Fore.RED}Error : {e}{Fore.RESET}")
            print(f"{Fore.RED}Error : {traceback.format_exc()}{Fore.RESET}")
            error_msg_to_user = f"Unknown error: {e}"
        

    print(f"Texts: {texts}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_page = {executor.submit(
            process_page, page): page for page in pdf}
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f'Page {page.number+1} generated an exception: {exc}')
            else:
                texts.append(data)

    text = " ".join(texts)
    
    return text, error_msg_to_user

def get_words_from_file(uploaded_file, ocr=False):
    print(f"uploaded_file : {uploaded_file}")
    if uploaded_file.name.endswith(".pdf"):
        return get_words_from_pdf(uploaded_file, ocr)
    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read(), ""
   
    return None, "File type not supported"