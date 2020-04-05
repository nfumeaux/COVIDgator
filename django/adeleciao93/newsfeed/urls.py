from django.urls import path

from . import views

app_name = 'newsfeed'
urlpatterns = [
    # e.g. /newsfeed/
    path('', views.index, name='index'),
    # e.g. /newsfeed/7
    path('<int:article_id>/', views.detail, name='detail'),
    # e.g. /newsfeed/
    path('<int:article_id>/vote', views.vote, name='vote')
]
