import requests
import re
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.utils import timezone

from newsfeed.models import Article, Publisher


class Command(BaseCommand):
    help = 'Populates articles with data from a specified feed'

    # hardcoded stuff
    url = 'http://feeds.nature.com/nature/rss/current?x=1'
    # url = 'http://feeds.bbci.co.uk/news/world/rss.xml'  # url for the feed
    publisher_name = 'Nature'
    b_write = True

    def handle(self, *args, **options):
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.content, features='xml')

        # find titles for filtering
        relevant_soup = soup.find_all('title', string=re.compile('virus'))
        relevant_soup2 = soup.find_all('title', string=re.compile('COVID'))

        relevant_titles = []
        for title in relevant_soup:
            relevant_title = title.text
            relevant_titles.append(relevant_title)

        for title in relevant_soup2:
            relevant_title = title.text
            relevant_titles.append(relevant_title)

        set_titles = set(relevant_titles)
        list_titles = list(set_titles)

        # find all items and creare list of dictionaries
        items = soup.find_all('item')

        news_items = []

        for item in items:
            news_item = {}
            news_item['title'] = item.title.text
            news_item['link'] = item.link.text
            news_item['source'] = self.publisher_name
            news_items.append(news_item)

        # filtering for relevant titles
        news_items_filt = [d for d in news_items if d['title'] in list_titles]

        for item in news_items_filt:
            print(item['title'])
            if self.b_write:
                # check if publisher exists in database by name
                try:
                    publisher = Publisher.objects.get(publisher_name=item['source'])
                except Exception as e:
                    publisher = Publisher.objects.create(publisher_name=item['source'])
                    print('Created publisher: ' + item['source'])
                Article.objects.create(
                    article_title=item['title'],
                    article_date=timezone.now(),
                    article_url=item['link'],
                    article_publisher=publisher,
                    article_positive_votes=0,
                    article_negative_votes=0,
                )
