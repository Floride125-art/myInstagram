from django.urls import path
from .views import home, signup, profile, user_profile, follow, unfollow, comment, like
from app.views import PostLikeToggle, PostLikeAPIToggle


urlpatterns = [

    path('', home , name ='home'),
    #path('create_post/', create_post , name ='create_post'),
    path('signup/', signup , name='signup'),
    path('profile/<username>/', profile, name='profile'),
    path('user_profile/<username>/', user_profile, name='user_profile'),
    path('follow/<pk>', follow, name='follow'),
    path('unfollow/<pk>',unfollow, name='unfollow'),
    path('post/<pk>', comment, name='comment'),
    path('post/<id>/like', PostLikeToggle.as_view(), name='liked'),
    path('api/post/<id>/like', PostLikeAPIToggle.as_view(), name='liked-api'),
    path('like', like, name='like_post'),


]