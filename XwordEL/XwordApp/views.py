from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from colorama import Fore
from lxml import etree

from .models import common_word, User_played_words_Thai_meaning, User_played_words_Eng_meaning
from .models import all_Eng_words, all_Thai_words
from .crossword_algo_mod import CrossWord, CrossWordFormatter, MaxLoopError
from .forms import CrosswordSessionForm, userUploadFile
from .getclue import get_word_info_longdodict, get_word_info_freedict
from .pdf_processer import get_words_from_file
from .words_process import get_base_words

from XwordEL.test_api import test_api

import gc
import sys
import ast
import random
import traceback
import itertools
import concurrent.futures


def random_list_with_blacklist(blacklist, items, length) -> list:
    print(f"blacklist : {len(blacklist)}\n=====\nitems : {len(items)}")
    filtered_items = list(itertools.filterfalse(
        lambda item: item in blacklist, items))
    if (len(filtered_items)==0) or (length < 0):
        return []
    
    if length > len(filtered_items):
        return filtered_items
    return random.sample(filtered_items, length)

def file_upload_error(msg) -> str:
    # set elem to red with etree
    error_msg_elem = etree.Element('p')
    error_msg_elem.set('style', 'color:red')
    error_msg_elem.text = msg
    return(etree.tostring(error_msg_elem, pretty_print=True).decode('utf-8'))

def file_upload(request):
    if request.method == "POST":
        form = userUploadFile(request.POST, request.FILES)
        if form.is_valid():
            print(
                f"request.FILES['file'] {request.FILES['file']}")
            file_type = request.FILES['file'].content_type
            print(f"file_type {file_type}")
            bool_ocr = bool(request.POST.get('file-ocr'))
            print(f"bool_ocr {bool_ocr}")
            uploaded_file = request.FILES['file']
            if (file_type == 'application/pdf') or (file_type == 'text/plain'):
                word_list = []
                err_msg = ""

                if (file_type == 'application/pdf'):
                    text,err_msg_ocr = get_words_from_file(uploaded_file, bool_ocr)
                    get_base_words_info = get_base_words(text)
                    err_msg += get_base_words_info['error_msg']
                    word_list = get_base_words_info['base_words']
                    print(
                        f"{Fore.CYAN}(wordlist size){sys.getsizeof(word_list)} bytes{Fore.RESET}", file=sys.stderr)
                elif (file_type == 'text/plain'):
                    word_list = []
                    text =  uploaded_file.read().decode('utf-8')
                    get_base_words_info = get_base_words(text)
                    err_msg += get_base_words_info['error_msg']
                    word_list = get_base_words_info['base_words']

                word_list_str = "\n".join(word_list)
                gc.collect()
                if len(err_msg_ocr)!=0:
                    if len(err_msg)!=0:
                        err_msg+=", "
                    err_msg+=f"{err_msg_ocr} => disbled OCR"
                msg= f"{file_upload_error(err_msg)}\nword_list: ({word_list_str})"
                
                # collect word_list_str in session
                request.session['new_word_from_file'] = True
                request.session['word_from_file'] = word_list_str
                request.session['word_from_file_count'] = len(word_list)
                return HttpResponse(msg)

            else:
                err_msg="File type not supported\nPlease upload a txt or pdf file"
                return HttpResponse(file_upload_error(err_msg))
            
        else:
            err_msg="Form rejected, invalid file (maybe by name of file)"
            return HttpResponse(file_upload_error(err_msg))


def get_word_clue_and_create(word, clues_type, word_meaning_objects):
    if not word_meaning_objects.filter(word=word).exists():
        print(f"word '{word}' not exist in db", file=sys.stderr)
        if clues_type == "thai":
            word_clue = get_word_info_longdodict(word)
        elif clues_type == "eng":
            word_clue = get_word_info_freedict(word)

        if word_clue == None:
            print(f"X X X word '{word}' clue is None")
            word_meaning_objects.create(word=word, meaning=[])
            return None

        word_meaning_objects.create(word=word, meaning=word_clue)
        return word
    else:
        # the mean the word is already in database
        # check if word have meaning or [] in database
        word_meaning_list_raw = list(word_meaning_objects.filter(
            word=word).values_list('meaning', flat=True))
        word_meaning_list = ast.literal_eval(word_meaning_list_raw[0])
        if len(word_meaning_list) == 0:
            print(
                f"{Fore.RED}word '{word}' have no clue in database []{Fore.RESET}", file=sys.stderr)
            return None
        else:
            return word


