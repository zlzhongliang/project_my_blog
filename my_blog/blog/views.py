import random
import time

from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Create your views here.
from blog.models import UserModel, ArticleModel, LinkModel

global list1,list2,likes,likes
list1 = ["生活笔记", "技术杂谈", "福利专区"]
list2 = [['个人随笔','个人日记','个人展示'],['C/C++','java','PHP','HTML','Python','JS','Other'],['福利专区']]
likes = ArticleModel.objects.all().order_by('-share')[:8]
links = LinkModel.objects.all().order_by('sort')

def test(request):
    return render(request, 'blog/1.html')


def index(request):
    token = request.session.get('token')
    articles = ArticleModel.objects.all().order_by('sort')
    praises = ArticleModel.objects.all().order_by('-praise')[:5]
    data = {'token': token,
            'title': "雪舞-钟亮的个人博客",
            'articles': articles,
            'list2': list2,
            'praises': praises,
            'likes': likes,
            'links': links,
            'nav1': "current-menu-item",
            }
    return render(request, 'blog/index.html', data)


def article_list(request, first_classify, second_classify, third_classify):

    if third_classify == '0':  # 这是作者文章列表的标记
        if second_classify == '0':
            articles = ArticleModel.objects.filter(first_classify=first_classify).order_by('sort')
        else:
            articles = ArticleModel.objects.filter(first_classify=first_classify, second_classify=second_classify).order_by('sort')
    else:
        user = UserModel.objects.get(id = int(third_classify))
        articles = ArticleModel.objects.filter(author=user).order_by('sort')
    if first_classify == '0':
        nav = 'nav2'
    elif first_classify == '1':
        nav = 'nav3'
    else:
        nav = 'nav4'
    token = request.session.get('token')
    data = {'token': token,
            'articles': articles,
            'likes': likes,
            'links': links,
            nav: "current-menu-item",
            }
    return render(request, 'blog/article_list.html', data)


def about(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav5': "current-menu-item",
            'title': '关于自己-雪舞',
            }
    return render(request, 'blog/about.html', data)


def main(request):
    ticket = request.session.get('ticket')
    token = request.session.get('token')
    if ticket:
        try:
            user = UserModel.objects.get(ticket=ticket)
            data = {'user': user,
                    'token': token,
                    'title': "个人中心-"+ user.username,
                    'nav1': "current-menu-item",
                    }
            if request.method == 'POST':
                username = request.POST.get('username')
                try:
                    test = UserModel.objects.get(username=username)
                    if test != user:
                        data['username_result'] = "用户名已存在"
                        return render(request, 'blog/main.html', data)
                    else:
                        return render(request, 'blog/main.html', data)
                except Exception as e:
                    if 1 < len(username) < 7:
                        user.username = username
                        user.save()
                        request.session['token'] = username
                        data['token'] = username
                        return render(request, 'blog/main.html', data)
                    else:
                        data['username_result'] = "请输入2-6位的用户名"
                        return render(request, 'blog/main.html', data)
            else:
                return render(request, 'blog/main.html', data)
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
                    'nav1' : "current-menu-item",
                    }
            return render(request, 'blog/main_article.html', date)
        except Exception as e:
            quit()
            return redirect("/login")
    else:
        return redirect("/login")


def article(request,articleid):
    article = ArticleModel.objects.get(id=articleid)
    s1 = list1[int(article.first_classify)]
    s2 = list2[int(article.first_classify)][int(article.second_classify)-1]
    token = request.session.get('token')
    data = {'title': "文章的标题",
            'token': token,
            'article': article,
            's1': s1,
            's2': s2,
            }
    return render(request, 'blog/article.html', data)


def message(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav6': "current-menu-item",
            'title': '给我留言-雪舞',
            }
    return render(request,'blog/message.html',data)

def donate(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav7': "current-menu-item",
            'title': '赞助作者-雪舞',
            }
    return render(request,'blog/donate.html',data)

def exchange(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav8': "current-menu-item",
            'title': '技术交流-雪舞',
            }
    return render(request,'blog/exchange.html',data)


def project(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav9': "current-menu-item",
            'title': '项目合作-雪舞',
            }
    return render(request,'blog/project.html',data)