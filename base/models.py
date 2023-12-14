from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    link = models.URLField()
    pages = models.PositiveIntegerField()
    year = models.IntegerField()
    poster = models.ImageField()
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    @property
    def imageURL(self):
        try :
            url = self.poster.url
        except:
            url = ''
        return url


class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()