from django.urls import path

from . import views

urlpatterns = [
    # e.g. /newsfeed/
    path('', views.index, name='index'),
    # e.g. /newsfeed/7
    path('<int:article_id>/', views.detail, name='detail')
]