@login_required(login_url='/auth/login/')
def get_completed_percentage(request):
    if request.method == 'POST':
        session_data = request.session
        cluetype = session_data.get('clues_type')
        gamemode = session_data.get('gamemode')

        if gamemode == "normal":
            if cluetype == "thai":
                User_played_words_meaning_objects = User_played_words_Thai_meaning.objects
            elif cluetype == "eng":
                User_played_words_meaning_objects = User_played_words_Eng_meaning.objects
            else:
                # just in case, should not happen
                User_played_words_meaning_objects = User_played_words_Thai_meaning.objects

            User_played_words = User_played_words_meaning_objects.filter(
                userID=request.user.username).values_list('word', flat=True)
            user_played_words_list = ast.literal_eval(User_played_words[0])
            user_played_words_list_len = len(user_played_words_list)
            common_word_count = common_word.objects.count()
            
            print(f"{Fore.CYAN}user_played_words_meaning_count: {user_played_words_list_len}{Fore.RESET}",
                  )
            print(f"{Fore.CYAN}user_played_words_meaning: {user_played_words_list}{Fore.RESET}",)
            print(f"{Fore.CYAN}common_word_count: {common_word_count}{Fore.RESET}",
                  )

            percentage = (user_played_words_list_len /
                          common_word_count)*100
        elif gamemode == "filemode":
            word_count = session_data.get('word_from_file_count')
            print(f"{Fore.CYAN}word_count: {word_count}{Fore.RESET}",
                  file=sys.stderr)
            if session_data.get('wordlist') == None:
                percentage = 100
            else:
                print(
                    f"{Fore.CYAN}wordlist len : {len(session_data.get('wordlist'))}{Fore.RESET}", file=sys.stderr)
                percentage = ((
                    word_count-len(session_data.get('wordlist'))) / word_count)*100
        else:
            percentage = "error"
        if type(percentage) == float:
            percentage = round(percentage, 2)
        # use in case percentage > 100
        if percentage > 100:
            percentage = 100

        return HttpResponse(percentage)

def updated_user_played_words(request: object, User_played_words_meaning_objects: object, word_to_add: list) -> None:
    # Fetch the user's played words once
    user_played_words_obj = User_played_words_meaning_objects.filter(
        userID=request.user.username)

    if not user_played_words_obj.exists():
        raise ValueError("user_played_words_obj not exist")
    
    # transform string to list
    user_played_words_list = ast.literal_eval(user_played_words_obj.values_list('word', flat=True)[0]   )

    # remove duplicate word
    updated_user_played_words_list = list(
        set(user_played_words_list + word_to_add))

    # Update the user's played words
    user_played_words_obj.update(word=updated_user_played_words_list)

    '''
    User_played_words = User_played_words_meaning_objects.filter(
        userID=request.user.username).values_list('word', flat=True)

    # transform string to list
    user_played_words_list = ast.literal_eval(
        User_played_words[0])

    #remove duplicate word
    updated_user_played_words_list = list(
        set(user_played_words_list + corrected_words))
    User_played_words_meaning_objects.filter(
        userID=request.user.username).update(word=(updated_user_played_words_list))
    '''
        

