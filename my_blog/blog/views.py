import datetime
import random
import re
import time

from django.contrib.auth import logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from blog.models import UserModel, ArticleModel, LinkModel, CommetModel, LikeModel, NavModel

global icon

icon = 'blog/img/icon/icon.png'

def test(request):
    return render(request, 'blog/1.html')


def index(request):
    token = request.session.get('token')
    praises = ArticleModel.objects.filter(is_show=True,is_Delete=True,to_examine=True).order_by('-praise')[:5]
    articles = ArticleModel.objects.filter(is_show=True,is_Delete=True,to_examine=True).order_by('sort','-id')
    likes = ArticleModel.objects.filter(is_show=True, is_Delete=True, to_examine=True).order_by('-comment_num')[:8]
    links = LinkModel.objects.all().order_by('sort')

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
            'title': "明日之我-钟亮的个人博客",
            'articles': page_of_blogs,
            'praises': praises,
            'likes': likes,
            'links': links,
            'nav1': "current-menu-item",
            }
    return render(request, 'blog/index.html', data)


# def author_show(request,id):
#     global icon
#     token = request.session.get('token')
#     ticket = request.session.get('ticket')
#     if ticket:
#         user = UserModel.objects.get(ticket=ticket)
#         icon = user.icon
#     comments = CommetModel.objects.filter(classify=1,parent=None).order_by('-alterdate')
#     count = len(CommetModel.objects.filter(classify=1))
#     data = {'token': token,
#             'nav5': "current-menu-item",
#             'title': '关于自己-雪舞',
#             'icon': icon,
#             'article_id': 0,
#             'classify_id': 1,
#             'commets': comments,
#             'count': count,
#             }
#     return render(request,'blog/authorshow.html',data)



def article_list(request, id):
    if id == '0':
        serch = request.GET.get('s')
        articles=ArticleModel.objects.filter(title__contains=serch,is_Delete=True,is_show=True,to_examine=True).order_by('-browse_count')
        title = '搜索'+serch+'的结果-明日之我-钟亮的个人博客'
        str_serch = 's='+serch
    else:
        nav_flag = NavModel.objects.get(id=id)
        if nav_flag.Nav_root:
            articles = ArticleModel.objects.filter(nav2=nav_flag,is_Delete=True,is_show=True,to_examine=True).order_by('sort','-id')
        else:
            articles = ArticleModel.objects.filter(nav1=nav_flag,is_Delete=True,is_show=True,to_examine=True).order_by('sort','-id')
        title = nav_flag.nav_name+'-明日之我-钟亮的个人博客'
        str_serch = 0
    if id in ['3','14']:
        nav = 'nav4'
    elif id in ['1','4','5','6']:
        nav = 'nav2'
    elif id == '0':
        nav = 'nav1'
    else:
        nav = 'nav3'
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

    likes = ArticleModel.objects.filter(is_show=True, is_Delete=True, to_examine=True).order_by('-comment_num')[:8]
    links = LinkModel.objects.all().order_by('sort')
    data = {'token': token,
            'title': title,
            'articles': page_of_blogs,
            'likes': likes,
            'links': links,
            'icon': icon,
            nav: "current-menu-item",
            'str_serch':str_serch,
            }
    return render(request, 'blog/article_list.html', data)


def about(request):
    global icon
    token = request.session.get('token')
    ticket = request.session.get('ticket')
    if ticket:
        user = UserModel.objects.get(ticket=ticket)
        icon = user.icon
    comments = CommetModel.objects.filter(classify=1,parent=None).order_by('-alterdate')
    count = len(CommetModel.objects.filter(classify=1))
    data = {'token': token,
            'nav5': "current-menu-item",
            'title': '关于自己-明日之我-钟亮的个人博客',
            'icon': icon,
            'article_id': 0,
            'classify_id': 1,
            'commets': comments,
            'count': count,
            }
    return render(request, 'blog/about.html', data)


