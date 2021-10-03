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
    jumbotron = Jumbotron.objects.all()
    context = {
        'title': 'Home',
        'blogs': blogs,
        'jumbotron' : jumbotron
    }
    return render(request, 'home/home.html', context)


def gallery(request):
    images = Blog.objects.all().order_by('-id')[:5:-1]
    context = {
        'title': 'Gallery',
        'images': images
    }
    return render(request, 'home/gallery.html', context)


def contact(request):
    if request.method == "POST":
        email = request.POST.get('email')
        message = request.POST.get('message')

        if email and message:
            obj = MyMessages.objects.create(email=email, messages=message)
            obj.save()
        messages.success(request, 'Thank you for the feedback !')
        return redirect('contact')
    context = {
        'title': 'Contact'
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
        'title': 'Login'
    }
    return render(request, 'home/login.html', context)


def logoutAdmin(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def adm(request):
    blogs = Blog.objects.all()
    context = {
        'title': 'Admin Page',
        'blogs': blogs
    }
    return render(request, 'home/admin.html', context)


@login_required(login_url='login')
def editArticle(request, pk):
    a = Blog.objects.get(id=pk)
    createArticleForm = CreateArticleForm(instance=a)

    if request.method == 'POST':
        createArticleForm = CreateArticleForm(
            request.POST, request.FILES, instance=a)
        if createArticleForm.is_valid():
            createArticleForm.save()
            return redirect('adm')

    context = {
        'title': 'Edit Akun',
        'form': createArticleForm
    }
    return render(request, 'home/edit.html', context)


@login_required(login_url='login')
def deleteArticle(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'GET':
        blog.delete()
        return redirect('/adm')
    context = {
        'title': 'Hapus article',
    }
    return render(request, 'home/delete.html', context)


@login_required(login_url='login')
def createArticle(request):
    createArticleForm = CreateArticleForm()
    if request.method == 'POST':
        createArticleForm = CreateArticleForm(request.POST, request.FILES)
        if createArticleForm.is_valid():
            createArticleForm.save()
            return redirect('adm')
    context = {
        'title': 'Create Article',
        'createForm': createArticleForm
    }
    return render(request, 'home/tambah_blog.html', context)


@login_required(login_url='login')
def viewMessages(request):
    mymessages = MyMessages.objects.all()
    context = {
        'title': 'View Messages',
        'mymessages': mymessages
    }
    return render(request, 'home/viewmessages.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    mymessages = MyMessages.objects.get(id=pk)
    if request.method == 'GET':
        mymessages.delete()
        messages.success(request, "message successfully deleted!")
        print(mymessages)
        print(type(mymessages))
        return redirect('view-messages')
    context = {
        'title': 'View Messages'
    }
    return render(request, 'home/deletemessages.html', context)


def searchArticle(request):
    blogs = reversed(Blog.objects.all().order_by('-id')[:5:-1])
    len_blogs = False
    print(type(blogs))
    qs = request.GET['qs']
    if request.method == 'GET':
        if request.GET['qs']:
            blogs = Blog.objects.filter(title__contains=qs)
            len_blogs = len(blogs)
    context = {
        'title': 'Search for '+qs,
        'blogs': blogs,
        'qs': qs,
        'count': len_blogs
    }
    return render(request, 'home/search.html', context)


def blog(request, blogid):
    blogs = Blog.objects.filter(slug=blogid)
    for blog in blogs:
        title = blog.title
        key = blog.key
        content = blog.content
        date = blog.date_created

    keystr = str(key)
    keycropped = keystr[0:3]
    suggestion = reversed(Blog.objects.filter(key__contains=keycropped)[0:3])
    context = {
        'title': title,
        'key': key,
        'content': content,
        'date': date,
        'blogs': blogs,
        'suggestion': suggestion
    }
    return render(request, 'home/blog.html', context)
