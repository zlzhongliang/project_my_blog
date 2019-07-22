# Generated by Django 2.2.3 on 2019-07-21 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='0', max_length=32, verbose_name='昵称')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('email', models.CharField(max_length=64, unique=True, verbose_name='邮箱地址')),
                ('sex', models.BooleanField(null=True, verbose_name='性别')),
                ('icon', models.ImageField(default='blog/img/user/icon.png', upload_to='', verbose_name='头像')),
                ('is_delete', models.BooleanField(default=True, verbose_name='是否禁用')),
                ('is_activate', models.BooleanField(default=False, verbose_name='是否激活')),
                ('ticket', models.CharField(max_length=30, null=True, verbose_name='session值')),
                ('logintime', models.DateTimeField(auto_now=True, verbose_name='最近登录')),
                ('registertime', models.DateField(auto_now_add=True, verbose_name='注册时间')),
                ('phonenumber', models.CharField(default='0', max_length=62, verbose_name='手机号码')),
                ('reserve2', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve3', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve4', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve5', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve6', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve7', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='正文')),
                ('picture', models.ImageField(default='blog/img/user/icon.png', upload_to='', verbose_name='图片')),
                ('first_classify', models.IntegerField(verbose_name='一级分类')),
                ('second_classify', models.IntegerField(verbose_name='二级分类')),
                ('third_classify', models.IntegerField(verbose_name='三级分类')),
                ('issuedate', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('alterdate', models.DateTimeField(auto_now=True, verbose_name='最近修改')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('browse_count', models.IntegerField(default=0, verbose_name='浏览次数')),
                ('praise', models.IntegerField(default=0, verbose_name='点赞')),
                ('share', models.IntegerField(default=0, verbose_name='分享')),
                ('is_Delete', models.BooleanField(default=True, verbose_name='是否显示')),
                ('reserve1', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve2', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve3', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve4', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('reserve5', models.CharField(default='0', max_length=62, verbose_name='保留字段')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.UserModel', verbose_name='作者')),
            ],
        ),
    ]
