from django.urls import path

from . import views

app_name = 'newsfeed'
urlpatterns = [
    # e.g. /newsfeed/
    path('', views.index, name='index'),
    # e.g. /newsfeed/7
    path('<int:article_id>/', views.detail, name='detail'),
    # e.g. /newsfeed/7/vote
    path('<int:article_id>/vote', views.vote, name='vote'),
    # e.g. /newsfeed/7/comment
    path('<int:article_id>/comment', views.comment, name='comment')
]
