from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import UserCreateForm
import sys


def home(request):
    return render(request, "home.html")


def XwordEL_login(request):
    print(User.objects.all(), file=sys.stderr)
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(request, username=username, password=pass1)
        try:
            #set session expiry to 0 to make sure the user is logged out after closing the browser
            request.session.set_expiry(0)
        except:
            pass
        print(user, file=sys.stderr)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning (request, "authentication failed")
            return redirect('login')

    return render(request, "login.html")


def XwordEL_logout(request):
    logout(request)

    return redirect('home')


def XwordEL_signup(request):
    if request.method == "GET":
        return render(
            request, "signup.html",
            {"form": UserCreateForm})
    
    elif request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Your Account has been created succesfully!! Don't forget your username and password.")
            return redirect(reverse("login"))
        else:
            messages.warning(request, "Form is invalid please make sure your info is matching the requirements")
            
        return redirect('signup')
