import random
import time

from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Create your views here.
from blog.models import UserModel

global date_base
date_base = {}


def index(request):
    token = request.session.get('token')
    date = {'token': token}
    return render(request, 'blog/index.html', date)


def life(requset):
    return render(requset, 'blog/life.html')


def skill(requset):
    return render(requset, 'blog/skill.html')


def resources(request):
    return render(request, 'blog/resources.html')


def about(request):
    return render(request, 'blog/about.html')


def main(request):
    ticket = request.session.get('ticket')
    token = request.session.get('token')

    if ticket:
        try:
            user = UserModel.objects.get(ticket=ticket)
            date = {'user': user,
                    'token': token
                    }
            print(user.sex)
            print(type(user))
            return render(request, 'blog/main.html', date)
        except Exception as e:
            quit()
            return redirect("/login")
    else:
        return redirect("/login")



def login(request):
    ticket = request.session.get('ticket')
    if ticket:
        return redirect('/main')
    else:
        return render(request, 'blog/login.html')


def do_login(request):
    if request.method == 'POST':
        email = request.POST.get('user_email')
        try:
            user = UserModel.objects.get(email = email)
            password = request.POST.get('user_password')
            if password == user.password:
                ticket = time.time() + random.randrange(1, 100000)
                user.ticket = ticket
                user.save()
                request.session['token'] = user.username
                request.session['ticket'] = ticket
                return redirect('/main')
            else:
                return redirect('/login')
        except Exception as e:
            return redirect('/login')
    else:
        return redirect('/login')


def register(request):
    return render(request, 'blog/register.html')


def do_register(request):
    if request.method == 'POST':
        email = request.POST.get('user_email')
        password = request.POST.get('user_password')
        username = email
        try:
            user = UserModel.createUser(password, email, username)
            user.save()
            return redirect('/login')
        except Exception as e:
            return redirect('/register')
    else:
        return redirect('/register')


def quit(request):
    logout(request)
    return redirect('/index')
