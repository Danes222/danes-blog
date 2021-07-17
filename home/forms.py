from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog

class CreateArticleForm(ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"