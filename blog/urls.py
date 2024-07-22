from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:blog_id>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),
    path('<int:blog_id>/blog/', views.blog_view, name='blog_view'),
    path('register/', views.register, name='register'),
    path('categories/', views.categories, name='categories'),
    path('<int:category_id>/category/', views.category, name='category'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('search/', views.search, name='search'),
]
