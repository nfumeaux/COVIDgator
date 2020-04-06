from django.core.management.base import BaseCommand
from newsfeed.models import Article


class Command(BaseCommand):
    help = 'Prints the titles of all articles'

    def handle(self, *args, **options):
        for a in Article.objects.all():
            print(a.article_title)