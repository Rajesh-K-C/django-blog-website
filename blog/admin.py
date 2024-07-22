from django.contrib import admin
from .models import Blog, Category, Profile

# Register your models here.

admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Profile)