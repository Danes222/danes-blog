from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers
from .serializers import BlogSerializer
from home.models import Blog

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def apiOverView(request):
    api_url_list = {
        'Overview' : 'api',
        'Latestblogs' : 'api/latest-blogs',
        'Allview' : 'api/blogs',
        'Detailview' : 'api/detail-blog/<str:pk>',
        'Create' : 'api/create',
        'Update' : 'api/update',
        'Delete' : 'api/delete',
    }
    return Response(api_url_list)

@api_view(['GET'])
def Blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def latestBlogs(request):
    blogs = reversed(Blog.objects.all().order_by('-id')[:3:-1])
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def detailBlog(request, blogslug):
    blogs = Blog.objects.filter(slug=blogslug)
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)
