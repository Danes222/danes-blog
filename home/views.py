from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, request
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
def home(request):
    blogs = reversed(Blog.objects.all().order_by('-id')[:3:-1])
    context = {
        'title' : 'Home',
        'blogs' : blogs
    }
    return render(request, 'home/home.html', context)
def gallery(request):
    images = Blog.objects.all()
    context = {
        'title' : 'Gallery',
        'images' : images
    }
    return render(request, 'home/gallery.html', context)
def contact(request):
    context = {
        'title' : 'Contact'
    }
    return render(request, 'home/contact.html', context)

def loginAdmin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('adm')
        else:
            messages.info(request, 'Username or password are incorect!')
    context = {
        'title' : 'Login'
    }
    return render(request, 'home/login.html', context)
def logoutAdmin(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def adm(request):
    blogs = Blog.objects.all()
    context = {
        'title' : 'Admin Page',
        'blogs' : blogs
    }
    return render(request, 'home/admin.html', context)
def editArticle(request, pk):
    a = Blog.objects.get(id=pk)
    createArticleForm = CreateArticleForm(instance=a)
    
    if request.method == 'POST':
        createArticleForm = CreateArticleForm(request.POST,request.FILES, instance=a)
        if createArticleForm.is_valid():
            createArticleForm.save()
            return redirect('adm')

    context = {
        'judul' : 'Edit Akun',
        'title' : 'Edit Akun',
        'form' : createArticleForm
    }
    return render(request, 'home/edit.html', context)
def deleteArticle(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'GET':
        blog.delete()
        return redirect('/adm')
    context = {
        'judul' : 'Hapus article',
    }
    return render(request, 'home/delete.html', context)

def createArticle(request):
    createArticleForm = CreateArticleForm()
    if request.method == 'POST':
        createArticleForm = CreateArticleForm(request.POST,request.FILES)
        if createArticleForm.is_valid():
            createArticleForm.save()
            return redirect('adm')
    context = {
        'title' : 'Create Article',
        'createForm' : createArticleForm
    }
    return render(request, 'home/tambah_blog.html', context)

def searchArticle(request):
    blogs = Blog.objects.all()[:5:-1]
    print(type(blogs))
    qs = request.GET['qs']
    if request.method == 'GET':
        if request.GET['qs']:
            blogs = Blog.objects.filter(title__contains=qs)
    context = {
        'title' : 'Search for '+qs,
        'blogs' : blogs,
        'qs' : qs,
        'count' : len(blogs)
    }
    return render(request, 'home/search.html', context)



def blog(request, blogid):
    blogs = Blog.objects.filter(id=blogid)
    for blog in blogs:
        title = blog.title
        key = blog.key
        content = blog.content
        date = blog.date_created

    keystr = str(key)
    keycropped = keystr[0:3]
    suggestion = reversed(Blog.objects.filter(key__contains=keycropped)[0:3])
    context = {
        'title' : title,
        'key' : key,
        'content' : content,
        'date' : date,
        'blogs' : blogs,
        'suggestion' : suggestion
    }
    return render(request, 'home/blog.html', context)

