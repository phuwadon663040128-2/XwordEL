import requests as rq
import concurrent.futures
import threading
from lxml import etree
import json
import time
import re
import time


def get_word_info_longdodict(word: str, mode=2) -> list:
    """
    this only work with the word from NECTEC Lexitron Dictionary EN-TH
    mode = 1 : search with -word-
    mode = 2 : search with word-
    """
    if mode == 1:
        r = rq.get(f"https://dict.longdo.com/mobile.php?search=-{word}-")
    elif mode == 2:
        r = rq.get(f"https://dict.longdo.com/mobile.php?search={word}-")

    r.encoding = 'utf-8'
    r_content = r.content.decode('utf-8')

    html_content = etree.HTML(r_content)

    result_table_html_list = html_content.xpath('//*[@class="result-table"]')

    word_info = []
    for result_table_html in result_table_html_list:

        dict_name = result_table_html.getprevious().text
        if dict_name != "NECTEC Lexitron Dictionary EN-TH":
            continue

        for row in result_table_html.xpath('.//tr'):
            cells = row.xpath('.//td')

            if word != cells[0].xpath('.//text()')[0]:
                continue
            word_from_dict = cells[0].xpath('.//text()')
            word_str_from_dict = ''.join(word_from_dict) 
            print(f"word : {word} | word_from_dict : {(''.join(word_from_dict))}")
            word_des = "".join(cells[1].xpath('.//text()'))
            

            word_des = re.sub(r'See also.*', '', word_des)

            word_des = re.sub(r'Syn.*', '', word_des)
            word_des = word_des.rstrip(" ")
            word_des = word_des.rstrip(",")

            if mode == 1 and word_str_from_dict != word:
                continue
            elif mode == 2 :
                #replace word in word_from_dict with *
                tmp = re.sub(rf'{word}', '*'*len(word), word_str_from_dict) 
                word_des = tmp + " : " + word_des
                #print(f"word_des : {word_des}")

            word_info.append(word_des)

    if len(word_info) == 0:
        if mode == 1:
            return get_word_info_longdodict(word, mode=2)
        else:
            return None

    return word_info


def get_word_info_freedict(word: str) -> list:

    r = rq.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if r.status_code != 200:
        if r.status_code == 404:
            return None
        time.sleep(1)
        return get_word_info_freedict(word)

    r.encoding = 'utf-8'
    r_content = r.content.decode('utf-8')
    r_content = json.loads(r_content)
    word_meanings = r_content[0]['meanings']
    word_info = []
    for meaning in word_meanings:
        for definition in meaning['definitions']:
            word_info_str = f"({meaning['partOfSpeech']}) {definition['definition']}"
            word_info.append(word_info_str)
    # print(word_info)
    return word_info


# get word from file "20k.txt"
if __name__ == "__main__":
    thread_local = threading.local()

    words = ["abandon", "was", "abandoasdasdasnment", "abashed", "abate", "abatement",
             "abbreviate", "abbreviation", "abdicate", "abdomen", "abdominal", "abduct", "abduction",]
    '''
    start = time.perf_counter()
    for word in words:
        print(f"----------------> {word}")
        word_info = get_word_info_freedict(word)
        print(repr(word_info))
    end = time.perf_counter()
    total1 = end-start
    '''
    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(get_word_info_longdodict, words)
        for word, result in zip(words, results):
            print(f"{word} : {result}")

    end = time.perf_counter()
    total2 = end-start

        