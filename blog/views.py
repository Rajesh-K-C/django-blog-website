from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Category, Profile
from .forms import BlogForm, ProfileUpdateForm, UserRegistrationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

def index(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'blogs': blogs, 'query':  ''})

@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_edit(request, blog_id: int):
    blog = get_object_or_404(Blog, pk=blog_id, user = request.user) 
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form':form})

@login_required
def blog_delete(request, blog_id: int):
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request, 'blog/blog_confirm_delete.html', {'blog':blog})

def blog_view(request, blog_id: int):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/blog_view.html', {"blog": blog })

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def categories(request):
    categories = Category.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)
    # total_blogs = categories.aggregate(total=Count('blog'))['total']
    
    # categories = Category.objects.all().order_by('category')
    return render(request, 'blog/categories.html', {'categories': categories})

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    blogs = Blog.objects.filter(category=category_id).order_by('-created_at')
    # total_blogs = categories.aggregate(total=Count('blog'))['total']
    print(categories)
    return render(request, 'blog/index.html',  {'blogs': blogs, 'category':  category})


def search(request):
    query = request.GET.get('query')
    if not query:
        query = ' '
        blogs = None
    else:
        blogs = Blog.objects.filter(title__icontains=query).order_by('-created_at')
    return render(request, 'blog/index.html', {'blogs': blogs, 'query':  query})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    user = get_object_or_404(User.objects.select_related('profile'), username=request.user)
    blogs = Blog.objects.filter(user_id=user.id)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
        'blogs': blogs
    }
    return render(request, 'blog/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'blog/change_password.html', {'form': form})
