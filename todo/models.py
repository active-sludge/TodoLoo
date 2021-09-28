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
    article_id = models.AutoField(primary_key=True)
    article_title = models.TextField(blank=True, null=True)
    article_abstract = models.TextField(blank=True, null=True)
    author_list = models.TextField(blank=True, null=True)
    keyword_list = models.TextField(blank=True, null=True)
    pub_date = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.article_id.__str__() + ", " + self.article_title + ", " + self.author_list
