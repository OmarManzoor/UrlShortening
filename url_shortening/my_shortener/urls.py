from django.conf.urls import url

from . import views

app_name = 'my_shortener'
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^/result/$', views.Result.as_view(), name='result'),
    url(r'^/result_redirect/(?P<short_word>[-\w]+)/$', views.ResultRedirect.as_view(), name='result_redirect'),
    url(r'^/(?P<short_word>[-\w]+)/$', views.Actual.as_view(), name='actual'),
]