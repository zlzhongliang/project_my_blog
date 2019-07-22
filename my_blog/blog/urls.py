from django.conf.urls import url

from blog import views

urlpatterns = [
url(r'^index$', views.index, name='index'),
url(r'^main_article$', views.main_article, name='main_article'),
url(r'^quit$', views.quit, name='quit'),
url(r'^main$', views.main, name='main'),
url(r'^login$', views.login, name='login'),
url(r'^do_login$', views.do_login, name='do_login'),
url(r'^register$', views.register, name='register'),
url(r'^do_register$', views.do_register, name='do_register'),
url(r'^about$', views.about, name='about'),
url(r'^resources$', views.resources, name='resources'),
url(r'^skill$', views.skill, name='skill'),
url(r'^life$', views.life, name='life'),
url(r'^$', views.index, name='index'),
]
app_name = 'blog'