from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('gallery', views.gallery, name='gallery'),
    path('contact', views.contact, name='contact'),
    path('b/<str:blogid>/', views.blog, name='blog'),
    path('login/', views.loginAdmin, name='login'),
    path('logout/', views.logoutAdmin, name='logout'),
    path('adm/', views.adm, name='adm'),
    path('edit-article/<str:pk>/', views.editArticle, name='edit-article'),
    path('delete-article/<str:pk>/', views.deleteArticle, name='delete-article'),
    path('search/', views.searchArticle, name='search'),
    path('create-article/', views.createArticle, name='create-article'),
]