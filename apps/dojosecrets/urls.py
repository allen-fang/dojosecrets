from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^secrets$', views.secrets),
    url(r'^post$', views.post),
    url(r'^logout$', views.logout),
    url(r'^like/(?P<id>\d+)$', views.like_post),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^secrets/popular$', views.popular),
]