@login_required(login_url='/auth/login/')
def genGame(request):
    if request.method == 'POST':
        '''
        try:
            del request.file['file']
        except:
            print(f"{Fore.RED}file not exist, failed to delete{Fore.RESET}", file=sys.stderr)                
        '''
        session_data = request.session
        # print(f"session_data key : {session_data.keys()}", file=sys.stderr)
        # -----------  gamemode , clues_type , difficulty ----------------
        gamemode = session_data.get('gamemode')
        clues_type = session_data.get('clues_type')
        difficulty = session_data.get('difficulty')
        clues_num_str = session_data.get('clues_num')
        hint_str = session_data.get('hint')
        # --------------------------------------------------------
        is_all_correct = False

        # check if previous game clue_type is same as current or not
        if 'clues_type' in session_data:
            if clues_type != session_data['clues_type']:
                del session_data['wordlist']
                del session_data['crossword_html']
                del session_data['correct_cell']
                del session_data['word_set']
                del session_data['corrected_words']

        # check if previous game gamemode is same as current or not
        if 'gamemode' in session_data:
            if gamemode != session_data['gamemode']:
                del session_data['wordlist']
                del session_data['crossword_html']
                del session_data['correct_cell']
                del session_data['word_set']
                del session_data['corrected_words']
                del session_data['word_from_file']
                del session_data['word_from_file_count']

        if clues_type == "thai":
            User_played_words_meaning_objects = User_played_words_Thai_meaning.objects
            word_meaning_objects = all_Thai_words.objects

        elif clues_type == "eng":
            User_played_words_meaning_objects = User_played_words_Eng_meaning.objects
            word_meaning_objects = all_Eng_words.objects

        # if empty, create empty word
        if not User_played_words_meaning_objects.filter(userID=request.user.username).exists():
            print(
                f"create empty word for {request.user.username}", file=sys.stderr)
            User_played_words_meaning_objects.create(
                userID=request.user.username, word=[])

        print(f"check wordlist in session_data", file=sys.stderr)
        if 'wordlist' not in session_data:
            print(f"======>  no wordlist, create wordlist", file=sys.stderr)
            if gamemode == "normal":
                # get all words from database
                all_words = common_word.objects.all().values_list('word', flat=True)

                # get user played words from database
                User_played_words = User_played_words_meaning_objects.filter(
                    userID=request.user.username).values_list('word', flat=True)

                # transform string to list
                user_played_words_list = ast.literal_eval(User_played_words[0])
                # debugging
                print(f"all_words: {len(all_words)}", file=sys.stderr)
                print(
                    f"user_played_words_list: {len(user_played_words_list)}", file=sys.stderr)

                # get wordlist by random words that is not in user played words
                wordlist = random_list_with_blacklist(
                    user_played_words_list, all_words, 15)

            elif gamemode == "filemode":
                # get wordlist from session
                if session_data.get('new_word_from_file'):
                    wordlist = session_data.get('word_from_file').splitlines()
                    #print(f"{Fore.YELLOW}wordlist: {wordlist}{Fore.RESET}")
                    session_data['new_word_from_file'] = False

                    # save wordlist to session
                    session_data['wordlist'] = wordlist

                else:
                    wordlist = session_data.get('wordlist')

        else:
            wordlist = session_data.get('wordlist')
        #print(f"{Fore.BLUE}wordlist: {wordlist}{Fore.RESET}")
        if wordlist == None:
            return redirect("empty_wordlist")
        if len(wordlist) < 3:

            if session_data.get('wordlist'):
                del session_data['wordlist']

            return redirect("empty_wordlist")

        print(f"check crossword_html in session_data", file=sys.stderr)
        print(f"session_data: {session_data.keys()}", file=sys.stderr)
        if 'crossword_html' not in session_data:
            print(f"======>  no crossword_html, create crossword_html",
                  file=sys.stderr)
            if gamemode == "normal":
                # filter wordlist to only word that have meaning in api
                new_wordlist = []
                '''
                for word in wordlist:
                    result = get_word_clue_and_create(
                        word, clues_type, word_meaning_objects)
                    if result is not None:
                        new_wordlist.append(result)
                '''
                # use concurrent to get word meaning
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    results = executor.map(get_word_clue_and_create,
                                           wordlist, itertools.repeat(clues_type), itertools.repeat(word_meaning_objects))
                    for result in results:
                        if result is not None:
                            new_wordlist.append(result)

                wordlist = new_wordlist

                table_Xword_html, missing, word_set, answer_dict = XwordEL_table_html(
                    wordlist, hint=int(hint_str))
            elif gamemode == "filemode":

                #print(f"{Fore.YELLOW}wordlist: {wordlist}{Fore.RESET}",file=sys.stderr)
                table_Xword_html, missing, word_set, answer_dict = XwordEL_table_html(
                    wordlist, hint=int(hint_str))

                wordlist_temp = [word_info[2] for word_info in word_set]

                new_wordlist_temp = []
                '''
                for word in wordlist_temp:
                    result = get_word_clue_and_create(
                        word, clues_type, word_meaning_objects)
                    print(f"result: {result}", file=sys.stderr)
                    if result is not None:
                        new_wordlist_temp.append(result)
                '''
                # use concurrent to get word meaning
                with concurrent.futures.ThreadPoolExecutor(max_workers=10)as executor:
                    results = executor.map(get_word_clue_and_create,
                                           wordlist_temp, itertools.repeat(clues_type), itertools.repeat(word_meaning_objects))

                    for result in results:
                        if result is not None:
                            new_wordlist_temp.append(result)

                # del no meaning word from wordlist
                for word in wordlist_temp:
                    if word not in new_wordlist_temp:
                        print(
                            f"{Fore.RED}del word: '{word}' from wordlist (no meaning){Fore.RESET}", file=sys.stderr)
                        wordlist.remove(word)

                wordlist_temp = new_wordlist_temp

                table_Xword_html, missing, word_set, answer_dict = XwordEL_table_html(
                    wordlist_temp, hint=int(hint_str))

            session_data['crossword_html'] = table_Xword_html
            session_data['word_set'] = word_set
            session_data['answer_dict'] = answer_dict
        else:
            table_Xword_html = session_data.get('crossword_html')
            word_set = session_data.get('word_set')
            answer_dict = session_data.get('answer_dict')

        form = CrosswordSessionForm(request.POST)

        if form.is_valid():
            print(f"form: {form.cleaned_data}", file=sys.stderr)
            if form.cleaned_data['reset_session']:
                del request.session['crossword_html']

                # return redirect('gameUI')
            if form.cleaned_data['reset_wordlist']:
                print(f"{Fore.RED}reset_wordlist{Fore.RESET}", file=sys.stderr)

                del request.session['wordlist']
                del request.session['crossword_html']
                # check the correct_cell
                if 'correct_cell' in request.session:
                    del request.session['correct_cell']
                # return redirect('gameUI')

            ################### check answer #########################
            if form.cleaned_data['check_crossword']:
                # filter request.POST if input in '' or ' '
                request.POST = {key: value for key, value in request.POST.items() if value not in [
                    '', ' ']}

                table_Xword_html, is_all_correct = check_answer(
                    request, table_Xword_html)
                corrected_words = session_data.get('corrected_words')
                print(
                    f"corrected_word: {corrected_words}")
                
                updated_user_played_words(request, User_played_words_meaning_objects, corrected_words)

                if is_all_correct:
                    print("------------------->  all correct", file=sys.stderr)
                    corrected_words = request.session.get('corrected_words')
                    # save wordlist to played word
                    if gamemode == "normal":
                        updated_user_played_words(request, User_played_words_meaning_objects, corrected_words)

                        if request.session.get("wordlist"):
                            del request.session['wordlist']

                        del request.session['crossword_html']
                        del request.session['correct_cell']
                        del request.session['word_set']
                        del request.session['corrected_words']

                    elif gamemode == "filemode":
                        wordlist = session_data.get('wordlist')
                        corrected_words = session_data.get('corrected_words')
                        print(len(wordlist), len(corrected_words))
                        print(f"{Fore.YELLOW}wordlist: {wordlist}{Fore.RESET}",
                              file=sys.stderr)
                        print(f"{Fore.YELLOW}corrected_words: {corrected_words}{Fore.RESET}",
                              file=sys.stderr)
                        print(f"{Fore.CYAN}wordlist: {len(wordlist)}{Fore.RESET}",
                              file=sys.stderr)
                        wordlist = list(set(wordlist) - set(corrected_words))
                        print(
                            f"{Fore.CYAN}wordlist: {len(wordlist)}{Fore.RESET}", file=sys.stderr)
                        session_data['wordlist'] = wordlist
                        """
                        fix me
                        """
                        del request.session['crossword_html']
                        del request.session['correct_cell']
                        del request.session['word_set']
                        del request.session['corrected_words']
                        pass

    if 'corrected_words' in request.session:
        corrected_words = request.session['corrected_words']
    else:
        corrected_words = []
    print(f"word_set: {word_set}", file=sys.stderr)
    # word_set: [[1, 1, 'animal'], [2, 1, 'three'], [3, 1, 'usual'], [4, 1, 'divide'], [5, 1, 'probable'], [6, 1, 'speed'], [7, 1, 'shore'], [8, 1, 'corner'], [1, 0, 'liquid'], [2, 0, 'experience'], [3, 0, 'sudden'], [4, 0, 'boat'], [5, 0, 'want']]
    for word_info in word_set:
        print(f"({word_info[0]},{word_info[2]})", end=" ", file=sys.stderr)

    table_clues_html = gen_table_clues_html(
        word_set, corrected_words, clues_type, max_meaning=int(clues_num_str), is_all_correct=is_all_correct,)

    # <div class="game_button">
    game_button = etree.Element('div')
    # <input type="submit" name="reset_session" value="reset Session (for debug)" class="button" />
    game_button.set('class', 'game_button')
    game_button_input = etree.SubElement(game_button, 'input')
    game_button_input.set('type', 'submit')
    game_button_input.set('name', 'check_crossword')
    game_button_input.set('value', 'Check')
    game_button_input.set('id', 'crossword_answer')
    game_button_input.set('class', 'button')
    # <input type="reset" name="reset_crossword" value="reset" class="button" />
    game_button_input = etree.SubElement(game_button, 'input')
    game_button_input.set('type', 'reset')
    game_button_input.set('name', 'reset_crossword')
    game_button_input.set('value', 'Reset')
    game_button_input.set('class', 'button')
    # <input type="button" name="show_hint" value="hint" class="button" />
    '''
    game_button_input = etree.SubElement(game_button, 'input')
    game_button_input.set('type', 'button')
    game_button_input.set('name', 'show_hint')
    game_button_input.set('value', 'hint')
    game_button_input.set('class', 'button')
    

    # <input type="submit" name="reset_session" value="reset Session (for debug)" class="button" />
    game_button_input = etree.SubElement(game_button, 'input')
    game_button_input.set('type', 'submit')
    game_button_input.set('name', 'reset_session')
    game_button_input.set('value', 'reset Session (for debug)')
    game_button_input.set('class', 'button')
    
    # <input type="submit" name="reset_wordlist" value="reset Word (for debug)" class="button" />
    game_button_input = etree.SubElement(game_button, 'input')
    game_button_input.set('type', 'submit')
    game_button_input.set('name', 'reset_wordlist')
    game_button_input.set('value', 'reset Word (for debug)')
    game_button_input.set('class', 'button')
    '''
    game_button = etree.tostring(
        game_button, pretty_print=True).decode('utf-8')

    return HttpResponse(table_Xword_html + table_clues_html+game_button)


