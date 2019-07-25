from django.conf.urls import url

from blog import views

urlpatterns = [
url(r'^test$', views.test, name='test'),
url(r'^message$', views.message, name='message'),
url(r'^donate$', views.donate, name='donate'),
url(r'^exchange$', views.exchange, name='exchange'),
url(r'^project$', views.project, name='project'),
url(r'^index$', views.index, name='index'),
url(r'^article/(\d+)$', views.article, name='article'),
url(r'^main_article$', views.main_article, name='main_article'),
url(r'^quit$', views.quit, name='quit'),
url(r'^main$', views.main, name='main'),
url(r'^login$', views.login, name='login'),
url(r'^do_login$', views.do_login, name='do_login'),
url(r'^register$', views.register, name='register'),
url(r'^do_register$', views.do_register, name='do_register'),
url(r'^about$', views.about, name='about'),
url(r'^article_list/(\d+)/(\d+)/(\d+)$', views.article_list, name='article_list'),
url(r'^$', views.index, name='index'),
]
app_name = 'blog'