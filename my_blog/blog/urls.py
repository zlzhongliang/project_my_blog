from django.conf.urls import url

from blog import views

urlpatterns = [
url(r'^test$', views.test, name='test'),
url(r'^link$', views.link, name='link'),
url(r'^change_url$', views.change_url, name='change_url'),
url(r'^change_sex$', views.change_sex, name='change_sex'),
url(r'^change_phone$', views.change_phone, name='change_phone'),
url(r'^change_icon$', views.change_icon, name='change_icon'),
url(r'^like_add$', views.like_add, name='like_add'),
url(r'^like_show$', views.like_show, name='like_show'),
url(r'^do_commet/(\d+)/(\d+)/(\d+)$', views.do_commet, name='do_commet'),
url(r'^message$', views.message, name='message'),
url(r'^donate$', views.donate, name='donate'),
url(r'^exchange$', views.exchange, name='exchange'),
url(r'^project$', views.project, name='project'),
url(r'^index$', views.index, name='index'),
url(r'^article/(\d+)$', views.article, name='article'),
url(r'^main_article$', views.main_article, name='main_article'),
url(r'^article_write/(\d+)$', views.article_write, name='article_write'),
url(r'^article_delete/(\d+)$', views.article_delete, name='article_delete'),
url(r'^do_article/(\d+)$', views.do_article, name='do_article'),
url(r'^quit$', views.quit, name='quit'),
url(r'^main$', views.main, name='main'),
url(r'^login$', views.login, name='login'),
url(r'^do_login$', views.do_login, name='do_login'),
url(r'^register$', views.register, name='register'),
url(r'^do_register$', views.do_register, name='do_register'),
url(r'^about$', views.about, name='about'),
url(r'^article_list/(\d+)$', views.article_list, name='article_list'),


url(r'^$', views.index, name='index'),
]
app_name = 'blog'