@login_required(login_url='/auth/login/')
def xwordelGame(request):

    if request.method == 'POST':
        print(
            f"{Fore.LIGHTGREEN_EX}request.POST: {request.POST}{Fore.RESET}", file=sys.stderr)
        print(f"request.session: {request.session}", file=sys.stderr)

        keys_to_delete = []
        # check hint type in session
        if 'hint' in request.session:
            if request.session['hint'] != request.POST.get('hint'):
                print(f"{Fore.RED}hint change{Fore.RESET}", file=sys.stderr)
                print(
                    f"{Fore.YELLOW}request session all key: {request.session.keys()}{Fore.RESET}", file=sys.stderr)
                keys_to_delete = ['wordlist', 'crossword_html',
                                  'correct_cell', 'word_set', 'corrected_words', 'answer_dict']

        # if frist time
        if request.POST.get('reset_crossword') == "true":
            print(f"{Fore.RED}reset_crossword{Fore.RESET}", file=sys.stderr)
            keys_to_delete = ['wordlist', 'crossword_html',
                              'correct_cell', 'word_set', 'corrected_words']

        for key in keys_to_delete:
            if request.session.get(key) != None:
                del request.session[key]

        # ----------- set gamemode , clues_type , difficulty ----------------
        if "gamemode" in request.POST:
            gamemode = request.POST['gamemode']
            request.session['gamemode'] = gamemode
        else:
            gamemode = request.session['gamemode']

        if "clues_type" in request.POST:
            clues_type = request.POST['clues_type']
            request.session['clues_type'] = clues_type
        else:
            clues_type = request.session['clues_type']

        if "difficulty" in request.POST:
            difficulty = request.POST['difficulty']
            request.session['difficulty'] = difficulty
        else:
            difficulty = request.session['difficulty']

        if "clues_num" in request.POST:
            clues_num = request.POST['clues_num']
            request.session['clues_num'] = clues_num
        else:
            clues_num = request.session['clues_num']

        if "hint" in request.POST:
            hint = request.POST['hint']
            request.session['hint'] = hint
        else:
            hint = request.session['hint']

        print(
            f"gamemode: {gamemode}, clues_type: {clues_type}, difficulty: {difficulty}, clues_num: {clues_num}, hint: {hint}", file=sys.stderr)
        # --------------------------------------------------------

    print(f'Request path: {request.path}', file=sys.stderr)
    print(f'Request method: {request.method}', file=sys.stderr)

    return render(request, 'XwordGame.html')


