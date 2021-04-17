from django import forms
from .models import Post, Profile, Comment
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image','name', 'caption')
