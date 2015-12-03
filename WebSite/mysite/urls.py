from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^randomUser$', views.randomUser, name='randomUser'),
    url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<id>[0-9]+)/(?P<grade>[1-4]+)$', views.detailByGrade, name='detailByGrade'),
    url(r'^predict/(?P<id>[0-9]+)/$', views.predict, name='predict'),
]