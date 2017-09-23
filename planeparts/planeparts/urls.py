#planeparts URL Configuration

from django.conf.urls import url, include
from django.contrib.auth import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'', include('manager.urls')),
]
