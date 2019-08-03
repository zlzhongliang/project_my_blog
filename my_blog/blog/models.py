import datetime

from django.db import models

# Create your models here.

# 上传图片的地址
def user_avatar_path(instance, filename):
    """自定义用户头像保存路径和文件名"""
    # 获取源文件名的后缀
    ext = filename.split('.')[-1]
    # 通过当前时间字符串作为文件名
    file_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 拼接文件名和后缀
    file = 'blog/img/icon/'+file_name + '.' + ext
    # 使用当前用户id为路径
    return file


class UserModel(models.Model):
    username = models.CharField(max_length=32, default='0', verbose_name='昵称')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.CharField(max_length=64, unique=True, verbose_name='邮箱地址')
    # Falsh代表女
    sex = models.BooleanField(null=True, verbose_name='性别')
    icon = models.ImageField(upload_to=user_avatar_path,default='blog/img/user/icon.png', verbose_name='头像')
    is_delete = models.BooleanField(default=True, verbose_name='是否禁用')
    is_activate = models.BooleanField(default=False, verbose_name='是否激活')
    ticket = models.CharField(max_length=30,null=True, verbose_name='session值')
    logintime = models.DateTimeField(auto_now=True, verbose_name='最近登录')
    registertime = models.DateField(auto_now_add=True, verbose_name='注册时间')
    phonenumber = models.CharField(max_length=62, default='0', verbose_name='手机号码')
    my_url = models.CharField(max_length=100, default='/about', verbose_name='URL')
    reserve3 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve4 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve5 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve6 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve7 = models.CharField(max_length=62, default='0', verbose_name='保留字段')

    def __str__(self):
        return self.username

    @classmethod
    def createUser(cls, password, email, username):
        user = cls(password=password, email=email, username=username)
        return user


class NavModel(models.Model):
    nav_name = models.CharField(max_length=6,verbose_name='类别')
    issuedate = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    is_Show = models.BooleanField(default=True,verbose_name='是否显示')
    is_Delete = models.BooleanField(default=True,verbose_name='是否删除')
    Nav_root = models.ForeignKey('self',related_name='root_nav',null=True,on_delete=models.DO_NOTHING,blank=True,verbose_name='根')

    def __str__(self):
        return self.nav_name


    @classmethod
    def create_nav(cls, nav_name, nav_root):
        nav = cls(Nav_name=nav_name, Nav_root=nav_root)
        return nav


class ArticleModel(models.Model):
    # first_class = (
    #     (0, u'生活笔记'),
    #     (1, u'技术杂谈'),
    #     (2, u'福利专区'),
    # )
    title = models.CharField(max_length=200, verbose_name='文章标题')
    synopsis = models.CharField(max_length=500, default='0', verbose_name='大纲')
    content = models.TextField(verbose_name='正文')
    picture = models.ImageField(default='blog/img/article/default.png', verbose_name='图片')
    # first_classify = models.IntegerField(choices=first_class,verbose_name='一级分类')
    # second_classify = models.IntegerField(verbose_name='二级分类')
    # third_classify = models.IntegerField(verbose_name='三级分类')
    nav1 = models.ForeignKey(NavModel,related_name='nav1',default=1,on_delete=models.CASCADE,verbose_name='一级类别')
    nav2 = models.ForeignKey(NavModel,related_name='nav2',default=1, on_delete=models.CASCADE, verbose_name='二级类别')
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='作者')
    issuedate = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    alterdate = models.DateTimeField(auto_now=True,verbose_name='最近修改')
    sort = models.IntegerField(default=0,verbose_name='排序')
    browse_count = models.IntegerField(default=0, verbose_name="浏览次数")
    praise = models.IntegerField(default=0, verbose_name='点赞')
    share = models.IntegerField(default=0, verbose_name='分享')
    is_Delete = models.BooleanField(default=True,verbose_name='是否删除')
    is_show = models.BooleanField(default=True,verbose_name='是否显示')
    comment_num = models.IntegerField(default=0, verbose_name='评论次数')
    reserve3 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve4 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve5 = models.CharField(max_length=62, default='0', verbose_name='保留字段')

    def __str__(self):
        return self.title

    @classmethod
    def createArticle(cls,author, title,synopsis, content,nav1,nav2,is_show,picture):
        article = cls(author=author,title=title,synopsis=synopsis ,content=content,nav1=nav1,nav2=nav2,is_show=is_show,picture=picture)
        return article


class LinkModel(models.Model):
    link = models.CharField(max_length=50,verbose_name='链接地址')
    link_name = models.CharField(max_length=20,verbose_name='链接名称')
    sort = models.IntegerField(default=0, verbose_name='排序')
    issuedate = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    is_Delete = models.BooleanField(default=True,verbose_name='是否显示')
    def __str__(self):
        return self.link

    @classmethod
    def createArticle(cls, link, link_name, sort):
        link = cls(link=link, link_name=link_name, sort=sort)
        return link


class CommetModel(models.Model):
    commet=models.CharField(max_length=500, verbose_name='评论内容')
    author = models.ForeignKey(UserModel,related_name='author', on_delete=models.DO_NOTHING, verbose_name='作者')
    article = models.ForeignKey(ArticleModel, on_delete=models.DO_NOTHING,null=True,blank=True,verbose_name='文章')
    issuedate = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    alterdate = models.DateTimeField(auto_now=True,verbose_name='最近修改')
    classify = models.IntegerField(verbose_name='评论类型',null=True)
    sort = models.IntegerField(default=0,verbose_name='排序')
    is_Show = models.BooleanField(default=True,verbose_name='是否显示')
    is_Delete = models.BooleanField(default=True,verbose_name='是否删除')
    root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.DO_NOTHING,blank=True,verbose_name='根评论')
    parent = models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.DO_NOTHING,blank=True,verbose_name='父评论')
    reply_to = models.ForeignKey(UserModel,related_name='replies',null=True,on_delete=models.DO_NOTHING,blank=True,verbose_name='评论给谁')

    def __str__(self):
        return self.commet


    @classmethod
    def create_commet(cls, commet, author, article, classify,root,parent,reply_to):
        commet = cls(commet=commet, author=author, article=article, classify=classify,root=root,parent=parent,reply_to=reply_to)
        return commet


class LikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, verbose_name='用户')
    article = models.ForeignKey(ArticleModel, on_delete=models.DO_NOTHING,verbose_name='文章')
    sort = models.IntegerField(default=0, verbose_name='排序')
    issuedate = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    is_Delete = models.BooleanField(default=True,verbose_name='是否显示')
    def __str__(self):
        return self.article.title

    @classmethod
    def createLike(cls, user, article):
        like = cls(user=user, article=article)
        return like


