from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiOverView, name='api'),
    path('blogs', views.Blogs, name='blogs'),
    path('latest-blogs', views.latestBlogs, name='latest-blogs'),
    path('detail-blog/<str:blogslug>', views.detailBlog, name='detail-blog'),
]
