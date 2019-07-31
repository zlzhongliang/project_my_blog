import random
import time

from django.contrib.auth import logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from blog.models import UserModel, ArticleModel, LinkModel, CommetModel, LikeModel

global list1,list2,likes,likes,icon
list1 = ["生活笔记", "技术杂谈", "福利专区"]
list2 = [['个人随笔','个人日记','个人展示'],['C/C++','java','PHP','HTML','Python','JS','Other'],['福利专区']]
likes = ArticleModel.objects.all().order_by('-share')[:8]
links = LinkModel.objects.all().order_by('sort')
icon = 'blog/img/user/icon.png'

def test(request):
    return render(request, 'blog/1.html')


def index(request):
    token = request.session.get('token')
    praises = ArticleModel.objects.all().order_by('-praise')[:5]
    articles = ArticleModel.objects.all().order_by('sort')

    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(articles, 5)

    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        page_of_blogs = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        page_of_blogs = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        page_of_blogs = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    data = {'token': token,
            'title': "雪舞-钟亮的个人博客",
            'articles': page_of_blogs,
            'list2': list2,
            'praises': praises,
            'likes': likes,
            'links': links,
            'nav1': "current-menu-item",
            }
    return render(request, 'blog/index.html', data)


def article_list(request, first_classify, second_classify, third_classify):

    if third_classify == '0':  # 这是当前点击的作者的文章列表的标记
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
    title = ArticleModel.first_class[int(first_classify)][1]
    token = request.session.get('token')
    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(articles, 5)

    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        page_of_blogs = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        page_of_blogs = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        page_of_blogs = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    data = {'token': token,
            'title': title,
            'articles': page_of_blogs,
            'likes': likes,
            'links': links,
            'icon': icon,
            nav: "current-menu-item",
            }
    return render(request, 'blog/article_list.html', data)


def about(request):
    token = request.session.get('token')
    comments = CommetModel.objects.filter(classify=1,parent=None).order_by('-alterdate')
    print(comments)
    count = len(CommetModel.objects.filter(classify=1))
    data = {'token': token,
            'nav5': "current-menu-item",
            'title': '关于自己-雪舞',
            'icon': icon,
            'article_id': 0,
            'classify_id': 1,
            'commets': comments,
            'count': count,
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
                    'icon': icon,
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
            logout(request)
            return redirect("/login")
    else:
        return redirect("/login")



def login(request):
    commet_next = request.session.get('commet_next')
    if commet_next:
        next = commet_next
    else:
        next = request.GET.get('next','')
    request.session['next'] = next
    ticket = request.session.get('ticket')
    if ticket:
        return redirect('/main')
    else:
        data = {'title': '登陆页面-雪舞',
                'next': next
                }
        return render(request, 'blog/login.html', data)


def do_login(request):
    global icon
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
                icon = user.icon
                if next:
                    return HttpResponseRedirect(request.session['next'])
                else:
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
                    'icon': icon,
                    }
            return render(request, 'blog/main_article.html', date)
        except Exception as e:
            quit()
            return redirect("/login")
    else:
        return redirect("/login")


def article(request,articleid):
    article = ArticleModel.objects.get(id=articleid)
    article.browse_count +=1
    article.save()
    title = article.title
    share = article.share
    s1 = list1[int(article.first_classify)]
    s2 = list2[int(article.first_classify)][int(article.second_classify)-1]
    token = request.session.get('token')
    nav = 'nav'+str(article.first_classify+2)
    commets = CommetModel.objects.filter(article=article,parent=None).order_by('-alterdate')
    count=len(CommetModel.objects.filter(article=article))
    article_ul = ArticleModel.objects.all().order_by('-browse_count')[:4]
    article_myself = ArticleModel.objects.filter(first_classify=0).order_by('-browse_count')[:6]
    article_fuli = ArticleModel.objects.filter(first_classify=2).order_by('-browse_count')[:2]

    # 生成paginator对象,定义每页显示10条记录
    paginator = Paginator(commets, 5)

    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        page_of_blogs = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        page_of_blogs = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        page_of_blogs = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    ticket = request.session.get("ticket")
    like_style = 'iconfont icon-icon-test'
    if ticket:
        try:
            user = UserModel.objects.get(ticket = ticket)
            like_article = LikeModel.objects.filter(user=user,article=article).first()
            if like_article:
                like_style = 'iconfont icon-aixin'
        except Exception as e:
            pass



    data = {'title': title,
            'token': token,
            'article': article,
            'likes': likes,
            'links': links,
            's1': s1,
            's2': s2,
            'commets': page_of_blogs,
            nav: "current-menu-item",
            'count': count,
            'icon': icon,
            'article_id':article.id,
            'classify_id': 0,
            'share': share,
            'article_ul': article_ul,
            'article_myself': article_myself,
            'article_fuli': article_fuli,
            'like_style': like_style,
            }
    return render(request, 'blog/article.html', data)


