import random
import time

from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Create your views here.
from blog.models import UserModel


def index(request):
    token = request.session.get('token')
    data = {'token': token}
    data['title'] = "雪舞-钟亮的个人博客"
    print(token)
    return render(request, 'blog/index.html', data)


def life(request):
    token = request.session.get('token')
    data = {'token': token}
    data['title'] = "生活笔记-雪舞"
    return render(request, 'blog/life.html', data)


def skill(request):
    token = request.session.get('token')
    data = {'token': token}
    data['title'] = "技术杂谈-雪舞"

    return render(request, 'blog/skill.html', data)


def resources(request):
    token = request.session.get('token')
    data = {'token': token}
    data['title'] = "福利专区-雪舞"
    return render(request, 'blog/resources.html', data)


def about(request):
    token = request.session.get('token')
    data = {'token': token}
    data['title'] = "关于自己-雪舞"
    return render(request, 'blog/about.html', data)


def main(request):
    ticket = request.session.get('ticket')
    token = request.session.get('token')

    if ticket:
        try:
            user = UserModel.objects.get(ticket=ticket)
            date = {'user': user,
                    'token': token,
                    'title': "个人中心-"+ user.username,
                    }
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
        data = {'title': '登陆页面-雪舞'}
        return render(request, 'blog/login.html', data)


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
    data = {'title': '注册页面-雪舞'}
    return render(request, 'blog/register.html', data)


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

def main_article(request):
    ticket = request.session.get('ticket')
    token = request.session.get('token')

    if ticket:
        try:
            user = UserModel.objects.get(ticket=ticket)
            date = {'user': user,
                    'token': token,
                    'title': "我发布的文章-"+user.username,
                    }
            return render(request, 'blog/main_article.html', date)
        except Exception as e:
            quit()
            return redirect("/login")
    else:
        return redirect("/login")
