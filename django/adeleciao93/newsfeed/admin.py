from django import forms
from django.contrib import admin

from .models import Article, Publisher, Vote, Comment, UserProfile


admin.site.register(Article)
admin.site.register(Publisher)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(UserProfile)
