from django.db import models
from django.db.models.fields import DateTimeField, SlugField

# Create your models here.
class Blog(models.Model):
    baner = models.ImageField(null=True, blank=True, default='defaultimages/default.png')
    key = models.CharField(max_length=200)
    title = models.TextField(max_length=300)
    content = models.TextField()
    date_created = DateTimeField(auto_now_add=True, null=True)
    slug = SlugField()

    def __str__(self):
        return self.title

class MyMessages(models.Model):
    email = models.EmailField(max_length=200)
    messages = models.TextField(max_length=300)

    def __str__(self):
        return self.email