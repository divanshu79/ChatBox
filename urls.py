from django.conf.urls import patterns,include,url
from . import views

app_name = 'chat'

urlpatterns =  patterns('',
    url(r'^login/$', 'chat.views.login', name='login'),
    url(r'^page/$', 'chat.views.page', name='page'),
                        )