def gen_table_clues_html(word_set, corrected_words, clues_type, max_meaning=3, is_all_correct=False):

    table_clues_wrapper = etree.Element('div')
    table_clues_wrapper.set('class', 'cluestable_wrapper')
    table_clues = etree.SubElement(table_clues_wrapper, 'table')

    table_clues.set('class', 'cluestable')
    # sort word_set by arrow and number
    word_set.sort(key=lambda x: x[0])
    word_set.sort(key=lambda x: x[1], reverse=True)

    # get word meaning from database
    if clues_type == "thai":
        word_meaning_objects = all_Thai_words.objects
    elif clues_type == "eng":
        word_meaning_objects = all_Eng_words.objects
    else:
        # just in case, should not happen
        word_meaning_objects = all_Thai_words.objects

    for num, vertical, word in word_set:
        is_word_correct = False
        if is_all_correct:
            continue

        # check if word is already in corrected_words
        if word in corrected_words:
            is_word_correct = True
        '''
        # ====================================================================
        
        # if word not already in database add it
        if not word_meaning_objects.filter(word=word).exists():
            print(f"word '{word}' not exist in db", file=sys.stderr)
            if clues_type == "thai":
                word_meaning_objects.create(
                    word=word, meaning=get_word_info_longdodict(word))
            elif clues_type == "eng":
                word_meaning_objects.create(
                    word=word, meaning=get_word_info_freedict(word))
        
        # ====================================================================
        '''
        # get word meaning list from database
        word_meaning_list_raw = list(word_meaning_objects.filter(
            word=word).values_list('meaning', flat=True))
        # print(f"word_meaning_list_raw: {word_meaning_list_raw}", file=sys.stderr)
        if len(word_meaning_list_raw) == 0:
            continue
        word_meaning_list = ast.literal_eval(word_meaning_list_raw[0])
        # print(f"word_meaning_list: {word_meaning_list}", file=sys.stderr)

        # set table elem
        row_element = etree.SubElement(table_clues, 'tr')
        if is_word_correct:
            # row_element.set('style', 'background-color: #00FF00;')
            row_element.set('class', 'cluestable_row_correct')
        row_element.set('id', f"clue_{'H' if vertical else 'V'}{num}")
        number_cell_element = etree.SubElement(row_element, 'td')
        vertical_cell_element = etree.SubElement(row_element, 'td')
        clue_cell_element = etree.SubElement(row_element, 'td')

        number_cell_element.set('class', 'cluestable_number')
        vertical_cell_element.set('class', 'cluestable_vertical')
        clue_cell_element.set('class', 'cluestable_clue')

        number_cell_element_p = etree.SubElement(number_cell_element, 'p')
        vertical_cell_element_p = etree.SubElement(vertical_cell_element, 'p')

        vertical_cell_element_p.text = 'across' if vertical else 'down'
        # number_cell_element.text = str(num)

        number_cell_element_p.text = f"{num}."
        # debugging
        # number_cell_element_p.text = word

        # generate clue
        for num, meaning in enumerate(word_meaning_list):
            clue_text_element = etree.SubElement(clue_cell_element, 'p')
            clue_text_element.text = meaning
            # print(f"max_meaning: {max_meaning}", file=sys.stderr)
            if num+1 >= max_meaning:
                break
            # etree.SubElement(clue_cell_element, 'br')

    table_clues_html = etree.tostring(
        table_clues_wrapper, pretty_print=True).decode('utf-8')
    return table_clues_html


