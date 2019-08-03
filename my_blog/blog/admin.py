from django.contrib import admin

# Register your models here.
from blog.models import UserModel, ArticleModel, LinkModel, CommetModel, LikeModel, NavModel


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','email','sex','icon','is_delete','is_activate','phonenumber','registertime')
    # 可以快捷编辑的选项
    list_editable = ["username","sex","phonenumber"]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','synopsis','picture','nav1','nav2','author','issuedate','alterdate','sort','browse_count','praise','share','is_Delete')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'link_name', 'issuedate','sort', 'is_Delete')


class CommetAdmin(admin.ModelAdmin):
    list_display = ('id', 'commet', 'author', 'article','issuedate','alterdate','classify','sort','is_Show', 'is_Delete','root','parent','reply_to')


class LikeAdmin(admin.ModelAdmin):
    like_display = ('id', 'user', 'article', 'issuedate','sort', 'is_Delete')


class NavAdmin(admin.ModelAdmin):
    like_display = ('id', 'nav_name')

admin.site.register(UserModel, UserAdmin)
admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(LinkModel, LinkAdmin)
admin.site.register(CommetModel, CommetAdmin)
admin.site.register(LikeModel, LikeAdmin)
admin.site.register(NavModel, NavAdmin)