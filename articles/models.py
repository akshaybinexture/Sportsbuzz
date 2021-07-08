from django.db import models
import uuid
from django.urls import reverse
import math
from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    article_id = models.IntegerField(primary_key=True, unique=True, default=1)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    heading = models.CharField(max_length=150)
    article_link = models.TextField()
    category = models.CharField(max_length=20)
    date_posted = models.DateTimeField()
    img_url = models.TextField()

    def __str__(self):
        return self.heading

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.date_posted

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"




class Article_detail(models.Model):
    article_detail_id = models.ForeignKey(Article, to_field='article_id', on_delete=models.CASCADE, unique=True)
    # article_detail_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    heading = models.TextField()
    img_url = models.TextField(null=True)
    date_posted = models.DateTimeField()
    description = models.TextField()
    tweet_url = models.TextField(null=True)
    likes = models.ManyToManyField(User, related_name='articles_article_detail')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.heading


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.article.heading, self.name.username)

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.date_added

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"




class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


