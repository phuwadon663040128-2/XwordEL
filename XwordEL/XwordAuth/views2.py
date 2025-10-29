from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.contrib import messages

from XwordApp.models import  User_played_words_Thai_meaning, User_played_words_Eng_meaning,common_word
from .forms import UserPlayedWordsDeleteForm

import datetime
import ast
import csv

class UserPlayedWords():
    def __init__(self, request) :
        self.User_played_words_Thai_meaning_objects = User_played_words_Thai_meaning.objects
        self.User_played_words_Eng_meaning_objects = User_played_words_Eng_meaning.objects
        self.common_word_objects = common_word.objects
        self.all_word = self.common_word_objects.all().count()

        self.User_played_words_Thai_meaning_objects_text = self.User_played_words_Thai_meaning_objects.filter(userID=request.user.username).values_list("word", flat=True)
        self.User_played_words_Eng_meaning_objects_text = self.User_played_words_Eng_meaning_objects.filter(userID=request.user.username).values_list("word", flat=True)

    def get_played_words_list_count(self,_QuerySet:QuerySet):
        if len(_QuerySet) == 0:
            return 0
        text = _QuerySet[0]
        user_played_words_list = ast.literal_eval(text)
        played_words_count = len(user_played_words_list)
        return played_words_count
    
    def get_played_word_count(self,lang:str):    
        if lang == "thai":
            User_played_words = self.User_played_words_Thai_meaning_objects_text
        elif lang == "eng":
            User_played_words = self.User_played_words_Eng_meaning_objects_text
        return self.get_played_words_list_count(User_played_words)
    
    def get_played_words_percent(self,lang:str):
        if lang == "thai":
            User_played_words = self.User_played_words_Thai_meaning_objects_text
        elif lang == "eng":
            User_played_words = self.User_played_words_Eng_meaning_objects_text
        played_words = self.get_played_words_list_count(User_played_words) 
        percentange = (played_words/self.all_word)*100
        return f"{percentange:.2f}"
    

@login_required(login_url='/auth/login/')
def XwordEL_profile(request):
    if request.method == "POST":
        form = UserPlayedWordsDeleteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            is_delete = form.cleaned_data["thaiWordDelete"] or form.cleaned_data["engWordDelete"]
            if form.cleaned_data["thaiWordDelete"]:
                User_played_words_Thai_meaning.objects.filter(userID=request.user.username).update(word="[]")
            if form.cleaned_data["engWordDelete"]:
                User_played_words_Eng_meaning.objects.filter(userID=request.user.username).update(word="[]")
            if is_delete:
                messages.success(request, "Words deleted successfully")
            else:
                messages.warning(request, "No words selected for deletion")
            return redirect("profile")
        else:
            print(f"Form is invalid: {form.errors}")
            messages.warning(request, "Form is invalid")

        return redirect("profile")
        
    elif request.method == "GET":
        user_played_words = UserPlayedWords(request)
  
        context = {
            "thai_played_words_count": user_played_words.get_played_word_count("thai"),
            "eng_played_words_count": user_played_words.get_played_word_count("eng"),
            "thai_played_words_percent": user_played_words.get_played_words_percent("thai"),
            "eng_played_words_percent": user_played_words.get_played_words_percent("eng"),
        }
        return render(request, "profile.html",context=context)


@login_required(login_url='/auth/login/')
class XwordEL_download_played_words():
    def __init__(self,request):
        self.User_played_words_Thai_meaning_objects = User_played_words_Thai_meaning.objects
        self.User_played_words_Eng_meaning_objects = User_played_words_Eng_meaning.objects
        self.request = request

    def download_played_words(self,lang:str):
        if lang == "thai":
            User_played_words = self.User_played_words_Thai_meaning_objects.filter(userID=self.request.user.username).values_list("word", flat=True)
        elif lang == "eng":
            User_played_words = self.User_played_words_Eng_meaning_objects.filter(userID=self.request.user.username).values_list("word", flat=True)
        if len(User_played_words) == 0:
            return []
        played_words_text = User_played_words[0]
        played_words = ast.literal_eval(played_words_text)
        return played_words

def played_words_download(request,lang:str):
    #get date and time
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%H-%M-%S")
    #download played words
    played_words = XwordEL_download_played_words(request).download_played_words(lang)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{lang}_played_words_{date}_{time}.csv"'
    writer = csv.writer(response)
    #sort played words
    played_words.sort()
    #write played words to csv
    #writer.writerow([f"{lang} played words"])
    for word in played_words:
        writer.writerow([word])
    return response


@login_required(login_url='/auth/login/')
def XwordEL_download_thaiplayedwords(request):
    return played_words_download(request,"thai")

@login_required(login_url='/auth/login/')
def XwordEL_download_engplayedwords(request):
    return played_words_download(request,"eng")
    