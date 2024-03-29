# restarant_auth/urls.py

from django.conf.urls import url
from restaurant_auth import views

app_name = 'restaurant_auth'

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.signin, name='login'),
    url(r'^logout/$', views.signout, name='logout'),
]