def message(request):
    token = request.session.get('token')
    comments = CommetModel.objects.filter(classify=2,parent=None).order_by('-alterdate')
    count = len(CommetModel.objects.filter(classify=2))
    data = {'token': token,
            'nav6': "current-menu-item",
            'title': '给我留言-雪舞',
            'icon': icon,
            'article_id': 0,
            'classify_id': 2,
            'commets': comments,
            'count': count,
            }
    return render(request,'blog/message.html',data)

def donate(request):
    comments = CommetModel.objects.filter(classify=3,parent=None).order_by('-alterdate')
    count = len(CommetModel.objects.filter(classify=3))
    token = request.session.get('token')
    data = {'token': token,
            'nav7': "current-menu-item",
            'title': '赞助作者-雪舞',
            'icon': icon,
            'article_id': 0,
            'classify_id': 3,
            'commets': comments,
            'count': count,
            }
    return render(request,'blog/donate.html',data)

def exchange(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav8': "current-menu-item",
            'title': '技术交流-雪舞',
            'icon': icon,
            }
    return render(request,'blog/exchange.html',data)


def project(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav9': "current-menu-item",
            'title': '项目合作-雪舞',
            'icon': icon,
            }
    return render(request,'blog/project.html',data)



def do_commet(request, article_id, classify_id,root_id):  # 在评论只有两层的情况下

    next = request.GET.get('next')
    next = next+'#comments'
    ticket = request.session.get("ticket")
    if ticket:
        try:
            user = UserModel.objects.get(ticket=ticket)
            if request.method == 'POST':
                up_commet = request.POST.get('up_comment')


                if up_commet:
                    commet = CommetModel()
                    commet.commet = up_commet
                    commet.author = user
                    commet.classify = classify_id
                    if classify_id == '0':  #表明是文章的评论
                        article = ArticleModel.objects.get(id=article_id)
                        article.comment_num += 1
                        article.save()
                        commet.article = article
                    if root_id == '0':
                        commet.save()
                    else:
                        root = CommetModel.objects.get(id=int(root_id))
                        commet.root = root
                        commet.parent = root
                        parent = root
                        commet.reply_to = root.author
                        commet.save()
                        root.sort+=1
                        root.save()

                    return HttpResponseRedirect(next)


                else:
                    print('提交内容为空')
                    return HttpResponseRedirect(next)

        except Exception as e:
            return redirect('/login')
    else:
        request.session['commet_next'] = next
        return redirect('/login')


def link(request):
    token = request.session.get('token')
    comments = CommetModel.objects.filter(classify=4,parent=None).order_by('-alterdate')
    count = len(CommetModel.objects.filter(classify=4))
    data = {'token': token,
            'nav1': "current-menu-item",
            'title': '友情连接-雪舞',
            'icon': icon,
            'article_id': 0,
            'classify_id': 4,
            'commets': comments,
            'count': count,
            }
    return render(request,'blog/link.html',data)



def like_add(request):
    ticket = request.session.get('ticket')
    article_id = request.GET.get('id')
    flag = request.GET.get('flag')
    article = ArticleModel.objects.get(id=article_id)
    if ticket:
        user = UserModel.objects.get(ticket=ticket)
        like_flag = LikeModel.objects.filter(user=user, article=article).first()
        if like_flag:
            like_flag.delete()
            article.praise -= 1
        else:
            like_article = LikeModel.createLike(user=user, article=article)
            like_article.save()
            article.praise += 1
        article.save()
        data = {
            'status': "success",
            'praise': article.praise,
        }
        return JsonResponse(data)


    else:
        if flag == '0':
            article.praise += 1
        else:
            article.praise -= 1
        article.save()
        data = {
            'status': "success",
            'praise': article.praise,
        }
        return JsonResponse(data)



#
# def like_add(request):
#     article_id = request.GET.get('id')
#     flag = request.GET.get('flag')
#     article = ArticleModel.objects.get(id=article_id)
#     user = 0
#     try:
#         user = UserModel.objects.get(ticket=request.session.get('ticket'))
#         like_flag = LikeModel.objects.get(user=user, article=article)
#     except Exception as e:
#         pass
#     if flag == '0':
#         if user:
#             like_article = LikeModel.createLike(user=user, article=article)
#             like_article.save()
#         else:
#             article.praise += 1
#     else:
#         if user:
#             like_article = LikeModel.objects.get(user=user, article=article)
#             like_article.delete()
#         else:
#             pass
#         article.praise -= 1
#     article.save()
#     data={
#         'status':"success",
#         'praise':article.praise,
#     }
#     return JsonResponse(data)



def like_show(request):
    ticket = request.session.get('ticket')
    data = {}
    if ticket:
        article_id = request.GET.get('article_id')
        article = ArticleModel.objects.get(id=article_id)
        try:

            user = UserModel.objects.get(ticket=ticket)
        except Exception as e:
            pass


        try:
            is_like = LikeModel.objects.filter(user=user,article=article).first()
            print(is_like)
            if is_like:
                data = {
                    'status': "success",
                    'flag': 1,
                }
                return JsonResponse(data)
        except Exception as e:
            return JsonResponse(data)
    else:
        return JsonResponse(data)