def main(request):  # 这是用户的主页的首页
    ticket = request.session.get('ticket')
    token = request.session.get('token')
    phone_result = request.session.get('phone_result')  # 修改电话号码时返回的错误信息
    if ticket:
        try:
            user = UserModel.objects.get(ticket=ticket)
            data = {'user': user,
                    'token': token,
                    'title': user.username+"-个人中心",
                    'nav1': "current-menu-item",
                    'icon': icon,
                    }
            if phone_result:
                data['phone_result'] = phone_result
                del request.session['phone_result']
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
        data = {'title': '登陆页面-明日之我-钟亮的个人博客',
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
    data = {'title': '注册页面-明日之我-钟亮的个人博客'}
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
        # try:
        user = UserModel.objects.get(ticket=ticket)
        main_articles = ArticleModel.objects.filter(author=user,is_Delete=True).order_by('-id')
        date = {'user': user,
                'token': token,
                'title': user.username+"-发布的文章",
                'nav1' : "current-menu-item",
                'icon': icon,
                'main_articles': main_articles,
                }
        return render(request, 'blog/main_article.html', date)
        # except Exception as e:
        #     logout(request)
        #     return redirect("/login")
    else:
        return redirect("/login")


def article(request,articleid):
    global icon
    ticket = request.session.get('ticket')
    if ticket:
        icon = UserModel.objects.get(ticket=ticket).icon
    try:
        article = ArticleModel.objects.get(id=articleid,is_show=True,is_Delete=True,to_examine=True)

        article.browse_count +=1
        article.save()
        title = article.title
        share = article.share
        token = request.session.get('token')
        if article.nav1.id == 3:
            nav = 'nav4'
        elif article.nav1.id in [1, 4, 5, 6]:
            nav = 'nav2'
        else:
            nav = 'nav3'
        commets = CommetModel.objects.filter(article=article,parent=None).order_by('-alterdate')
        count=len(CommetModel.objects.filter(article=article))
        article_ul = ArticleModel.objects.filter(is_show=True,is_Delete=True,to_examine=True).order_by('-browse_count')[:4]
        article_myself = ArticleModel.objects.filter(is_show=True,is_Delete=True,to_examine=True).order_by('-browse_count')[:6]
        article_next = ArticleModel.objects.filter(id__lt=articleid,is_show=True,is_Delete=True,to_examine=True).order_by('-id').first()
        article_prev = ArticleModel.objects.filter(id__gt=articleid,is_show=True,is_Delete=True,to_examine=True).first()
    except Exception as e:
        return redirect('/index')
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
    likes = ArticleModel.objects.filter(is_show=True, is_Delete=True, to_examine=True).order_by('-comment_num')[:8]
    links = LinkModel.objects.all().order_by('sort')
    data = {'title': title,
            'token': token,
            'article': article,
            'likes': likes,
            'links': links,
            'commets': page_of_blogs,
            nav: "current-menu-item",
            'count': count,
            'icon': icon,
            'article_id':article.id,
            'classify_id': 0,
            'share': share,
            'article_ul': article_ul,
            'article_myself': article_myself,
            'article_next': article_next,
            'article_prev': article_prev,
            'like_style': like_style,
            }
    return render(request, 'blog/article.html', data)


def message(request):
    token = request.session.get('token')
    comments = CommetModel.objects.filter(classify=2,parent=None).order_by('-alterdate')
    count = len(CommetModel.objects.filter(classify=2))
    data = {'token': token,
            'nav6': "current-menu-item",
            'title': '给我留言-明日之我-钟亮的个人博客',
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
            'title': '赞助作者-明日之我-钟亮的个人博客',
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
            'title': '技术交流-明日之我-钟亮的个人博客',
            'icon': icon,
            }
    return render(request,'blog/exchange.html',data)


def project(request):
    token = request.session.get('token')
    data = {'token': token,
            'nav9': "current-menu-item",
            'title': '项目合作-明日之我-钟亮的个人博客',
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
            'title': '友情连接-明日之我-钟亮的个人博客',
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


def like_show(request):
    ticket = request.session.get('ticket')
    data = {'status': "success",}
    if ticket:
        article_id = request.GET.get('article_id')
        article = ArticleModel.objects.get(id=article_id)
        user = UserModel.objects.get(ticket=ticket)
        try:
            is_like = LikeModel.objects.filter(user=user,article=article).first()
            if is_like:
                data['flag'] = 1
                return JsonResponse(data)
        except Exception as e:
            return JsonResponse(data)
    else:
        return JsonResponse(data)


def change_sex(request):
    if request.method == 'POST':
        sex = request.POST.get('sex')
        ticket = request.session.get('ticket')
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            user.sex = sex
            user.save()
            return redirect('/main')
        else:
            return redirect('/login')
    else:
        return redirect('/main')

def change_phone(request):
    if request.method == 'POST':
        phonenumber = request.POST.get('phonenumber')
        try:
            test = UserModel.objects.get(phonenumber=phonenumber)
            request.session['phone_result'] = "此号码已经被注册"
            return redirect('/main')
        except Exception as e:
            re_phone = re.search("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$",phonenumber)
            print(re_phone)
            if not re_phone:
                request.session['phone_result']="请输入正确的电话号码"
                return redirect('/main')
            else:
                ticket = request.session.get('ticket')
                if ticket:
                    user = UserModel.objects.get(ticket=ticket)
                    user.phonenumber = phonenumber
                    user.save()
                    return redirect('/main')
                else:
                    return redirect('/login')
    else:
        return redirect('/main')


def change_icon(request):
    ticket = request.session.get('ticket')
    if ticket:
        user = UserModel.objects.get(ticket=ticket)
        if request.method == 'POST':
            filename = request.FILES.get('icon')

            ext = str(filename).split('.')[-1]
            # 通过当前时间字符串作为文件名
            file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            # 拼接文件名和后缀
            file = 'media/blog/img/icon/' + file_name + '.' + ext
            user.icon = 'blog/img/icon/' + file_name + '.' + ext
            user.save()
            with open(file, 'wb+') as f:
                f.write(filename.read())
        return redirect('/main')
    else:
        return redirect('/login')


def change_url(request):
    if request.method == 'POST':
        my_url = request.POST.get('my_url')
        print(my_url)
        ticket = request.session.get('ticket')
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            user.my_url = my_url
            user.save()
            return redirect('/main')
        else:
            return redirect('/login')
    else:
        return redirect('/main')


def article_write(request,id):
    ticket = request.session.get("ticket")
    token = request.session.get('token')
    user = UserModel.objects.get(ticket=ticket)
    if ticket:
        data = {'token': token,
                'article_id': 0,
                'title': user.username+'-发布/修改文章',
                }
        # id = 0 表示发布文章
        if id == '0':
            pass
        # id !=0 表示修改文章
        else:
            article = ArticleModel.objects.filter(id=id,is_Delete=True,author=user).first()
            nav2_list = NavModel.objects.filter(Nav_root=article.nav1)
            data['article'] = article
            data['article_id'] = article.id
            data['nav2_list'] = nav2_list
        return render(request,'blog/articlewrite.html',data)
    else:
        return redirect('/login')


def do_article(request,id):
    ticket = request.session.get("ticket")
    if ticket:
        author = UserModel.objects.get(ticket=ticket)
        title = request.POST.get('title')
        first_class=request.POST.get('first')
        second_class = request.POST.get('second')
        is_show = request.POST.get('is_show')
        synopsis = request.POST.get('synopsis')
        content = request.POST.get('content')
        nav1 = NavModel.objects.get(nav_name=first_class,Nav_root=None)
        nav2 = NavModel.objects.get(nav_name=second_class,Nav_root=nav1)




        if id == '0':

            picture = request.FILES.get('icon')
            if picture == None:
                article_picture = 'blog/img/article/default.png'
            else:
                ext = str(picture).split('.')[-1]
                # 通过当前时间字符串作为文件名
                file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                # 拼接文件名和后缀
                file = 'media/blog/img/icon/' + file_name + '.' + ext
                article_picture = 'blog/img/icon/' + file_name + '.' + ext
                with open(file, 'wb+') as f:
                    f.write(picture.read())
            article = ArticleModel.createArticle(author,title,synopsis,content,nav1,nav2,is_show,article_picture)
            article.save()

        else:
            article = ArticleModel.objects.get(id=id,author=author,is_Delete=True)
            article.title = title
            article.nav1=nav1
            article.nav2=nav2
            article.is_show = is_show
            article.synopsis = synopsis
            article.content = content
            article.to_examine = False
            picture = request.FILES.get('icon')
            if picture == None:
                article.save()
            else:
                ext = str(picture).split('.')[-1]
                # 通过当前时间字符串作为文件名
                file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                # 拼接文件名和后缀
                file = 'media/blog/img/icon/' + file_name + '.' + ext
                article_picture = 'blog/img/icon/' + file_name + '.' + ext
                with open(file, 'wb+') as f:
                    f.write(picture.read())
                article.picture = 'blog/img/icon/' + file_name + '.' + ext
                article.save()
        return redirect('/main_article')
    else:
        return redirect('/login')


def article_delete(request,id):
    ticket = request.session.get('ticket')
    if ticket:
        try:
            user = UserModel.objects.get(ticket=ticket)
            article = ArticleModel.objects.get(id = id,is_Delete=True,author=user)
            article.is_Delete = False
            article.save()
            return redirect('blog:main_article')
        except Exception as e:
            return redirect('blog:main_article')
    else:
        logout(request)
        return redirect('/login')













