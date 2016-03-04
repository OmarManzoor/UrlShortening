from django.conf.urls import url

from . import views

app_name = 'my_shortener'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^/result/$', views.result, name='result'),
    url(r'^/result_redirect/(?P<short_word>[-\w]+)/$', views.result_redirect, name='result_redirect'),
    url(r'^/(?P<short_word>[-\w]+)/$', views.actual, name='actual'),
]