@login_required(login_url='/auth/login/')
def options(request):

    return render(request, 'gameoptions.html', {'form': userUploadFile()})


####################################################
def check_answer(request, table_Xword_html):
    if request.method == 'POST':

        answer_dict = request.session['answer_dict']
        table_Xword = etree.fromstring(table_Xword_html)

        correct_cell = []
        # filter the request.POST to only input_* and value is not empty
        filtered_request = {key: value for key, value in request.POST.items(
        ) if key.startswith('input_') and value not in ['', ' ']}
        # add correct_cell to filtered_request
        if 'correct_cell' in request.session:
            for target_id, letter in request.session['correct_cell']:
                filtered_request[f"input_{target_id}"] = letter

        # del request.session starts with 'input_'
        for key in request.session.keys():
            if key.startswith('input_'):
                del request.session[key]

        corrected_words = []

        # check word is correct
        diffcultly = request.session['difficulty']
        print(f"diffcultly: {diffcultly}", file=sys.stderr)
        if diffcultly == 'word':
            # check if the all letter in the word is correct
            for word in answer_dict.keys():
                temp_correct_cell = []
                for target_id, letter in answer_dict[word]:
                    # print(f"target_id: {target_id}, letter: {letter}", file=sys.stderr)
                    # print(f"filtered_request: {filtered_request}", file=sys.stderr)
                    if f"input_{target_id}" not in filtered_request:
                        break
                    if filtered_request[f"input_{target_id}"].lower() == letter.lower():
                        temp_correct_cell.append((target_id, letter))
                    else:
                        temp_correct_cell = []
                        break
                    if len(temp_correct_cell) == len(answer_dict[word]):
                        correct_cell += temp_correct_cell
                        corrected_words.append(word)

        elif diffcultly == 'letter':
            # check if the letter in correct
            for word in answer_dict.keys():
                temp_correct_cell = []
                for target_id, letter in answer_dict[word]:
                    if f"input_{target_id}" in filtered_request:
                        if filtered_request[f"input_{target_id}"].lower() == letter.lower():
                            correct_cell.append((target_id, letter))
                            temp_correct_cell.append((target_id, letter))
                # if all letter in the word is correct add word to corrected_words
                if len(temp_correct_cell) == len(answer_dict[word]):
                    corrected_words.append(word)


        print(
            f"{Fore.GREEN}corrected_words: {corrected_words}{Fore.RESET}", file=sys.stderr)
        request.session['corrected_words'] = corrected_words

        for target_id, letter in correct_cell:
            request.session['correct_cell'] = correct_cell

        # change the color of correct cell
        for target_id, letter in correct_cell:
            xpath = f".//*[@id='{target_id}']/div"
            letter_cell = table_Xword.find(xpath)

            # remove input tag
            letter_cell_input = letter_cell.find('input')
            if letter_cell_input == None:
                # print(f"at xpath: {xpath} letter_cell_input is None", file=sys.stderr)
                continue
            # get antribute word-data-number
            word_data_number = letter_cell_input.attrib['word-data-number']
            letter_cell.remove(letter_cell.find('input'))

            letter_cell_div = etree.SubElement(letter_cell, 'div')
            letter_cell_div.set('class', 'Xwordtable_cell_content_correct')
            letter_cell_div.set('id', f"input_{target_id}")
            letter_cell_div.set('word-data-number', word_data_number)
            letter_cell_div.text = letter

        # print(f"answer_dict : {answer_dict}", file=sys.stderr)
        answer_dict_letter_list = []
        for value_list in answer_dict.values():
            answer_dict_letter_list.extend(value_list)

        # print(len(correct_cell), len(answer_dict_letter_list), file=sys.stderr)

        return etree.tostring(table_Xword, pretty_print=True).decode('utf-8'), len(correct_cell) == len(answer_dict_letter_list)
    # else:return redirect('xwordelGame')


