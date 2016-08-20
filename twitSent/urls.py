from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as view3
from django.conf.urls import include

urlpatterns = [ #'twitter_auth.views',
    url(r'^$', views.main, name='main'),
    url(r'^callback/$', views.callback, name='auth_return'),
    url(r'^logout/$', views.unauth, name='oauth_unauth'),
    url(r'^auth/$', views.auth, name='oauth_auth'),
    url(r'^info/$', views.info, name='info'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='delete'),
    url(r'^urls/$', views.url_list),
	url(r'^urls/(?P<pk>[0-9]+)/$', views.url_detail),
	url(r'^api-token-auth/', view3.obtain_auth_token),
]