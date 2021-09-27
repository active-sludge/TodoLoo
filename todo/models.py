from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    article_id = models.CharField(max_length=20)
    article_title = models.CharField(max_length=200)
    article_abstract = models.TextField(blank=True)
    author_list = models.TextField(blank=True)
    keyword_list = models.TextField(blank=True)
    pub_date = models.CharField(max_length=100)

    def __str__(self):
        return self.article_id + ", " + self.article_title + ", " + self.author_list
