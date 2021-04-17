from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Follow, Comment
from django.contrib.auth.models import User
from .forms import PostForm

# Create your views here.

@login_required(login_url='login')
def home(request):
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    form = PostForm(request.POST or None, files=request.FILES)      
    if form.is_valid():
        post=form.save(commit=False)
        post.user = request.user.profile
        post.save()
        return redirect('home')
    context = {
        'posts': posts,
        'form': form,
        'users':users,
    }
    return render(request, 'home.html', context)
      