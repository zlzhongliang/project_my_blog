from django.contrib import admin

# Register your models here.
from blog.models import UserModel, ArticleModel, LinkModel


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','password','email','sex','icon','is_delete','is_activate','phonenumber','registertime')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','synopsis','picture','first_classify','second_classify','third_classify','author','issuedate','alterdate','sort','browse_count','praise','share','is_Delete')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'link', 'link_name', 'issuedate','sort', 'is_Delete')


admin.site.register(UserModel, UserAdmin)
admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(LinkModel, LinkAdmin)