def XwordEL_table_html(wordlist, hint=None):
    answer_dict = {}
    # Define the number of rows and columns
    '''
    num_rows = 15
    num_cols = num_rows
    '''
    num_cols = 12
    num_rows = 12
    max_try = 10
    for i in range(max_try):
        try:
            # =================

            solution = None
            # default max-loop 5000

            cwd = CrossWord(cols=num_cols, rows=num_rows, empty=' ',
                            maxloops=10000, wordlist=wordlist)

            score = cwd.compute_crossword(
                best_of=10, force_solved=False)

            tmplist = [w.word.lower() for w in cwd.placed_words]
            missing = [w.word for w in cwd.wordlist if w.word.lower()
                       not in tmplist]
            print(f"missing: {missing}", file=sys.stderr)

            formatter = CrossWordFormatter(cwd, ppb=32, solution=solution)
            # print(formatter.get_crossword_ascii_grid(False, True), file=sys.stderr)
            # =================
            output_info_dict = formatter.get_crossword_ascii_grid(
                False, True)
            # anti repeat number
            # print(output_info_dict, file=sys.stderr)
            dict_count = {}
            for word in output_info_dict.keys():
                number = output_info_dict[word]['number']
                vertical = output_info_dict[word]['vertical']
                if f"{number}_{vertical}" in dict_count:
                    dict_count[f"{number}_{vertical}"] += 1
                else:
                    dict_count[f"{number}_{vertical}"] = 1
            # check if there is repeat number ,continue
            # print(f"dict_count ----> {dict_count}", file=sys.stderr)

            for key, value in dict_count.items():
                if value > 1:
                    raise Exception("repeat number")
            # debugging
            # make it randomly repeat

            break
        except MaxLoopError as e:
            print(f"except: {traceback.format_exc()}", file=sys.stderr)
            print(f"MaxLoopError: {i}", file=sys.stderr)
            print(f"MaxLoopError word : {e.word}", file=sys.stderr)
            print(
                f"MaxLoopError count : {e.count}", file=sys.stderr)
            # remove the word that cause MaxLoopError
            print(f"{Fore.RED}remove word: {e.word}{Fore.RESET}")
            wordlist.remove(e.word)
            pass
        except:

            print(f"try {i} times", file=sys.stderr)
            print(f"except: {traceback.format_exc()}", file=sys.stderr)
            pass

    Xwordtable_wrapper = etree.Element('div')
    Xwordtable_wrapper.set('class', 'Xwordtable_wrapper')
    table = etree.SubElement(Xwordtable_wrapper, 'table')
    table.set('class', 'Xwordtable')

    for row in range(num_rows):
        row_element = etree.SubElement(table, 'tr')

        for col in range(num_cols):
            col_element = etree.SubElement(row_element, 'td')
            col_element_div = etree.SubElement(col_element, 'div')
            col_element.set('id', f'X_{col + 1}_Y_{row + 1}')

    # Xword_letter_cell.attrib["style"] = "color: red; font-size: 16px;"
    print(f"output_info_dict: {output_info_dict}", file=sys.stderr)
    for word, word_property in output_info_dict.items():
        letter_col = word_property['start_X']
        letter_row = word_property['start_Y']
        letter_vertical = word_property['vertical']

        letter_indx = 0

        answer_dict[word] = []

        for letter in word:

            target_id = f'X_{letter_col}_Y_{letter_row}'
            answer_dict[word].append((target_id, letter))

            xpath = f".//*[@id='{target_id}']/div"
            # print(xpath, file=sys.stderr)

            letter_cell = table.find(xpath)

            if letter_indx == 0:
                letter_cell_sup = etree.SubElement(letter_cell, 'div')
                letter_cell.remove(letter_cell_sup)
                letter_cell.insert(0, letter_cell_sup)
                letter_cell_sup.set('class', 'Xwordtable_cell_sup')
                letter_cell_sup.text = str(word_property['number'])

                # print(f"number: {word_property['number']}", file=sys.stderr)

            letter_cell.set('class', 'Xwordtable_cell_content')

            # set word-data-number to input
            word_data_number = f"{'H' if letter_vertical else 'V'}{word_property['number']}"
            # if letter_cell is already filled, skip
            if 'input' not in [child.tag for child in letter_cell]:

                letter_cell_input = etree.SubElement(letter_cell, 'input')

                letter_cell_input.set('type', 'text')
                letter_cell_input.set('id', f"input_{target_id}")
                letter_cell_input.set('name', f"input_{target_id}")
                letter_cell_input.set('maxlength', '1')
                letter_cell_input.set('size', '1')

                # hint 1 == not show
                # hint 2 == show vowel
                # hint 3 == random show
                if hint == 1:
                    pass
                elif hint == 2:
                    if letter in ['a', 'e', 'i', 'o', 'u']:
                        letter_cell_input.set('placeholder', letter)
                elif hint == 3:
                    if (random.randint(0, 10) > 5):
                        letter_cell_input.set('placeholder', letter)

                # debugging
                #letter_cell_input.set('value', letter)

                letter_cell_input.set('class', 'Xwordtable_cell_content_input')

                letter_cell_input.set('word-data-number', word_data_number)

            else:
                letter_cell_input = letter_cell.find('input')

                letter_cell_input.set(
                    'word-data-number', f"{letter_cell_input.attrib['word-data-number']},{word_data_number}")

                # check vertical

                ######################################################
                # if (random.randint(0, 10) != 0):
                #    letter_cell_input.set('value', letter)
                ######################################################

                # add word-data-number

            ######################################################
            letter_col += int(letter_vertical)
            letter_row += int(not letter_vertical)
            letter_indx += 1

    # print(output_info_dict, file=sys.stderr)

    # print(table_Xword, file=sys.stderr)
    # print(f"min_x: {min_x}, min_y: {min_y}, max_x: {max_x}, max_y: {max_y}", file=sys.stderr)

    # remove unused rows and columns
    '''
    for row in table:
        row_index = row.find('td').attrib['id'].split('_')[3]
        if int(row_index) < min_y or int(row_index) > max_y:
            table.remove(row)
            continue

        for col in row:
            col_index = col.attrib['id'].split('_')[1]
            if int(col_index) < min_x or int(col_index) > max_x:
                row.remove(col)
    '''
    table_Xword = etree.tostring(
        Xwordtable_wrapper, pretty_print=True).decode('utf-8')

    # word set (number,word)
    word_set = [(word_property['number'], word_property['vertical'], word)
                for word, word_property in output_info_dict.items()]
    # print(answer_dict, file=sys.stderr)
    return table_Xword, missing, word_set, answer_dict
