from django.contrib import admin

from .models import Article, Publisher, Vote

admin.site.register(Article)
admin.site.register(Publisher)
admin.site.register(Vote)
