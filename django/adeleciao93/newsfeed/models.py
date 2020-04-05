import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    article_url = models.CharField(max_length=200)  # TODO move to useful url
    # article_url = models.URLField(max_length=200)
    article_publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    article_positive_votes = models.IntegerField(default=0)
    article_negative_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.article_date >= timezone.now() - datetime.timedelta(days=2)

    def date_str(self):
        return self.article_date.date()

    def rating_str(self):
        total_votes = self.article_negative_votes + self.article_positive_votes
        if total_votes > 0:
            return '{0:.1f}'.format(self.article_positive_votes*100/total_votes) + '% (' + str(total_votes) + ' votes )'
        else:
            return 'unknown'


class Vote(models.Model):
    vote_value = models.IntegerField(default=0) # can be 1 if user liked or -1 if user disliked
    vote_user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_article = models.ForeignKey(Article, on_delete=models.CASCADE)


# class Comment(models.Model):
#     comment_text = models.CharField(max_length=200)
#     comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
#     article_date = models.DateTimeField('date published')
#     comment_positive_votes = models.IntegerField(default=0)
#     comment_negative_votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.comment_text
