from django.contrib import admin

# Register your models here.
from blog.models import UserModel, ArticleModel, LinkModel,CommetModel,ChildCommetModel


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','email','sex','icon','is_delete','is_activate','phonenumber','registertime')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','synopsis','picture','first_classify','second_classify','third_classify','author','issuedate','alterdate','sort','browse_count','praise','share','is_Delete')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'link_name', 'issuedate','sort', 'is_Delete')


class CommetAdmin(admin.ModelAdmin):
    list_display = ('id', 'commet', 'author', 'article','issuedate','classify','sort','is_Show', 'is_Delete',)


class ChildCommetAdmin(admin.ModelAdmin):
    list_display = ('id', 'commet', 'author','issuedate','father_commet','sort','is_Show', 'is_Delete',)


admin.site.register(UserModel, UserAdmin)
admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(LinkModel, LinkAdmin)
admin.site.register(CommetModel, CommetAdmin)
admin.site.register(ChildCommetModel, ChildCommetAdmin)