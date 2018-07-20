from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
       #url(r'^',views.index,name='index'),
       url(r'^index/$', views.index,name='index'),
       #url(r'^search/',views.search, name = 'search'),
       url(r'^stats/',views.stats,name = 'stats'),
       #url(r'^scrapy/search/',views.scsearch, name = 'scsearch'),
       url(r'^details/(?P<comp>.*)/',views.details,name = 'details'),
]