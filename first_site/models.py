from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    category = models.CharField(max_length=100, default="etc", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_key = models.CharField(max_length=12)



