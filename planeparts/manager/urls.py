from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^admin/', views.admin),
    url(r'^search/', views.search_parts, name='search'),
    #url(r'^contact/', views.contact, name='contact'),
    url(r'^new/$', views.new_type, name='new_type'),
    url(r'^parts/([0-9]+)/$', views.part_detail, name='part_detail'),
    url(r'^parts/([0-9]+)/edit/$', views.edit_type, name='edit_type'),
    url(r'^parts/([0-9]+)/remove/$', views.delete_type, name='delete_type'),
]
