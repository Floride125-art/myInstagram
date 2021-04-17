from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Profile, Follow, Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import PostForm, UserCreationForm, UpdateUserProfileForm, CommentForm
from django.contrib.auth import login, authenticate

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
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    context = {
        'prof_form': prof_form,
        'images': images,

    }
    return render(request, 'profile.html', context)
def follow(request, pk):
    if request.method == 'GET':
        user = Profile.objects.get(pk=pk)
        follow = Follow(following=request.user.profile, followers=user)
        follow.save()
        
    return redirect('user_profile', user.user.username)
    
def unfollow(request, pk):
    if request.method == 'GET':
        user_ = Profile.objects.get(pk=pk)
        unfollow= Follow.objects.filter(following=request.user.profile, followers=user_)
        unfollow.delete()
        return redirect('user_profile', user_.user.username)    

@login_required(login_url='login')
def comment(request, pk):
    image = get_object_or_404(Post, pk=pk)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = image
            comment.user = request.user.profile
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    context = {
        'image': image,
        'form': form,
        'is_liked': is_liked,
        'total_likes': image.total_likes()
    }
    return render(request, 'post.html', context)