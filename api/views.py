from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from comments.models import Comment
from friends.models import Friend, Follow
from posts.models import Post
from tags.models import Tag
from django.contrib.auth.models import User

# Create your views here.

@login_required
def get_posts(request,page="1"):
    #author/posts
    #author/author_id/posts

    # authenticated user
    user = request.user
    return Post.objects.all()

def get_post(request,post_id=None,page="1"):
    if post_id is not None:
        return Post.objects.get(post_id)
    else:
        # TODO: Import these enum visibilities
        # I don't like hardcoding...
        return Post.objects.filter(visibility=5).order_by('-date')

def friend_request(request,page="1"):
    return None

def get_friends(request,page="1"):
    return None

def is_friend(request,page="1"):
    return None
