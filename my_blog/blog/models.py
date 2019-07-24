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
    file = 'blog/img/carouse/'+file_name + '.' + ext
    # 使用当前用户id为路径
    return file


class UserModel(models.Model):
    username = models.CharField(max_length=32, default='0', verbose_name='昵称')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.CharField(max_length=64, unique=True, verbose_name='邮箱地址')
    # Falsh代表女
    sex = models.BooleanField(null=True, verbose_name='性别')
    icon = models.ImageField(default='blog/img/user/icon.png', verbose_name='头像')
    is_delete = models.BooleanField(default=True, verbose_name='是否禁用')
    is_activate = models.BooleanField(default=False, verbose_name='是否激活')
    ticket = models.CharField(max_length=30,null=True, verbose_name='session值')
    logintime = models.DateTimeField(auto_now=True, verbose_name='最近登录')
    registertime = models.DateField(auto_now_add=True, verbose_name='注册时间')
    phonenumber = models.CharField(max_length=62, default='0', verbose_name='手机号码')
    reserve2 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve3 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve4 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve5 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve6 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve7 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    @classmethod
    def createUser(cls, password, email, username):
        user = cls(password=password, email=email, username=username)
        return user


class ArticleModel(models.Model):
    first_class = (
        (0, u'生活笔记'),
        (1, u'技术杂谈'),
        (2, u'福利专区'),
    )
    title = models.CharField(max_length=200, verbose_name='文章标题')
    content = models.TextField(verbose_name='正文')
    picture = models.ImageField(default='blog/img/article/default.png', verbose_name='图片')
    first_classify = models.IntegerField(choices=first_class,verbose_name='一级分类')
    second_classify = models.IntegerField(verbose_name='二级分类')
    third_classify = models.IntegerField(verbose_name='三级分类')
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='作者')
    issuedate = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    alterdate = models.DateTimeField(auto_now=True,verbose_name='最近修改')
    sort = models.IntegerField(default=0,verbose_name='排序')
    browse_count = models.IntegerField(default=0, verbose_name="浏览次数")
    praise = models.IntegerField(default=0, verbose_name='点赞')
    share = models.IntegerField(default=0, verbose_name='分享')
    is_Delete = models.BooleanField(default=True,verbose_name='是否显示')
    synopsis = models.CharField(max_length=500, default='0', verbose_name='大纲')
    reserve2 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve3 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve4 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    reserve5 = models.CharField(max_length=62, default='0', verbose_name='保留字段')
    @classmethod
    def createArticle(cls, title, content, picture, first_classify, second_classify, third_classify):
        article = cls(title=title, content=content, picture=picture, first_classify=first_classify, second_classify=second_classify, third_classify=third_classify)
        return article
