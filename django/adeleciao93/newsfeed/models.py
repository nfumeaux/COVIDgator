import datetime
from django.db import models
from django.utils import timezone


class Publisher(models.Model):
    publisher_name = models.CharField(max_length=200)

    def __str__(self):
        return self.publisher_name


# class Rating(models.Model):
#     rating_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return str(self.votes)


class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_date = models.DateTimeField('date published')
    article_url = models.CharField(max_length=200)
    article_publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    article_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=2)

