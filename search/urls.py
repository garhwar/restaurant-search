# search/urls.py

from django.conf.urls import url
from search import views

from django.contrib.auth.decorators import login_required

app_name = 'search'

urlpatterns = [
    url(r'^search$', login_required(views.SearchView.as_view()),
        name='search'),
    url(r'^restaurant/(?P<pk>\d+)/$', login_required(
        views.RestaurantDetailView.as_view()), name='restaurant-detail'),
    url(r'^restaurant/(?P<res_id>\d+)/review/(?P<pk>\d+)$', login_required(
        views.ReviewUpdateView.as_view()), name='review-update'),
    url(r'^restaurant/(?P<res_id>\d+)/review/create$', login_required(
        views.ReviewCreateView.as_view()), name='review-create'),
]
