from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^blog/$', views.post_list, name='post_list'),
    url(r'^blog/top5/$', views.top_posts, name='top_posts'),

    url(r'^blog/(?P<id>\d+)/$', views.post_details),
    url(r'^blog/top5/(?P<id>\d+)/$', views.post_details),

    url(r'^post/new/$', views.new_post, name='new_post'),
]
